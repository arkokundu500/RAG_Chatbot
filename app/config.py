import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    EMBEDDING_MODEL = "models/embedding-001"  # Experimental embedding model
    LLM_MODEL = "gemini-2.0-flash"
    CHROMA_PATH = "chroma_db"
    USER_DB = {
        "finance": {"password": "fin123", "role": "finance"},
        "marketing": {"password": "mkt123", "role": "marketing"},
        "hr": {"password": "hr123", "role": "hr"},
        "engineering": {"password": "eng123", "role": "engineering"},
        "ceo": {"password": "ceo123", "role": "c-level"},
        "employee": {"password": "emp123", "role": "employee"}
    }
    ROLE_ACCESS = {
        "finance": ["finance"],
        "marketing": ["marketing"],
        "hr": ["hr"],
        "engineering": ["engineering"],
        "c-level": ["engineering", "finance", "marketing", "hr", "general"],
        "employee": ["general"]
    }