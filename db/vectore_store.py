import datetime
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
        point = PointStruct(
            id=memory.id,
            vector=memory.embedding,
            payload={
                "content": memory.content,
                "timestamp": memory.timestamp.isoformat(),
                "memory_type": memory.memory_type.value,
                "importance_score": memory.importance_score,
                "user_id": memory.user_id,
                "tags": memory.tags,
                "last_accessed": memory.last_accessed.isoformat() if memory.last_accessed else None,
                "access_count": memory.access_count
            }
        )
        self.client.upsert(
            collection_name=self.collection_name,
            points=[point]
        )
        logger.info(f"Memory {memory.id} upserted successfully")
        return True 
        
        
    
    def search_memories(self, query: MemoryQuery, query_embedding: List[float]) -> List[Memory]:
        """Search for similar memories."""
        filter_conditions = []
        
        if query.memory_types:
            filter_conditions.append(
                FieldCondition(
                    key="memory_type",
                    match=MatchValue(any=query.memory_types)
                )
            )
        
        if query.tags:
            filter_conditions.append(
                FieldCondition(
                    key="tags",
                    match=MatchValue(any=query.tags)
                )
            )
        
        if query.time_window_days is not None:
            from datetime import datetime, timedelta
            time_threshold = (datetime.now() - timedelta(days=query.time_window_days)).isoformat()
            filter_conditions.append(
                FieldCondition(
                    key="timestamp",
                    range={"gte": time_threshold}
                )
            )
        
        
        search_filter = Filter(must=filter_conditions) if filter_conditions else None
        
        search_results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=query.top_k,
            filter=search_filter
        )
        
        memories = []
        for result in search_results:
            payload = result.payload
            memory = Memory(
                id=result.id,
                content=payload["content"],
                embedding=None,  # Embedding is not returned in search results
                timestamp=datetime.fromisoformat(payload["timestamp"]),
                memory_type=payload["memory_type"],
                importance_score=payload["importance_score"],
                user_id=payload["user_id"],
                tags=payload["tags"],
                last_accessed=payload["last_accessed"],
                access_count=payload["access_count"]
            )
            memories.append(memory)
        
        logger.info(f"Search returned {len(memories)} memories for query: {query.query_text}")
        return memories
       
        
    
    def delete_memory(self, memory_id: str) -> bool:
        """Delete a memory by ID."""
        self.client.delete(
            collection_name=self.collection_name,
            points=[memory_id]
        )
        logger.info(f"Memory {memory_id} deleted successfully")
        return True
    
    def get_memory_by_id(self, memory_id: str) -> Optional[Memory]:
        """Retrieve a memory by its ID."""
        result = self.client.retrieve(
            collection_name=self.collection_name,
            ids=[memory_id]
        )
        if not result or not result[0].payload:
            logger.warning(f"Memory {memory_id} not found")
            return None
        
        payload = result[0].payload
        memory = Memory(
            id=result[0].id,
            content=payload["content"],
            embedding=None,  # Embedding is not returned in retrieve results
            timestamp=datetime.fromisoformat(payload["timestamp"]),
            memory_type=payload["memory_type"],
            importance_score=payload["importance_score"],
            user_id=payload["user_id"],
            tags=payload["tags"],
            last_accessed=datetime.fromisoformat(payload["last_accessed"]),
            access_count=payload["access_count"]
        )
        logger.info(f"Memory {memory_id} retrieved successfully")
        return memory