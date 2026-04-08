"""NeuroMem MCP server entrypoint."""

from __future__ import annotations

import sys
import socket
import time
from pathlib import Path
from urllib.parse import urlparse

from loguru import logger
from mcp.server.fastmcp import FastMCP
import uvicorn

try:
    from config.settings import settings
except ModuleNotFoundError:
    # `mcp dev path/to/server.py:mcp` imports this file directly.
    # Ensure the project root is on sys.path for absolute imports.
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    from config.settings import settings

try:
    from .tools import (
        chat as run_chat,
        delete_memory as run_delete_memory,
        extract_memories as run_extract_memories,
        get_context as run_get_context,
        retrieve_memories as run_retrieve_memories,
        store_memory as run_store_memory,
    )
except ImportError:
    from mcp_server.tools import (
        chat as run_chat,
        delete_memory as run_delete_memory,
        extract_memories as run_extract_memories,
        get_context as run_get_context,
        retrieve_memories as run_retrieve_memories,
        store_memory as run_store_memory,
    )


def build_server(debug: bool = False) -> FastMCP:
    if not settings.mcp_enabled:
        raise RuntimeError("MCP server is disabled in settings")

    return FastMCP(
        settings.mcp_server_name,
        debug=debug,
        log_level=settings.mcp_log_level,
    )


mcp = build_server()


def _wait_for_tcp_service(name: str, host: str, port: int, timeout_seconds: int = 30) -> None:
    deadline = time.time() + timeout_seconds
    last_error = None

    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=2):
                logger.info(f"Startup check passed: {name} reachable at {host}:{port}")
                return
        except OSError as exc:
            last_error = exc
            time.sleep(1)

    raise RuntimeError(
        f"Startup check failed: {name} not reachable at {host}:{port} within {timeout_seconds}s"
        f" (last error: {last_error})"
    )


def _parse_host_port_from_url(url: str, default_port: int) -> tuple[str, int]:
    parsed = urlparse(url)
    if parsed.scheme and parsed.hostname:
        if parsed.port:
            return parsed.hostname, parsed.port
        if parsed.scheme == "https":
            return parsed.hostname, 443
        return parsed.hostname, default_port

    cleaned = url.replace("http://", "").replace("https://", "")
    host_port = cleaned.split("/", 1)[0]
    if ":" in host_port:
        host, port_str = host_port.rsplit(":", 1)
        return host, int(port_str)
    return host_port, default_port


def run_startup_checks() -> None:
    llm_provider = settings.llm_provider.lower()
    embedding_provider = settings.embedding_provider.lower()

    valid_providers = {"ollama", "gemini"}
    if llm_provider not in valid_providers:
        raise RuntimeError(f"Invalid llm_provider: {settings.llm_provider}")
    if embedding_provider not in valid_providers:
        raise RuntimeError(f"Invalid embedding_provider: {settings.embedding_provider}")

    _wait_for_tcp_service("Qdrant", settings.qdrant_host, settings.qdrant_port)

    if llm_provider == "ollama" or embedding_provider == "ollama":
        ollama_host, ollama_port = _parse_host_port_from_url(settings.ollama_base_url, default_port=11434)
        _wait_for_tcp_service("Ollama", ollama_host, ollama_port)

    if llm_provider == "gemini" or embedding_provider == "gemini":
        if not settings.gemini_api_key.strip():
            raise RuntimeError(
                "Startup check failed: GEMINI_API_KEY is required when llm_provider or embedding_provider is 'gemini'"
            )


@mcp.tool(name="store_memory")
def store_memory_tool(
    user_id: str,
    content: str,
    memory_type: str = "episodic",
    importance_score: float | None = None,
    tags: list[str] | None = None,
):
    """Store a memory for a user."""
    return run_store_memory(
        user_id=user_id,
        content=content,
        memory_type=memory_type,
        importance_score=importance_score,
        tags=tags,
    )


@mcp.tool(name="retrieve_memories")
def retrieve_memories_tool(
    user_id: str,
    query: str,
    top_k: int = 5,
    min_similarity: float = 0.5,
    memory_types: list[str] | None = None,
    tags: list[str] | None = None,
):
    """Retrieve memories for a user."""
    return run_retrieve_memories(
        user_id=user_id,
        query=query,
        top_k=top_k,
        min_similarity=min_similarity,
        memory_types=memory_types,
        tags=tags,
    )


@mcp.tool(name="get_context")
def get_context_tool(
    user_id: str,
    query: str,
    max_memories: int = 10,
):
    """Build memory context for a query."""
    return run_get_context(user_id=user_id, query=query, max_memories=max_memories)


@mcp.tool(name="delete_memory")
def delete_memory_tool(
    user_id: str,
    memory_id: str,
):
    """Delete a stored memory."""
    return run_delete_memory(user_id=user_id, memory_id=memory_id)


@mcp.tool(name="chat")
def chat_tool(
    user_id: str,
    user_message: str,
    system_instruction: str | None = None,
    auto_extract: bool = True,
    max_context_memories: int = 10,
):
    """Run a memory-aware chat turn."""
    return run_chat(
        user_id=user_id,
        user_message=user_message,
        system_instruction=system_instruction,
        auto_extract=auto_extract,
        max_context_memories=max_context_memories,
    )


@mcp.tool(name="extract_memories")
def extract_memories_tool(
    user_message: str,
    assistant_message: str,
):
    """Extract memories from a conversation turn."""
    return run_extract_memories(user_message=user_message, assistant_message=assistant_message)


def main(
    debug: bool = False,
    transport: str = "stdio",
    host: str = "127.0.0.1",
    port: int = 8000,
) -> None:
    if settings.mcp_startup_checks:
        logger.info("MCP startup checks enabled")
        run_startup_checks()
    logger.info(f"Starting MCP server: {settings.mcp_server_name} v{settings.mcp_server_version}")
    if debug:
        logger.info("MCP debug mode enabled")
    server = mcp

    if transport in {"streamable-http", "http"}:
        uvicorn.run(server.streamable_http_app(), host=host, port=port)
        return

    server.run(transport="stdio")
