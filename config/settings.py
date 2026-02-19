from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # gemini
    gemini_api_key: str = ""
    embedding_model: str = "models/gemini-embedding-001"
    llm_model: str = "gemini-2.5-flash"  
    
    # Qdrant
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_api_key: Optional[str] = None
    qdrant_collection_name: str = "ai_brain_memories"

    # Ollama
    llm_provider: str = "ollama"  # or "gemini"
    ollama_base_url: str = "http://localhost:11434/v1"
    ollama_model: str = "llama3.2"
    
    # Embedding provider
    embedding_provider: str = "ollama"  # "ollama" or "gemini"
    ollama_embedding_model: str = "embeddinggemma"
    
    # Memory settings
    max_working_memory: int = 10
    importance_threshold: float = 0.3
    similarity_threshold: float = 0.7
    decay_rate: float = 0.01  
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields like old EMBEDDING_DIMENSION
    
    @property
    def embedding_dimension(self) -> int:
        """Get embedding dimension based on provider and model."""
        if self.embedding_provider == "ollama":
            # Ollama model dimensions
            model_dims = {
                "nomic-embed-text": 768,
                "mxbai-embed-large": 1024,
                "all-minilm": 384,
            }
            return model_dims.get(self.ollama_embedding_model, 768)
        else:  # gemini
            return 3072

settings = Settings()