from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import uuid4

class MemoryType(str, Enum):
    EPISODIC = "episodic"   
    SEMANTIC = "semantic"     
    
class Memory(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    content: str
    embedding: Optional[List[float]] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    memory_type: MemoryType
    importance_score: float = Field(default=0.5, ge=0.0, le=1.0)
    user_id: str
    tags: List[str] = Field(default_factory=list)
    last_accessed : Optional[datetime] = None
    access_count: int = 0


class MemoryQuery(BaseModel):
    """Query structure for retrieving memories."""
    query_text: str
    user_id: str
    memory_types: Optional[List[MemoryType]] = None
    top_k: int = Field(default=5, ge=1, le=50)
    min_similarity: float = Field(default=0.7, ge=0.0, le=1.0)
    time_window_days: Optional[int] = None  # Only memories from last N days
    tags: Optional[List[str]] = None
    allow_cross_user: bool = False  


class MemorySearchResult(BaseModel):
    """Result from memory search with scoring."""
    memory: Memory
    similarity_score: float  # Raw cosine similarity from Qdrant
    final_score: float  # After applying importance + recency weighting

class MemoryDraft(BaseModel):
    """
    Draft memory before being stored.
    Missing user_id and embedding (added during storage).
    """
    content: str
    memory_type: MemoryType
    importance_score: float = Field(ge=0.0, le=1.0)
    tags: List[str] = Field(default_factory=list)
    
    def to_memory(self, user_id: str) -> Memory:
        """Convert draft to full Memory object."""
        from datetime import datetime, timezone
        from uuid import uuid4
        
        return Memory(
            id=str(uuid4()),
            content=self.content,
            embedding=None,
            timestamp=datetime.now(timezone.utc),
            memory_type=self.memory_type,
            importance_score=self.importance_score,
            user_id=user_id,
            tags=self.tags,
            access_count=0,
            last_accessed=None
        )