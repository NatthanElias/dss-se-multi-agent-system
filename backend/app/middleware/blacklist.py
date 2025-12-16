from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import logging

class BlacklistMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, blacklist_file: str = "blacklist.txt"):
        super().__init__(app)
        self.blacklist_file = blacklist_file
        self.logger = logging.getLogger("blacklist")

    async def dispatch(self, request: Request, call_next):
        # Allow requests to /docs, /redoc, /openapi.json to load UI even if IP issues (optional)
        if request.url.path in ["/docs", "/redoc", "/openapi.json"]:
             return await call_next(request)

        client_ip = request.client.host
        
        # Simple reload on every request to allow dynamic updates without restart
        # For production with high traffic, caching would be better
        try:
            with open(self.blacklist_file, "r") as f:
                blacklist = {line.strip() for line in f if line.strip() and not line.startswith("#")}
                
            if client_ip in blacklist:
                self.logger.warning(f"Blocked request from blacklisted IP: {client_ip}")
                raise HTTPException(status_code=403, detail="Your IP address is banned.")
                
        except FileNotFoundError:
            pass # No blacklist file, allow all
            
        response = await call_next(request)
        return response
