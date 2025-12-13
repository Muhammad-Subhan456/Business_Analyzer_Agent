"""
Configuration settings for the Business Analyst AI Agent
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set Ollama host for CrewAI/litellm
os.environ["OLLAMA_HOST"] = "http://127.0.0.1:11434"


class Config:
    """Application configuration."""
    
    # API Keys
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    SERPER_API_KEY = os.getenv("SERPER_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    
    # Ollama Settings
    OLLAMA_BASE_URL = "http://127.0.0.1:11434"
    
    # LLM Settings (using local Ollama)
    LLM_MODEL = "ollama/llama3.2"
    LLM_TEMPERATURE_TOOL = 0.1  # Low for tool agents
    LLM_TEMPERATURE_REASONING = 0.5  # Medium for reasoning
    LLM_TEMPERATURE_CREATIVE = 0.7  # Higher for report writing
    
    # Analysis Settings
    DEFAULT_PERIOD = "1y"
    MAX_COMPETITORS = 7
    MAX_NEWS_ITEMS = 10
    
    # Report Settings
    REPORT_MIN_WORDS = 800
    REPORT_MAX_WORDS = 1200
    
    # Crew Settings
    VERBOSE_MODE = True
    MAX_ITERATIONS = 10
    
    @classmethod
    def validate(cls):
        """Validate required configuration."""
        errors = []
        
        # GOOGLE_API_KEY no longer required - using local Ollama
        
        if not cls.SERPER_API_KEY:
            errors.append("SERPER_API_KEY is not set (needed for web search)")
        
        return len(errors) == 0, errors


# Validate on import
def check_config():
    """Check and display configuration status."""
    is_valid, errors = Config.validate()
    
    if not is_valid:
        print("⚠️  Configuration Issues:")
        for error in errors:
            print(f"   - {error}")
        print("\nPlease set the required environment variables.")
    else:
        print("✅ Configuration validated successfully")
    
    return is_valid

