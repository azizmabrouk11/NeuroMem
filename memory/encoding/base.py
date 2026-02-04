from abc import ABC, abstractmethod
from typing import List

class BaseEmbedder(ABC):
    """Abstract base class for all embedding providers."""
    @abstractmethod
    def embed(self, text: str) -> List[float]:
        pass    

    @abstractmethod
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        pass
    
    @abstractmethod
    def get_dimension(self) -> int:
        """Return the embedding dimension."""
        pass