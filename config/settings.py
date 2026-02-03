from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # gemini
    gemini_api_key: str
    embedding_model: str = "models/text-embedding-004"
    embedding_dimension: int = 768
    llm_model: str = "gemini-1.5-flash"  
    
    # Qdrant
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_api_key: Optional[str] = None
    qdrant_collection_name: str = "ai_brain_memories"
    
    # Memory settings
    max_working_memory: int = 10
    importance_threshold: float = 0.3
    similarity_threshold: float = 0.7
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()