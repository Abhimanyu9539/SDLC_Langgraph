import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-nano")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.3"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "5000"))
    
    # Workflow settings
    MAX_ITERATIONS = int(os.getenv("MAX_ITERATIONS", "3"))
    MAX_USER_STORIES = int(os.getenv("MAX_USER_STORIES", "3"))
    ENABLE_LOGGING = os.getenv("ENABLE_LOGGING", "true").lower() == "true"

settings = Settings()