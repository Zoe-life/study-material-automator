"""JWT Authentication"""
from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, get_jwt_identity, verify_jwt_in_request
from datetime import timedelta

jwt = JWTManager()


def init_jwt(app):
    """Initialize JWT manager"""
    jwt_secret = app.config.get('JWT_SECRET_KEY')
    if not jwt_secret or jwt_secret == 'your-jwt-secret-key-here':
        import secrets
        jwt_secret = secrets.token_hex(32)
        print(f"WARNING: Using auto-generated JWT secret. Set JWT_SECRET_KEY in .env for production!")
    app.config['JWT_SECRET_KEY'] = jwt_secret
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    jwt.init_app(app)
    return jwt


def jwt_required(fn):
    """Decorator to require JWT authentication"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return fn(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': 'Authentication required', 'message': str(e)}), 401
    return wrapper


def get_current_user():
    """Get current authenticated user ID"""
    try:
        verify_jwt_in_request()
        return get_jwt_identity()
    except Exception:
        return None


def generate_tokens(user_id):
    """Generate access and refresh tokens"""
    access_token = create_access_token(identity=user_id)
    refresh_token = create_refresh_token(identity=user_id)
    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }
