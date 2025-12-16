from fastapi import APIRouter, HTTPException
from app.controllers import agent_controller

router = APIRouter(tags=["Agent"])


@router.post("/api/run")
async def run_agent(body: dict):
    """
    Execute the agent and return all events.
    
    Request body (camelCase):
    {
        "appName": "cema_system",
        "userId": "user_123",
        "sessionId": "session_456",
        "newMessage": {
            "role": "user",
            "parts": [{"text": "Your question here"}]
        }
    }
    """
    try:
        # Extract fields from camelCase body
        app_name = body.get("appName")
        user_id = body.get("userId")
        session_id = body.get("sessionId")
        new_message = body.get("newMessage")
        
        if not all([app_name, user_id, session_id, new_message]):
            raise HTTPException(
                status_code=400, 
                detail="Missing required fields: appName, userId, sessionId, newMessage"
            )
        
        events = await agent_controller.execute_agent(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id,
            message=new_message
        )
        return events
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
