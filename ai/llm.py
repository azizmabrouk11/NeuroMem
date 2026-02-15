"""
LLM client for generating responses.
Uses Google Gemini API.
"""

from typing import List, Optional

from loguru import logger
from openai import OpenAI

from config.settings import settings

class LLMClient:
    """
    Initialize Gemini client.
        
    Args:
        model_name: Gemini model to use (default from settings)
    """
    def __init__(self, model_name: Optional[str] = None):
        """Initialize Ollama (OpenAI-compatible)."""
        
        self.client = OpenAI(
            base_url=settings.ollama_base_url,
            api_key="ollama"  # Dummy key
        )
        self.model_name = settings.ollama_model
        self.client_type = "openai"
    def generate_response(
        self,
        prompt: str,
        context: Optional[str] = None,
        system_instruction: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """Generate a response from Ollama."""
        try: 
            full_prompt = self._build_prompt(prompt, context, system_instruction)
            logger.debug(f"Sending prompt to LLM (length: {len(full_prompt)} chars)")
            
            messages = []
            if system_instruction:
                messages.append({"role": "system", "content": system_instruction})
            messages.append({"role": "user", "content": full_prompt})
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            result = response.choices[0].message.content
            logger.debug(f"LLM response: {result[:100]}...")
            return result
        except Exception as e:
            logger.error(f"Error generating LLM response: {e}")
            return "Sorry, I couldn't generate a response at this time."
        

    def _build_prompt(
            self, 
            user_input: str,
            context: Optional[str] = None,
            system_instruction: Optional[str] = None
    )->str:
        """
        Build the full prompt for the LLM, combining system instructions, context, and user input.
        Args:
            user_input: The user's message
            context: Memory context to include
            system_instruction: System-level instructions
        Returns:
            The combined prompt string
        """
        prompt_parts = []
        if system_instruction:
            prompt_parts.append(f"System Instruction:\n{system_instruction}\n\n")
        if context:
            prompt_parts.append(f"Context:\n{context}\n\n")
        prompt_parts.append(f"User Input:\n{user_input}")
        return "\n".join(prompt_parts)
    