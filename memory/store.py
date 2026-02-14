

from datetime import datetime, timezone
from loguru import logger
from db.vectore_store import VectorStore
from memory.encoding.base import BaseEmbedder
from typing import List, Optional

from models.memory import Memory, MemoryQuery


class MemoryStore:
    """
    High-level interface for storing memories.
    Handles embedding generation and vector DB storage.
    """
    def __init__(self, embedder: BaseEmbedder, vector_store: VectorStore):
        self.embedder = embedder
        self.vector_store = vector_store
    
    def store_memory(
            self, 
            content: str, 
            deduplication_threshold: float = 0.85,
            **metadata,
            ) -> Memory:
        """
        Store a memory with automatic deduplication.
        
        If a very similar memory exists:
        - Don't create duplicate
        - Boost existing memory's importance and access count
        
        Args:
            content: Memory text
            user_id: User identifier
            memory_type: EPISODIC or SEMANTIC
            importance_score: 0.0-1.0
            tags: Optional tags
            deduplication_threshold: Similarity threshold for duplicates (default 0.85)
            
        Returns:
            Memory object (either newly created or existing boosted one)
        """
        try:
            
            embedding = self.embedder.embed(content)
            similar_memories = self._find_duplicates( 
                content=content,
                embedding=embedding,
                user_id=metadata.get("user_id"),
                memory_type=metadata.get("memory_type"),
                threshold=deduplication_threshold
                )
            if similar_memories:
                canonical = self._merge_duplicates(
                    duplicates=similar_memories,
                    new_content=content,
                    new_importance=metadata.get("importance_score"),
                    new_tags=metadata.get("tags")

                )
                return canonical
            memory = Memory(content=content, embedding=embedding, **metadata)
            self.vector_store.upsert_memory(memory)
            return memory
        except Exception as e:
            logger.error(f"Error storing memory: {e}")
            raise e
    
    def store_memory_batch(
        self,
        memories_data: List[dict]
    ) -> List[Memory]:
        """
        Store multiple memories efficiently (batch embedding).
        
        Args:
            memories_data: List of dicts with keys: content, user_id, memory_type, etc.
            
        Returns:
            List of stored Memory objects
        """
        contents = [data["content"] for data in memories_data]
        embeddings = self.embedder.embed_batch(contents)
        
        stored_memories = []
        for data, embedding in zip(memories_data, embeddings):
            memory = Memory(content=data["content"], embedding=embedding, **{k: v for k, v in data.items() if k != "content"})
            self.vector_store.upsert_memory(memory)
            stored_memories.append(memory)
        
        return stored_memories
    
    def update_memory(
        self,
        memory_id: str,
        content: str = None,
        importance_score: float = None,
        tags: List[str] = None
    ) -> bool:
        """
        Update an existing memory.
        If content changes, re-generate embedding.
        """
        existing_memory = self.vector_store.get_memory_by_id(memory_id)
        if not existing_memory:
            return False
        
        if content and content != existing_memory.content:
            existing_memory.content = content
            existing_memory.embedding = self.embedder.embed(content)
        
        if importance_score is not None:
            existing_memory.importance_score = importance_score
        
        if tags is not None:
            existing_memory.tags = tags
        
        self.vector_store.upsert_memory(existing_memory)
        return True
    
    def _find_duplicates(
        self,
        content: str,
        embedding: List[float],
        user_id: str,
        memory_type: str,
        threshold: float
    ) -> List[Memory]:
        """Find similar memories for deduplication."""
        try:
            query = MemoryQuery(
                query_text=content,
                user_id=user_id,
                memory_type=memory_type,
                top_k=5,
                min_similarity=threshold
            )
            results = self.vector_store.search_memories(query, query_embedding=embedding)
            if results:
                duplicates = [r.memory for r in results]
                logger.debug(
                    f"Found {len(duplicates)} similar memories "
                    f"(threshold={threshold})"
                )
                return duplicates
            return []
        except Exception as e:
            logger.error(f"Error finding duplicates: {e}")
            raise e
        
    def _merge_duplicates(
            self,
            duplicates: List[Memory],
            new_content: str,
            new_importance: float,
            new_tags: Optional[List[str]]
    ):
        
        """
        Merge multiple duplicate memories into one canonical memory.
        
        Strategy:
        - Pick memory with highest importance as canonical
        - Merge access counts and tags from all
        - Delete the others
        - Boost importance
        """
        canonical = max(
        duplicates,
        key=lambda m: (m.importance_score, len(m.content))
        )
        logger.info(
        f"Merging {len(duplicates)} memories into canonical: {canonical.id[:8]}"
        )
        total_access_count = sum(m.access_count for m in duplicates)
        all_tags = set(canonical.tags)
        for memory in duplicates:
            if memory.id != canonical.id:
                all_tags.update(memory.tags)
                
                self.vector_store.delete_memory(memory.id)
                logger.debug(f"Deleted duplicate: {memory.id[:8]}")
        canonical.access_count = total_access_count + 1
        canonical.tags = list(all_tags)
        canonical.last_accessed = datetime.now(timezone.utc)
        boost = 0.05 * len(duplicates)  
        canonical.importance_score = min(
            canonical.importance_score + boost,
            1.0
        )
        self.vector_store.upsert_memory(canonical)
        logger.info(f"Merged {len(duplicates)} duplicates into canonical memory {canonical.id[:8]}")
        return canonical