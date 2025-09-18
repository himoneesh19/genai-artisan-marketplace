import os
import json
import base64
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    DATABASE_URI = 'sqlite:///artisans.db'
    GOOGLE_CLOUD_PROJECT = os.environ.get('GOOGLE_CLOUD_PROJECT') or 'my-project-genai-471504'

    # Support for service account credentials in .env
    GOOGLE_SERVICE_ACCOUNT_JSON = os.environ.get('GOOGLE_SERVICE_ACCOUNT_JSON')
    GOOGLE_SERVICE_ACCOUNT_KEY_B64 = os.environ.get('GOOGLE_SERVICE_ACCOUNT_KEY_B64')

    # Fallback to file-based credentials (removed to avoid missing file error)
    GOOGLE_APPLICATION_CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')

    VERTEX_AI_API_KEY = os.environ.get('VERTEX_AI_API_KEY') or os.environ.get('API_KEY') or os.environ.get('@GENAI')
    VERTEX_AI_LOCATION = 'asia-south1'  # Default location, can be changed

    @classmethod
    def get_service_account_credentials(cls):
        """Get service account credentials from .env or file"""
        if cls.GOOGLE_SERVICE_ACCOUNT_JSON:
            # Credentials stored as JSON string
            return json.loads(cls.GOOGLE_SERVICE_ACCOUNT_JSON)
        elif cls.GOOGLE_SERVICE_ACCOUNT_KEY_B64:
            # Credentials stored as base64 encoded JSON
            json_str = base64.b64decode(cls.GOOGLE_SERVICE_ACCOUNT_KEY_B64).decode('utf-8')
            return json.loads(json_str)
        else:
            # Fallback to file-based credentials
            return None

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
