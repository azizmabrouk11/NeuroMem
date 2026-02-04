# src/embedding/gemini.py
"""
Google Gemini embedding utilities.
Uses text-embedding-004 (current recommended model as of 2025–2026).
"""

import os
from typing import List

import google.generativeai as genai
from google.api_core import retry

from memory.encoding.base import BaseEmbedder
from config.settings import settings

class GeminiEmbedder(BaseEmbedder):
    """
    Thread-safe, reusable Gemini text embedder.
    
    Example:
        embedder = GeminiEmbedder()
        vec = embedder.embed("Hello world")
    """
    
    MODEL_NAME = settings.embedding_model  
    
    def __init__(
        self,
        api_key: str | None = None,
        configure_once: bool = True,
    ):
        """
        Args:
            api_key: Gemini API key. If None, reads from GEMINI_API_KEY env var.
            configure_once: Whether to call genai.configure() only once (recommended).
        """
        self.api_key = api_key or settings.gemini_api_key  
        if not self.api_key:
            raise ValueError(
                "No Gemini API key provided. "
                "Set GEMINI_API_KEY environment variable "
                "or pass api_key=... when creating the embedder."
            )
        
        if configure_once:
            genai.configure(api_key=self.api_key)
            self._configured = True
        else:
            self._configured = False

    @retry.Retry(predicate=retry.if_transient_error, initial=2, maximum=30, multiplier=1.5)
    def embed(self, text: str) -> List[float]:
        """
        Embed a single text string.
        
        Returns:
            List of floats (768-dimensional vector for text-embedding-004)
        """
        if not self._configured:
            genai.configure(api_key=self.api_key)
        
        if not text.strip():
            raise ValueError("Cannot embed empty or whitespace-only text")
        
        response = genai.embed_content(
            model=self.MODEL_NAME,
            content=text,
            task_type="RETRIEVAL_QUERY",  # or RETRIEVAL_DOCUMENT depending on use-case
            title=None,                       # optional – can help quality
        )
        
        return response["embedding"]


    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Embed multiple texts sequentially."""
        return [self.embed(text) for text in texts]

    def get_dimension(self) -> int:
        """Return embedding dimension."""
        return settings.embedding_dimension
    