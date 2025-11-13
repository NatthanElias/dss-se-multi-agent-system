import os
from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app

# Get base ADK FastAPI app
app: FastAPI = get_fast_api_app(
    agents_dir=os.path.dirname(__file__),  # Directory containing cema_system/
    allow_origins=["*"],  # CORS - for for testing * is ok
    web=False  # Disable dev UI in production
)

# Add custom health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "cema-backend",
        "agent": "cema_system"
    }

# Add agent info endpoint (optional)
@app.get("/info")
async def agent_info():
    try:
        from cema_system.agent import root_agent
        return {
            "agent_name": root_agent.name,
            "description": root_agent.description
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
