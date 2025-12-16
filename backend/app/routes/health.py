from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check():
    """Check API health status."""
    return {"status": "healthy", "service": "cema-backend"}
