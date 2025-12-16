from fastapi import APIRouter, HTTPException
from app.controllers import session_controller

router = APIRouter(tags=["Sessions"])


@router.post("/api/apps/{app_name}/users/{user_id}/sessions/{session_id}")
async def create_session(app_name: str, user_id: str, session_id: str, body: dict = None):
    """Create a new session with optional initial state."""
    try:
        session = await session_controller.create_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id,
            state=body or {}
        )
        return session
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/apps/{app_name}/users/{user_id}/sessions/{session_id}")
async def get_session(app_name: str, user_id: str, session_id: str):
    """Get session details."""
    session = await session_controller.get_session(app_name, user_id, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session
