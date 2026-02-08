"""
Brain - Main orchestrator for the AI memory system.
Provides high-level interface for storing, retrieving, and managing memories.
"""

from datetime import datetime
from typing import List, Optional
from bson import utc
from loguru import logger

from models.memory import Memory, MemoryType, MemoryQuery, MemorySearchResult
from memory.store import MemoryStore
from memory.retrieve import MemoryRetriever
from memory.encoding.gemini import GeminiEmbedder
from db.vectore_store import VectorStore
from config.settings import settings
class Brain:
    """
    Main controller for the AI memory system.
    
    Usage:
        brain = Brain(user_id="aziz")
        brain.remember("I love spicy food")
        results = brain.recall("What food do I like?")
    """
    def __init__(self, user_id):
        """
        Initialize the brain for a specific user.
        
        Args:
            user_id: Unique identifier for the user
        """
        self.user_id = user_id


        self.embedder = GeminiEmbedder()
        self.vector_store = VectorStore()
        self.memory_store = MemoryStore()
        self.memory_retriever = MemoryRetriever(self.embedder, self.vector_store)

        logger.info(f"Brain initialized for user: {user_id}")

    def remember(
            self,
            content: str, 
            memory_type: MemoryType = MemoryType.EPISODIC, 
            importance_score: Optional[float] = None
            ) -> Memory:
        """
        Store a new memory.
        
        Args:
            content: The memory text
            memory_type: EPISODIC or SEMANTIC
            importance_score: 0.0 to 1.0 (auto-calculated if None)
            tags: Optional tags for organization
            
        Returns:
            The stored Memory object
            
        Example:

        
            memory = brain.remember(
                "User prefers spicy Indian food",
                memory_type=MemoryType.SEMANTIC,
                importance_score=0.8,
                tags=["food", "preference"]
            )
        """
        try:
            if importance_score is None:
                importance_score = self._calculate_importance(content, memory_type)
            memory = self.memory_store.store_memory(
                content = content,
                user_id = self.user_id,
                memory_type = memory_type,
                importance_score = importance_score,
                tags = []
            )
            logger.info(f"Stored memory {memory.id[:8]} for user {self.user_id}")
            return memory
        

        except Exception as e:
            logger.error(f"Failed to store memory: {e}")
            raise

    def recall(
            
            self,
            query: str,
            memory_types: Optional[List[MemoryType]] = None,
            top_k: int = 5,
            min_similarity: float = 0.5,
            tags: Optional[List[str]] = None

            )-> List[MemorySearchResult]:
            
        """
        Retrieve relevant memories based on a query.
            
        Args:
            query: Search query text
            memory_types: Filter by memory types (None = all types)
            top_k: Maximum number of results
            min_similarity: Minimum similarity threshold (0.0-1.0)
            tags: Filter by tags
                
        Returns:
            List of MemorySearchResult sorted by relevance
                
        Example:
            results = brain.recall(
                "What food does the user like?",
                memory_types=[MemoryType.SEMANTIC],
                top_k=3
            )
        """
        try: 
            memory_query = MemoryQuery(
                query_text=query,
                user_id=self.user_id,
                memory_types=memory_types,
                top_k=top_k,
                min_similarity=min_similarity,
                tags=tags
            )
            results = self.memory_retriever.retrieve_memories(memory_query)
            self._update_access_stats(results)
            logger.info(f"Retrieved {len(results)} memories for query: '{query}'")
            return results
        except Exception as e:
            logger.error(f"Failed to retrieve memories: {e}")
            raise

    def forget(self, memory_id: str) -> bool:
        """
        Delete a specific memory.
        
        Args:
            memory_id: ID of the memory to delete
            
        Returns:
            True if successful, False otherwise
            
        Example:
            brain.forget("mem_abc123")
        """
        try:
            success = self.vector_store.delete_memory(memory_id)
            
            if success:
                logger.info(f"Deleted memory {memory_id}")
            else:
                logger.warning(f"Failed to delete memory {memory_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"Failed to delete memory: {e}")
            raise
    def get_context(self, query:str, max_memories: int = 10) -> str:
        """
        Build context string from relevant memories for LLM.
        
        Args:
            query: Query to find relevant memories
            max_memories: Maximum number of memories to include
            
        Returns:
            Formatted context string
            
        Example:
            context = brain.get_context("What are my preferences?")
            # Use this context with your LLM
        """
        try:
            results = self.recall(query = query, top_k = max_memories)
            if not results:
                return "no relevent memories found."
            context_parts = ["relevant memories about the user:\n"]
            for i, result in enumerate(results, 1):
                memory = result.memory
                context_parts.append(
                    f"{i}. {memory.content} "
                    f"(type: {memory.memory_type.value}, "
                    f"importance: {memory.importance_score:.2f}, "
                    f"relevance: {result.final_score:.2f})"
                )
            context = "\n".join(context_parts)
            logger.debug(f"Built context with {len(results)} memories for query: '{query}'")
            return context
        except Exception as e:
            logger.error(f"Failed to build context: {e}")
            raise
    def _calculate_importance(
        self,
        content: str,
        memory_type: MemoryType
    ) -> float:
        """
        Auto-estimate importance score based on content and type.
        
        Simple heuristic:
        - Semantic memories: default 0.7
        - Episodic memories: default 0.5
        - Longer content: slightly higher score
        """
        base_score = 0.7 if memory_type == MemoryType.SEMANTIC else 0.5
        
        # Boost for longer, more detailed content
        length_boost = min(len(content) / 200, 0.2)  # Up to +0.2
        
        final_score = min(base_score + length_boost, 1.0)
        return final_score
    
    def _update_access_stats(self, results: List[MemorySearchResult]):
        """
        Update access_count and last_accessed for retrieved memories.
        
        Note: This is a simplified version. In production, you'd want to
        batch update these in the database.
        """
        for result in results:
            memory = result.memory
            count =memory.access_count + 1
            last_accessed = datetime.now(tz=utc)
            return self.vector_store.update_memory_metadata(memory, {
                "access_count": count,
                "last_accessed": last_accessed
            })