from db.vectore_store import VectorStore
from memory.encoding.base import BaseEmbedder
from typing import List

from models.memory import Memory, MemoryQuery, MemorySearchResult
from datetime import datetime, timezone

class MemoryRetriever:

    """
    High-level interface for retrieving memories.
    Handles query embedding and vector DB search.
    """
    
    def __init__(self, embedder: BaseEmbedder, vector_store: VectorStore):
        self.embedder = embedder
        self.vector_store = vector_store

    def retrieve_memories(
        self,
        query:MemoryQuery,
    ) -> List[MemorySearchResult]:
        """
        Retrieve relevant memories based on the query.
        Args:
            query: MemoryQuery object with search parameters
        Returns:
            List of MemorySearchResult objects
        """
        search_embedding = self.embedder.embed_query(query.query_text)
        raw_memories = self.vector_store.search_memories(query, search_embedding)
        return raw_memories
    