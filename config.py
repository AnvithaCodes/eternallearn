"""Configuration for EternaLearn"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Central configuration"""
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    MODEL_NAME = "models/gemini-2.5-flash"
    TEMPERATURE = 0.7
    MAX_TOKENS = 2048
    ENABLE_SEARCH = True
    ENABLE_VISUAL_LEARNING = True #changes
    MEMORY_BANK_PATH = "./data/memory_bank.json"
    SESSION_TIMEOUT_MINUTES = 30
    LOG_LEVEL = "INFO"
    LOG_FILE = "eternallearn.log"
    
    @classmethod
    def validate(cls):
        if not cls.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY not found in .env file")
        return True

Config.validate()