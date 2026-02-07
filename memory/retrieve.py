from db.vectore_store import VectorStore
from intelligence.ranker import MemoryRanker
from memory.encoding.base import BaseEmbedder
from typing import List

from models.memory import Memory, MemoryQuery, MemorySearchResult
from loguru import logger
class MemoryRetriever:

    """
    High-level interface for retrieving memories.
    Handles query embedding and vector DB search.
    """
    
    def __init__(self, embedder: BaseEmbedder, vector_store: VectorStore):
        self.embedder = embedder
        self.vector_store = vector_store
        self.ranker = MemoryRanker()
        logger.info("MemoryRetriever initialized")

    def retrieve_memories(
        self,
        query:MemoryQuery,
    ) -> List[MemorySearchResult]:
        """
        Retrieve relevant memories based on the query.
        Args:
            query: MemoryQuery object with search parameters
        Returns:
            List of MemorySearchResult objects sorted by final_score
        """
        try:
            logger.info(f"Retrieving memories for query: '{query.query_text}' with top_k={query.top_k}")
            search_embedding = self.embedder.embed_query(query.query_text)
            raw_memories = self.vector_store.search_memories(query, search_embedding)
            logger.info(f"Vector search returned {len(raw_memories)} memories")
            ranked_memories = self.ranker.rank_memories(raw_memories)
            logger.info(f"Returned {len(ranked_memories)} ranked memories for query: '{query.query_text}'")
            return ranked_memories
        except Exception as e:
            logger.error(f"Error retrieving memories: {e}")
            return []