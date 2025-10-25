"""
Configuration file for Phisherman backend
Contains all environment variables and settings
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for Phisherman backend"""
    
    # MongoDB Configuration
    MONGO_URI = os.environ.get('MONGO_URI', "mongodb+srv://dsoc:dsoc@cluster0.dplte2b.mongodb.net/?appName=Cluster0")
    DATABASE_NAME = os.environ.get('DATABASE_NAME', 'phish')
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'im-phishing-it')
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Server Configuration
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 8080))
    
    # CORS Configuration
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000').split(',')
    
    # Session Configuration
    SESSION_COOKIE_SAMESITE = os.environ.get('SESSION_COOKIE_SAMESITE', 'Lax')
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    
    # Agent Configuration
    AGENT_PORTS = {
        'phish_master': 8001,
        'finance_phisher': 8002,
        'health_phisher': 8003,
        'personal_phisher': 8004,
        'phish_refiner': 8005
    }
    
    # Agentverse Configuration
    AGENTVERSE_ENABLED = os.environ.get('AGENTVERSE_ENABLED', 'True').lower() == 'true'
    AGENTVERSE_ENDPOINT = os.environ.get('AGENTVERSE_ENDPOINT', 'https://agentverse.ai')
    
    # Security Configuration
    BCRYPT_ROUNDS = int(os.environ.get('BCRYPT_ROUNDS', 12))
    
    @classmethod
    def get_mongo_uri(cls):
        """Get MongoDB URI"""
        return cls.MONGO_URI
    
    @classmethod
    def get_database_name(cls):
        """Get database name"""
        return cls.DATABASE_NAME
    
    @classmethod
    def get_agent_port(cls, agent_name):
        """Get port for specific agent"""
        return cls.AGENT_PORTS.get(agent_name, 8000)
    
    @classmethod
    def is_development(cls):
        """Check if running in development mode"""
        return cls.FLASK_ENV == 'development'
    
    @classmethod
    def is_production(cls):
        """Check if running in production mode"""
        return cls.FLASK_ENV == 'production'

# Create config instance
config = Config()
