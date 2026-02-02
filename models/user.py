from pydantic import BaseModel, EmailStr ,Field
from typing import Optional, Dict
from uuid import uuid4
from datetime import datetime, timezone




class UserProfile(BaseModel):
    '''User profile built from accumulated memories.'''
    interests: list[str] = Field(default_factory=list)
    communication_style: Optional[str] = None  
    expertise_areas: list[str] = Field(default_factory=list)
    common_topics: Dict[str, int] = Field(default_factory=dict)  # topic -> frequency

class UserPreferences(BaseModel):
    '''User preferences for interactions and content.'''
    max_memories_in_context: int = Field(default=10, ge=1, le=50)
    importance_threshold: float = Field(default=0.3, ge=0.0, le=1.0)
    enable_auto_summarization: bool = True
    preferred_memory_types: list[str] = Field(default_factory=lambda: ["semantic", "episodic"])

class User(BaseModel):
    '''A model representing a user in the system.'''
    id: int
    username: str = Field(default_factory=lambda: str(uuid4()))
    email: EmailStr
    name: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_active: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    profile: UserProfile = Field(default_factory=UserProfile)
    preferences: UserPreferences = Field(default_factory=UserPreferences)