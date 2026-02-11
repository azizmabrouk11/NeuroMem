"""
LLM client for generating responses.
Uses Google Gemini API.
"""

from typing import List, Optional
import google.generativeai as genai
from loguru import logger

from config.settings import settings

class LLMClient:
    """
    Initialize Gemini client.
        
    Args:
        model_name: Gemini model to use (default from settings)
    """
    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or settings.llm_model
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel(self.model_name)
        logger.info(f"Initialized LLM client with model: {self.model_name}")

    def generate_response(
            self,
            prompt: str,
            context: Optional[str] = None,
            system_instruction: Optional[str] = None,
            temperature: float = 0.7,
            max_tokens: int = 1000
        )-> str:
        """
        Generate a response from the LLM.
        
        Args:
            prompt: User's message
            context: Memory context to include
            system_instruction: System-level instructions
            temperature: Creativity (0.0-1.0)
            max_tokens: Max response length
            
        Returns:
            Generated text response
        """
        try: 
            full_prompt = self._build_prompt(prompt, context, system_instruction)
            logger.debug(f"Sending prompt to LLM (length: {len(full_prompt)} chars)")
            generation_config = genai.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens

            )
            if system_instruction:
                model = genai.GenerativeModel(
                    self.model_name,
                    system_instruction=system_instruction
                )
            else: 
                model = self.model
        
            response = model.generate_content(
                prompt=full_prompt,
                generation_config=generation_config
            )
            result =response.text
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
    