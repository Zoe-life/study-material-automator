"""OAuth 2.0 Authentication Providers"""
from flask import Blueprint, redirect, url_for, jsonify, session, current_app
from authlib.integrations.flask_client import OAuth
from datetime import datetime

oauth = OAuth()
google_bp = Blueprint('google_auth', __name__)
microsoft_bp = Blueprint('microsoft_auth', __name__)
apple_bp = Blueprint('apple_auth', __name__)


def init_oauth(app):
    """Initialize OAuth providers"""
    oauth.init_app(app)
    
    # Google OAuth
    oauth.register(
        name='google',
        client_id=app.config.get('GOOGLE_CLIENT_ID'),
        client_secret=app.config.get('GOOGLE_CLIENT_SECRET'),
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'}
    )
    
    # Microsoft OAuth
    oauth.register(
        name='microsoft',
        client_id=app.config.get('MICROSOFT_CLIENT_ID'),
        client_secret=app.config.get('MICROSOFT_CLIENT_SECRET'),
        server_metadata_url='https://login.microsoftonline.com/common/v2.0/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'}
    )
    
    # Apple OAuth
    oauth.register(
        name='apple',
        client_id=app.config.get('APPLE_CLIENT_ID'),
        client_secret=app.config.get('APPLE_CLIENT_SECRET'),
        server_metadata_url='https://appleid.apple.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email name'}
    )
    
    return oauth


# Google OAuth routes
@google_bp.route('/login')
def google_login():
    """Initiate Google OAuth login"""
    redirect_uri = url_for('google_auth.google_callback', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@google_bp.route('/callback')
def google_callback():
    """Handle Google OAuth callback"""
    try:
        token = oauth.google.authorize_access_token()
        user_info = token.get('userinfo')
        
        if not user_info:
            return jsonify({'error': 'Failed to get user info from Google'}), 400
        
        # Store OAuth info in session
        session['oauth_user'] = {
            'provider': 'google',
            'id': user_info.get('sub'),
            'email': user_info.get('email'),
            'name': user_info.get('name'),
            'picture': user_info.get('picture')
        }
        
        # Redirect to frontend with success
        return redirect(url_for('index') + '?oauth=success&provider=google')
    
    except Exception as e:
        current_app.logger.error(f'Google OAuth error: {e}')
        return redirect(url_for('index') + '?oauth=error')


# Microsoft OAuth routes
@microsoft_bp.route('/login')
def microsoft_login():
    """Initiate Microsoft OAuth login"""
    redirect_uri = url_for('microsoft_auth.microsoft_callback', _external=True)
    return oauth.microsoft.authorize_redirect(redirect_uri)


@microsoft_bp.route('/callback')
def microsoft_callback():
    """Handle Microsoft OAuth callback"""
    try:
        token = oauth.microsoft.authorize_access_token()
        user_info = token.get('userinfo')
        
        if not user_info:
            return jsonify({'error': 'Failed to get user info from Microsoft'}), 400
        
        session['oauth_user'] = {
            'provider': 'microsoft',
            'id': user_info.get('sub'),
            'email': user_info.get('email'),
            'name': user_info.get('name')
        }
        
        return redirect(url_for('index') + '?oauth=success&provider=microsoft')
    
    except Exception as e:
        current_app.logger.error(f'Microsoft OAuth error: {e}')
        return redirect(url_for('index') + '?oauth=error')


# Apple OAuth routes
@apple_bp.route('/login')
def apple_login():
    """Initiate Apple OAuth login"""
    redirect_uri = url_for('apple_auth.apple_callback', _external=True)
    return oauth.apple.authorize_redirect(redirect_uri)


@apple_bp.route('/callback')
def apple_callback():
    """Handle Apple OAuth callback"""
    try:
        token = oauth.apple.authorize_access_token()
        user_info = token.get('userinfo')
        
        if not user_info:
            return jsonify({'error': 'Failed to get user info from Apple'}), 400
        
        session['oauth_user'] = {
            'provider': 'apple',
            'id': user_info.get('sub'),
            'email': user_info.get('email'),
            'name': user_info.get('name', user_info.get('email', '').split('@')[0])
        }
        
        return redirect(url_for('index') + '?oauth=success&provider=apple')
    
    except Exception as e:
        current_app.logger.error(f'Apple OAuth error: {e}')
        return redirect(url_for('index') + '?oauth=error')
