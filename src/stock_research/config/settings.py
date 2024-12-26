from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings."""
    
    # API Keys
    OPENAI_API_KEY: str
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent.parent.parent
    KNOWLEDGE_DIR: Path = BASE_DIR / "src" / "stock_research" / "ai" / "knowledge"
    
    # Agent Settings
    DEFAULT_MODEL: str = "openai:gpt-4"
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 1000
    
    # Cache Settings
    CACHE_DIR: Path = BASE_DIR / ".cache"
    CACHE_TTL: int = 3600  # 1 hour
    
    # Streamlit Settings
    PAGE_TITLE: str = "Stock Market Research Assistant"
    PAGE_ICON: str = "📈"
    
    # Market Data Settings
    DEFAULT_TIMEFRAME: str = "1y"
    TECHNICAL_INDICATORS: list[str] = [
        "SMA_50",
        "SMA_200",
        "RSI",
        "MACD",
    ]
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

# Create settings instance
settings = Settings()