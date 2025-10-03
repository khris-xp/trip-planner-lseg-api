import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Configuration settings for the application"""
    
    # Gemini API Configuration
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    
    # Application Configuration
    APP_NAME: str = "Trip Planner API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Rate Limiting
    REQUESTS_PER_MINUTE: int = int(os.getenv("REQUESTS_PER_MINUTE", "60"))
    
    @classmethod
    def validate_gemini_api_key(cls) -> bool:
        """Validate if Gemini API key is configured"""
        return cls.GEMINI_API_KEY is not None and len(cls.GEMINI_API_KEY.strip()) > 0

settings = Settings()