from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/api/health")
async def health_check():
    """Check API health status."""
    return {"status": "healthy", "service": "agent-service"}
