import hashlib
import secrets
import time
from typing import Optional, Dict
from fastapi import Request, HTTPException, status
from fastapi.responses import RedirectResponse
from app.core.config import settings


class AuthManager:
    """Simple session-based authentication for admin panel."""
    
    def __init__(self):
        self.sessions: Dict[str, Dict] = {}
        self.session_timeout = 3600  # 1 hour
        self.session_secret = settings.get_session_secret()
    
    def generate_session_token(self) -> str:
        """Generate a secure session token."""
        return secrets.token_urlsafe(32)
    
    def hash_password(self, password: str) -> str:
        """Hash a password for secure comparison."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str) -> bool:
        """Verify a password against the configured admin password."""
        admin_password = settings.get_decrypted_admin_password()
        return password == admin_password
    
    def create_session(self, request: Request) -> str:
        """Create a new authenticated session."""
        token = self.generate_session_token()
        self.sessions[token] = {
            'created_at': time.time(),
            'last_accessed': time.time(),
            'ip_address': request.client.host if request.client else 'unknown'
        }
        return token
    
    def get_session_token_from_request(self, request: Request) -> Optional[str]:
        """Extract session token from request cookies."""
        return request.cookies.get('admin_session')
    
    def is_session_valid(self, token: str) -> bool:
        """Check if a session token is valid and not expired."""
        if not token or token not in self.sessions:
            return False
        
        session = self.sessions[token]
        current_time = time.time()
        
        # Check if session has expired
        if current_time - session['last_accessed'] > self.session_timeout:
            del self.sessions[token]
            return False
        
        # Update last accessed time
        session['last_accessed'] = current_time
        return True
    
    def invalidate_session(self, token: str):
        """Invalidate a session token."""
        if token in self.sessions:
            del self.sessions[token]
    
    def cleanup_expired_sessions(self):
        """Remove expired sessions."""
        current_time = time.time()
        expired_tokens = [
            token for token, session in self.sessions.items()
            if current_time - session['last_accessed'] > self.session_timeout
        ]
        for token in expired_tokens:
            del self.sessions[token]
    
    def require_auth(self, request: Request) -> bool:
        """Check if request is authenticated, raise HTTPException if not."""
        token = self.get_session_token_from_request(request)
        if not self.is_session_valid(token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )
        return True
    
    def get_session_count(self) -> int:
        """Get the number of active sessions."""
        self.cleanup_expired_sessions()
        return len(self.sessions)


# Global auth manager instance
auth_manager = AuthManager()


def require_admin_auth(request: Request) -> bool:
    """Dependency function to require admin authentication."""
    return auth_manager.require_auth(request)


def is_authenticated(request: Request) -> bool:
    """Check if request is authenticated without raising exception."""
    token = auth_manager.get_session_token_from_request(request)
    return auth_manager.is_session_valid(token) 