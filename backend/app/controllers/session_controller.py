from app.services import adk_service


async def create_session(app_name: str, user_id: str, session_id: str, state: dict = None):
    """Create a new session and return session data."""
    return await adk_service.create_session(app_name, user_id, session_id, state)


async def get_session(app_name: str, user_id: str, session_id: str):
    """Get session data by ID."""
    return await adk_service.get_session(app_name, user_id, session_id)
