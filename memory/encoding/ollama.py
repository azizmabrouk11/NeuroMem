"""
Ollama embedding utilities.
Self-hosted embeddings using Ollama.
"""

import requests
from typing import List
from memory.encoding.base import BaseEmbedder
from config.settings import settings


class OllamaEmbedder(BaseEmbedder):
    """
    Self-hosted Ollama embedder.
    
    Popular models:
    - nomic-embed-text (768 dims) - recommended
    - mxbai-embed-large (1024 dims)
    - all-minilm (384 dims)
    
    Example:
        embedder = OllamaEmbedder()
        vec = embedder.embed("Hello world")
    """
    
    def __init__(
        self,
        base_url: str | None = None,
        model: str | None = None,
    ):
        """
        Args:
            base_url: Ollama API base URL (default from settings)
            model: Embedding model name (default from settings)
        """
        self.base_url = (base_url or settings.ollama_base_url).rstrip("/v1").rstrip("/")
        self.model =  settings.ollama_embedding_model
        self._dimension = None
    
    def embed(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        response = requests.post(
            f"{self.base_url}/api/embeddings",
            json={
                "model": self.model,
                "prompt": text
            },
            timeout=30
        )
        response.raise_for_status()
        embedding = response.json()["embedding"]
        
        if self._dimension is None:
            self._dimension = len(embedding)
        
        return embedding
    
    def embed_query(self, text: str) -> List[float]:
        """Generate embedding for a query (same as embed for Ollama)."""
        return self.embed(text)
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        return [self.embed(text) for text in texts]
    
    def get_dimension(self) -> int:
        """Return the embedding dimension."""
        if self._dimension is None:
            # Get dimension by embedding a test string
            self.embed("test")
        return self._dimension
