import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"  # Ignore extra fields to prevent errors
    )
    
    # Bot Settings
    TELEGRAM_BOT_TOKEN: str = Field(default=..., description="Telegram Bot Token from @BotFather")
    
    # Google AI Settings  
    # For backward compatibility, still support API key
    GEMINI_API_KEY: str = Field(default="", description="Gemini API Key for authentication")
    
    # New: Service account credentials path
    GOOGLE_CREDENTIALS_PATH: str = Field(
        default=str(Path(__file__).parent.parent.parent / ".secrets" / "google-credentials.json"),
        description="Path to Google service account credentials JSON file"
    )
    
    # Google Cloud Project settings (required for Vertex AI)
    GOOGLE_CLOUD_PROJECT: str = Field(default="", description="Google Cloud Project ID for Vertex AI")
    GOOGLE_CLOUD_LOCATION: str = Field(default="us-central1", description="Google Cloud location for Vertex AI")

    # LLM Model IDs
    GEMINI_DEFAULT_MODEL: str = Field(default="gemini-2.5-flash", description="Default Gemini model")
    GEMINI_PRO_MODEL: str = Field(default="gemini-2.5-pro", description="Pro Gemini model")
    GEMINI_LITE_MODEL: str = Field(default="gemini-2.5-flash-lite", description="Lite Gemini model")
    GEMINI_EMBEDDING_MODEL: str = Field(default="gemini-embedding-001", description="Gemini embedding model")

    # RAG Settings
    RAG_RELEVANCE_THRESHOLD: float = Field(default=0.3, description="Relevance threshold for RAG retrieval")
    RAG_TOP_K: int = Field(default=5, description="Number of top results to retrieve for RAG")

    # Project paths
    ROOT_DIR: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent.resolve())
    DATA_DIR: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent / "data")
    INDEX_DIR: Path = Field(default_factory=lambda: Path(__file__).parent.parent / "rag" / "index")

    # Database settings
    DATABASE_URL: str = Field(
        default="sqlite+aiosqlite:///./admissions.db", 
        description="Database connection URL"
    )
    DB_ECHO: bool = Field(default=False, description="Enable database query logging")
    
    # API settings
    DEBUG: bool = Field(default=False, description="Enable debug mode")
    ALLOWED_ORIGINS: list[str] = Field(default=["*"], description="Allowed origins for CORS")
    ALLOW_ORIGIN_REGEX: Optional[str] = Field(default=None, description="Regex for allowed origins")


settings = Settings()