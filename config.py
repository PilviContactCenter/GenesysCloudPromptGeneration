"""
Application configuration for Prompt Studio.
Centralized configuration loaded from environment variables.
"""
import os
import secrets
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration."""
    
    # Flask Core
    SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_hex(32))
    
    # File Uploads
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    ALLOWED_EXTENSIONS = {'.wav'}
    
    # Session cookie settings
    # In development (HTTP): SameSite=Lax, Secure=False
    # In production (HTTPS): SameSite=None, Secure=True (for iframe support)
    _is_production = os.getenv('FLASK_ENV') == 'production'
    SESSION_COOKIE_SAMESITE = 'None' if _is_production else 'Lax'
    SESSION_COOKIE_SECURE = _is_production  # True only for HTTPS
    
    # Azure TTS Credentials
    AZURE_SPEECH_KEY = os.getenv('AZURE_SPEECH_KEY')
    AZURE_SPEECH_REGION = os.getenv('AZURE_SPEECH_REGION')
    
    # Genesys Cloud API Credentials (Client Credentials - for prompt exports)
    GENESYS_CLIENT_ID = os.getenv('GENESYS_CLIENT_ID')
    GENESYS_CLIENT_SECRET = os.getenv('GENESYS_CLIENT_SECRET')
    GENESYS_REGION = os.getenv('GENESYS_REGION', 'mypurecloud.de')
    
    # Genesys Cloud OAuth (Authorization Code - for user login)
    OAUTH_CLIENT_ID = os.getenv('OAUTH_CLIENT_ID')
    OAUTH_CLIENT_SECRET = os.getenv('OAUTH_CLIENT_SECRET')
    OAUTH_REDIRECT_URI = os.getenv('OAUTH_REDIRECT_URI', 'http://localhost:5001/oauth/callback')
    GENESYS_BASE_URL = os.getenv('GENESYS_BASE_URL', 'mypurecloud.de')
