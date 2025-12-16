import uvicorn
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI

# Load environment variables from cema_system/.env
env_path = Path(__file__).parent / "cema_system" / ".env"
load_dotenv(env_path)

from app.routes import health, session, agent
from app.middleware.blacklist import BlacklistMiddleware

# Create FastAPI application
app = FastAPI(
    title="CEMA Agent Service API",
    description="Agent Service - Microserviço para execução do Sistema Multiagente CEMA",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Register Middleware
app.add_middleware(BlacklistMiddleware, blacklist_file="blacklist.txt")

# Register routes (all with /api prefix for Gateway routing)
app.include_router(health.router)
app.include_router(session.router)
app.include_router(agent.router)



# Root endpoint
@app.get("/")
async def root():
    return {"message": "CEMA Backend API", "docs": "/docs"}

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8080, reload=True)
