"""MCP tool handlers for NeuroMem."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.brain import Brain
from ai.chat import ChatManager
from memory.extractor import MemoryExtractor
from models.memory import Memory, MemoryDraft, MemorySearchResult, MemoryType

from .schemas import serialize_drafts, serialize_memory, serialize_search_results


def _build_brain(user_id: str) -> Brain:
    return Brain(user_id=user_id)


def store_memory(
    *,
    user_id: str,
    content: str,
    memory_type: str = "episodic",
    importance_score: Optional[float] = None,
    tags: Optional[List[str]] = None,
) -> Dict[str, Any]:
    brain = _build_brain(user_id)
    resolved_type = MemoryType.SEMANTIC if memory_type == "semantic" else MemoryType.EPISODIC
    memory = brain.remember(
        content=content,
        memory_type=resolved_type,
        importance_score=importance_score,
        tags=tags,
    )
    return serialize_memory(memory)


def retrieve_memories(
    *,
    user_id: str,
    query: str,
    top_k: int = 5,
    min_similarity: float = 0.5,
    memory_types: Optional[List[str]] = None,
    tags: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    brain = _build_brain(user_id)
    resolved_types = None
    if memory_types:
        resolved_types = [
            MemoryType.SEMANTIC if memory_type == "semantic" else MemoryType.EPISODIC
            for memory_type in memory_types
        ]
    results = brain.recall(
        query=query,
        memory_types=resolved_types,
        top_k=top_k,
        min_similarity=min_similarity,
        tags=tags,
    )
    return serialize_search_results(results)


def get_context(
    *,
    user_id: str,
    query: str,
    max_memories: int = 10,
) -> Dict[str, Any]:
    brain = _build_brain(user_id)
    return {"context": brain.get_context(query=query, max_memories=max_memories)}


def delete_memory(*, user_id: str, memory_id: str) -> Dict[str, Any]:
    brain = _build_brain(user_id)
    return {"success": brain.forget(memory_id)}


def chat(
    *,
    user_id: str,
    user_message: str,
    system_instruction: Optional[str] = None,
    auto_extract: bool = True,
    max_context_memories: int = 10,
) -> Dict[str, Any]:
    chat_manager = ChatManager(user_id=user_id, system_instruction=system_instruction)
    response = chat_manager.chat(
        user_message=user_message,
        auto_extract=auto_extract,
        max_context_memories=max_context_memories,
    )
    return {"response": response}


def extract_memories(
    *,
    user_message: str,
    assistant_message: str,
) -> List[Dict[str, Any]]:
    extractor = MemoryExtractor()
    drafts = extractor.extract_memories(user_message, assistant_message)
    return serialize_drafts(drafts)
