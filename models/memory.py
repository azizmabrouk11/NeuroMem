from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import uuid4

class MemoryType(str, Enum):
    EPISODIC = "episodic"    # conversations, events
    SEMANTIC = "semantic"     # facts, preferences
    
class Memory(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    content: str
    embedding: Optional[List[float]] = None
    timestamp: datetime = Field(default_factory=datetime.now(timezone.utc))
    memory_type: MemoryType
    importance_score: float = Field(default=0.5, ge=0.0, le=1.0)
    user_id: str
    tags: List[str] = Field(default_factory=list)
class MemoryQuery(BaseModel):
    """Query structure for retrieving memories."""
    query_text: str
    user_id: str
    memory_types: Optional[list[MemoryType]] = None
    top_k: int = Field(default=5, ge=1, le=50)
    min_similarity: float = Field(default=0.7, ge=0.0, le=1.0)
    time_window_days: Optional[int] = None  # Only memories from last N days
    tags: Optional[list[str]] = None

class MemorySearchResult(BaseModel):
    """Result from memory search with scoring."""
    memory: Memory
    similarity_score: float  # Raw cosine similarity from Qdrant
    final_score: float  # After applying importance + recency weighting