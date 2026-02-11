"""
Extract memories from conversations using LLM.
Identifies facts, preferences, and important information to store.
"""
from typing import List
import google.generativeai as genai
from loguru import logger

from models.memory import MemoryDraft, MemoryType
from config.settings import settings

class MemoryExtractor:
    """
    Extracts memorable information from conversations.
    Uses LLM to identify facts, preferences, and important details.
    """

    def __init__(self, api_key: str = settings.gemini_api_key):
        """Initialize extractor with LLM."""
        self.api_key = api_key or settings.gemini_api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(settings.llm_model)
        logger.info("MemoryExtractor initialized")

    def extract_memories(
            self,
            user_message: str,
            assistant_message: str
            ) -> List[dict]:
        """
        Extract memories from a conversation turn.
        
        Args:
            user_message: What the user said
            assistant_message: What the assistant responded
            
        Returns:
            List of memory dicts with keys: content, memory_type, importance, tags
        """
        try: 

            prompt = self._build_extraction_prompt(user_message, assistant_message)
            response = self.model.generate_content(prompt)
            memories = self._parse_response(response.text)
            logger.info(f"Extracted {len(memories)} memories from conversation")
            return memories
        except Exception as e:
            logger.error(f"Error extracting memories: {e}")
            return []
    
    def _build_extraction_prompt(self, user_message: str, assistant_message: str) -> str:
        """Construct a prompt to extract memories from the conversation."""


        return f"""You are a memory extraction system. Analyze this conversation and extract important facts, preferences, or information about the user.



            Conversation:
            USER: {user_message}
            ASSISTANT: {assistant_message}

            Extract memories in this EXACT format (one per line):
            SEMANTIC|importance_score|tags|content
            EPISODIC|importance_score|tags|content

            Rules:
            - SEMANTIC: Facts, preferences, long-term information (e.g., "User is allergic to peanuts")
            - EPISODIC: Events, specific interactions (e.g., "User asked about Python on 2024-02-10")
            - importance_score: 0.0 to 1.0 (how important is this information?)
            - tags: comma-separated (e.g., "food,allergy" or "coding,python")
            - content: The actual memory text

            Only extract truly important information. If nothing important, respond with "NONE".

            Extracted memories:"""
    def _parse_response(self, response_text: str) -> List[MemoryDraft]:
        """
        Parse LLM's extraction response into memory dicts.
        """
        memories = []
        lines = response_text.strip().split("\n")
        for line in lines:
            if not line or line == "NONE":
                continue
            try:
                parts = line.split("|", 3)
                if len(parts) != 4:
                    logger.warning(f"Skipping malformed memory line: {line}")
                    continue
                mem_type, importance, tags, content = parts

                mem_type = (
                MemoryType.SEMANTIC 
                    if mem_type.strip().upper() == "SEMANTIC" 
                    else MemoryType.EPISODIC
                )

                importance = float(importance.strip())
                importance = max(0.0, min(1.0, importance))

                tags = [t.strip() for t in tags.split(',') if t.strip()]

                memory = MemoryDraft(
                    content=content.strip(),
                    memory_type=mem_type,
                    importance_score=importance,
                    tags=tags
                )
                memories.append(memory)
                logger.debug(f"Extracted memory: {memory['content'][:50]}...")
            except Exception as e:
                logger.error(f"Error parsing memory line: {line} - {e}")
        return memories




