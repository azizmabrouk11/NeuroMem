from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, 
    VectorParams, 
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue
)
from typing import List, Optional
from loguru import logger

from config.settings import settings
from models.memory import Memory, MemoryQuery

class VectorStore:
    def __init__(self):
        """Initialize connection to Qdrant."""
        self.client = QdrantClient(
            host=settings.qdrant_host,
            port=settings.qdrant_port,
            api_key=settings.qdrant_api_key
        )
        self.collection_name = settings.qdrant_collection_name
        self._initialize_collection()
    
    def _initialize_collection(self):
        """Create collection if it doesn't exist."""
        collections = self.client.get_collections().collections
        collection_names = [c.name for c in collections]
        
        if self.collection_name not in collection_names:
            logger.info(f"Creating collection: {self.collection_name}")
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=settings.embedding_dimension,
                    distance=Distance.COSINE
                )
            )
            logger.info(f"Collection {self.collection_name} created successfully")
        else:
            logger.info(f"Collection {self.collection_name} already exists")
    
    def upsert_memory(self, memory: Memory) -> bool:
        """Store or update a memory in Qdrant."""
        
        
    
    def search_memories(self, query: MemoryQuery, query_embedding: List[float]) -> List[Memory]:
        """Search for similar memories."""
       
        
    
    def delete_memory(self, memory_id: str) -> bool:
        """Delete a memory by ID."""
        
        