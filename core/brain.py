"""
Brain - Main orchestrator for the AI memory system.
Provides high-level interface for storing, retrieving, and managing memories.
"""

from typing import List, Optional
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