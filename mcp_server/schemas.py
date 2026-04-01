"""Shared schemas and serialization helpers for NeuroMem MCP tools."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from models.memory import Memory, MemoryDraft, MemorySearchResult


def serialize_datetime(value: Optional[datetime]) -> Optional[str]:
    if value is None:
        return None
    return value.isoformat()


def serialize_memory(memory: Memory) -> Dict[str, Any]:
    return {
        "id": memory.id,
        "content": memory.content,
        "timestamp": serialize_datetime(memory.timestamp),
        "memory_type": memory.memory_type.value,
        "importance_score": memory.importance_score,
        "user_id": memory.user_id,
        "tags": memory.tags,
        "last_accessed": serialize_datetime(memory.last_accessed),
        "access_count": memory.access_count,
    }


def serialize_search_result(result: MemorySearchResult) -> Dict[str, Any]:
    return {
        "memory": serialize_memory(result.memory),
        "similarity_score": result.similarity_score,
        "final_score": result.final_score,
    }


def serialize_draft(draft: MemoryDraft) -> Dict[str, Any]:
    return {
        "content": draft.content,
        "memory_type": draft.memory_type.value,
        "importance_score": draft.importance_score,
        "tags": draft.tags,
    }


def serialize_search_results(results: List[MemorySearchResult]) -> List[Dict[str, Any]]:
    return [serialize_search_result(result) for result in results]


def serialize_drafts(drafts: List[MemoryDraft]) -> List[Dict[str, Any]]:
    return [serialize_draft(draft) for draft in drafts]
