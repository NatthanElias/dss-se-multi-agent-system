from app.services import adk_service


async def execute_agent(app_name: str, user_id: str, session_id: str, message: dict):
    """Execute the agent and return events."""
    return await adk_service.run_agent(app_name, user_id, session_id, message)
