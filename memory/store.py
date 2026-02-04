


from db.vectore_store import VectorStore
from memory.encoding.base import BaseEmbedder
from types import List

from models.memory import Memory


class MemoryStore:
    """
    High-level interface for storing memories.
    Handles embedding generation and vector DB storage.
    """
    def __init__(self, embedder: BaseEmbedder, vector_store: VectorStore):
        self.embedder = embedder
        self.vector_store = vector_store
    
    def store_memory(self, content: str, **metadata) -> Memory:
        """Embed and store a memory with associated metadata."""
        embedding = self.embedder.embed(content)
        memory = Memory(content=content, embedding=embedding, **metadata)
        self.vector_store.upsert_memory(memory)
        return memory
    
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
