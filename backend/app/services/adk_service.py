import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from cema_system.agent import root_agent

# Global session service (stateful, keeps sessions in memory)
session_service = InMemorySessionService()

# Thread pool for running sync code
executor = ThreadPoolExecutor(max_workers=4)


async def create_session(app_name: str, user_id: str, session_id: str, state: dict = None):
    """Create a new session in memory."""
    session = await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
        state=state or {}
    )
    return {
        "id": session.id,
        "appName": session.app_name,
        "userId": session.user_id,
        "state": session.state,
        "events": [],
        "lastUpdateTime": datetime.now().isoformat()
    }


async def get_session(app_name: str, user_id: str, session_id: str):
    """Get session by ID."""
    session = await session_service.get_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )
    if not session:
        return None
    return {
        "id": session.id,
        "appName": session.app_name,
        "userId": session.user_id,
        "state": session.state,
        "events": [{"content": e.content} for e in session.events] if session.events else [],
        "lastUpdateTime": datetime.now().isoformat()
    }


def _run_agent_sync(app_name: str, user_id: str, session_id: str, content):
    """Synchronous agent execution in separate thread."""
    # Create fresh runner and session service for this thread
    sync_session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent, 
        app_name=app_name, 
        session_service=sync_session_service
    )
    
    # Create session synchronously
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(
            sync_session_service.create_session(
                app_name=app_name,
                user_id=user_id,
                session_id=session_id,
                state={}
            )
        )
        
        # Collect events
        events = []
        for event in runner.run(
            user_id=user_id,
            session_id=session_id,
            new_message=content
        ):
            event_data = {
                "author": getattr(event, 'author', None),
                "invocationId": getattr(event, 'invocation_id', None),
            }
            
            if hasattr(event, 'content') and event.content:
                event_data["content"] = {
                    "role": getattr(event.content, 'role', None),
                    "parts": []
                }
                if hasattr(event.content, 'parts') and event.content.parts:
                    for p in event.content.parts:
                        if hasattr(p, 'text') and p.text:
                            event_data["content"]["parts"].append({"text": p.text})
            
            events.append(event_data)
        
        return events
    finally:
        loop.close()


async def run_agent(app_name: str, user_id: str, session_id: str, message: dict):
    """Execute the agent and return all events."""
    # Build the message content
    parts = []
    for part in message.get("parts", []):
        if "text" in part:
            parts.append(types.Part.from_text(text=part["text"]))
    
    content = types.Content(role=message.get("role", "user"), parts=parts)
    
    try:
        # Run sync code in thread pool
        loop = asyncio.get_event_loop()
        events = await loop.run_in_executor(
            executor,
            _run_agent_sync,
            app_name,
            user_id,
            session_id,
            content
        )
        return events
    except Exception as e:
        return [{
            "author": "system",
            "error": str(e),
            "errorType": type(e).__name__
        }]
