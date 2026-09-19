import time
import uuid
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.security import verify_access_token
import jwt

logger = logging.getLogger(__name__)

class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # We only audit state-changing requests
        state_changing_methods = {"POST", "PUT", "PATCH", "DELETE"}
        
        # We also skip audit for the actual auth/login endpoint if it exists
        
        if request.method not in state_changing_methods:
            return await call_next(request)
            
        # Try to extract user info from auth header
        user_id = "anonymous"
        role = "UNAUTHENTICATED"
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                payload = verify_access_token(token)
                user_id = payload.get("sub", "unknown")
                role = payload.get("role", "UNKNOWN")
            except Exception:
                pass
                
        # Try to extract case_id from path parameters or body
        case_id = None
        # Example naive extraction from path: /cases/{case_id}/something
        path_parts = request.url.path.split("/")
        if "cases" in path_parts:
            idx = path_parts.index("cases")
            if len(path_parts) > idx + 1:
                case_id = path_parts[idx + 1]
                
        correlation_id = str(uuid.uuid4())
        ip_address = request.client.host if request.client else "unknown"
        timestamp = time.time()
        
        # The request logic is executed
        response = await call_next(request)
        
        # Log the audit event
        # In reality, this would write to an `audit_log` DB table
        audit_event = {
            "user_id": user_id,
            "role": role,
            "endpoint": request.url.path,
            "method": request.method,
            "case_id": case_id,
            "ip_address": ip_address,
            "correlation_id": correlation_id,
            "timestamp": timestamp,
            "status_code": response.status_code
        }
        
        logger.info(f"AUDIT EVENT: {audit_event}")
        
        return response
