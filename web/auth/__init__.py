"""Authentication module"""
from .jwt_auth import init_jwt, jwt_required, get_current_user
from .oauth import init_oauth, google_bp, microsoft_bp, apple_bp

__all__ = ['init_jwt', 'jwt_required', 'get_current_user', 'init_oauth', 'google_bp', 'microsoft_bp', 'apple_bp']
