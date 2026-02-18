from datetime import datetime, timedelta
from xmlrpc import client
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, 
    VectorParams,
    Filter,
    FieldCondition,
    MatchValue,
    PointIdsList
)
from typing import List, Optional
from loguru import logger

from config.settings import settings
from models.memory import Memory, MemoryQuery, MemorySearchResult, MemoryType

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
        point = {
            "id": str(memory.id),
            "vector": memory.embedding,
            "payload": {
                "content": memory.content,
                "timestamp": memory.timestamp.isoformat(),
                "memory_type": memory.memory_type.value,
                "importance_score": memory.importance_score,
                "user_id": memory.user_id,
                "tags": memory.tags,
                "last_accessed": memory.last_accessed.isoformat() if memory.last_accessed else None,
                "access_count": memory.access_count
            }
        }
        self.client.upsert(
            collection_name=self.collection_name,
            points=[point]
        )
        logger.info(f"Memory {memory.id} upserted successfully")
        return True 
        
        
    
    def search_memories(self, query: MemoryQuery, query_embedding: List[float]) -> List[MemorySearchResult]:
        """Search for similar memories."""
        filter_conditions = []
        
        if not query.allow_cross_user:
            filter_conditions.append(
                FieldCondition(
                    key="user_id", 
                    match=MatchValue(value=query.user_id))
            )
        if query.memory_types:
            filter_conditions.append(
                FieldCondition(
                    key="memory_type",
                    match=MatchValue(any=[mt.value for mt in query.memory_types])
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
            time_threshold = (datetime.now() - timedelta(days=query.time_window_days)).isoformat()
            filter_conditions.append(
                FieldCondition(
                    key="timestamp",
                    range={"gte": time_threshold}
                )
            )
        
        
        search_filter = Filter(must=filter_conditions) if filter_conditions else None
        
        search_results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            limit=query.top_k,
            query_filter=search_filter
        )
        
        memories = []
        for result in search_results.points:
            # Filter by minimum similarity threshold
            if result.score < query.min_similarity:
                continue
                
            payload = result.payload
            memory = MemorySearchResult(
                similarity_score=result.score,
                final_score=result.score,  # Placeholder; apply weighting as needed
                memory=Memory(
                    id=result.id,
                    content=payload["content"],
                    embedding=None,  # Embedding is not returned in search results
                    timestamp=datetime.fromisoformat(payload["timestamp"]),
                    memory_type=MemoryType(payload["memory_type"]),
                    importance_score=payload["importance_score"],
                    user_id=payload["user_id"],
                    tags=payload["tags"],
                    last_accessed=datetime.fromisoformat(payload["last_accessed"]) if payload["last_accessed"] else None,
                    access_count=payload["access_count"]    
                )
            )
            memories.append(memory)
        
        logger.info(f"Search returned {len(memories)} memories for query: {query.query_text}")
        return memories
       
        
    
    def delete_memory(self, memory_id: str) -> bool:
        """Delete a memory by ID."""
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=PointIdsList(
                points=[str(memory_id)]
            )
        )
        logger.info(f"Memory {memory_id} deleted successfully")
        return True
    
    def get_memory_by_id(self, memory_id: str) -> Optional[Memory]:
        """Retrieve a memory by its ID."""
        result = self.client.retrieve(
            collection_name=self.collection_name,
            ids=[str(memory_id)]
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
            last_accessed=datetime.fromisoformat(payload["last_accessed"]) if payload.get("last_accessed") else None,
            access_count=payload["access_count"]
        )
        logger.info(f"Memory {memory_id} retrieved successfully")
        return memory
    def update_memory_metadata(self, memory: Memory, new_metadata: dict) -> bool:
        """Update metadata fields of a memory."""
        existing_memory = self.get_memory_by_id(memory.id)
        if not existing_memory:
            logger.error(f"Memory {memory.id} not found for metadata update")
            return False
        
        # Convert datetime objects to ISO format strings
        processed_metadata = {}
        for key, value in new_metadata.items():
            if isinstance(value, datetime):
                processed_metadata[key] = value.isoformat()
            else:
                processed_metadata[key] = value
        
        self.client.set_payload(
            collection_name=self.collection_name,
            payload=processed_metadata,
            points=[str(memory.id)]
        )
        logger.info(f"Memory {memory.id} metadata updated successfully")
        return True
    
    def count_memories_for_user(self, user_id: str) -> int:
        """Count total number of memories for a user."""
        result = self.client.scroll(
            collection_name=self.collection_name,
            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key="user_id",
                        match=MatchValue(value=user_id)
                    )
                ]
            ),
            limit=10000,  # High limit to get all
            with_payload=False,
            with_vectors=False
        )
        count = len(result[0]) if result else 0
        logger.info(f"User {user_id} has {count} memories")
        return count