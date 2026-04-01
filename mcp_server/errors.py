"""MCP error helpers for NeuroMem."""

from __future__ import annotations


class MCPServerError(Exception):
    """Base error for MCP server failures."""


class InvalidToolInput(MCPServerError):
    """Raised when a tool request fails validation."""


class ServiceUnavailable(MCPServerError):
    """Raised when a backing service is unavailable."""
