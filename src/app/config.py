import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    # LLM Model IDs
    GEMINI_DEFAULT_MODEL: str = "gemini-2.5-flash"
    GEMINI_PRO_MODEL: str = "gemini-2.5-pro"
    GEMINI_LITE_MODEL: str = "gemini-2.5-flash-lite"
    GEMINI_EMBEDDING_MODEL: str = "gemini-embedding-001"

    # RAG Settings
    RAG_RELEVANCE_THRESHOLD: float = 0.75
    RAG_TOP_K: int = 5

    # Project paths
    ROOT_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DATA_DIR: str = os.path.join(ROOT_DIR, "src", "data", "seed")
    INDEX_DIR: str = os.path.join(ROOT_DIR, "src", "rag", "index")

    class Config:
        case_sensitive = True

settings = Settings()
