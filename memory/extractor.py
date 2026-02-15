"""
Extract memories from conversations using LLM.
Identifies facts, preferences, and important information to store.
"""
from typing import List

from loguru import logger
from openai import OpenAI

from models.memory import MemoryDraft, MemoryType
from config.settings import settings

class MemoryExtractor:
    """
    Extracts memorable information from conversations.
    Uses LLM to identify facts, preferences, and important details.
    """

    def __init__(self):
        """Initialize extractor with Ollama LLM."""
        self.client = OpenAI(
            base_url=settings.ollama_base_url,
            api_key="ollama"  # Dummy key for Ollama compatibility
        )
        self.model_name = settings.ollama_model
        self.client_type = "openai"
        logger.info(f"MemoryExtractor initialized with Ollama model: {self.model_name}")

    def extract_memories(
            self,
            user_message: str,
            assistant_message: str
            ) -> List[MemoryDraft]:
        """
        Extract memories from a conversation turn.
        
        Args:
            user_message: What the user said
            assistant_message: What the assistant responded
            
        Returns:
            List of MemoryDraft objects with content, memory_type, importance_score, and tags
        """
        try: 

            prompt = self._build_extraction_prompt(user_message, assistant_message)
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            memories = self._parse_response(response.choices[0].message.content)
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

Extract memories in this EXACT format (one per line, with actual values):

Examples:
SEMANTIC|0.8|food,preference|User loves spicy Indian food
EPISODIC|0.6|conversation,work|User asked about Python programming on Feb 15
SEMANTIC|0.9|health,allergy|User is allergic to peanuts

Format: TYPE|SCORE|TAGS|CONTENT
- TYPE: SEMANTIC (facts/preferences) or EPISODIC (events/interactions)
- SCORE: Number between 0.0 and 1.0 (importance)
- TAGS: Comma-separated words (no spaces after commas)
- CONTENT: The actual memory text

Only extract truly important information that's worth remembering long-term.
If there's nothing important worth remembering, respond ONLY with: NONE

Output your extracted memories (or NONE):"""
    def _parse_response(self, response_text: str) -> List[MemoryDraft]:
        """
        Parse LLM's extraction response into memory dicts.
        """
        logger.info(f"Attempting to parse response: {response_text[:100]}...")
        memories = []
        lines = response_text.strip().split("\n")
        for line in lines:
            line = line.strip()
            if not line or line.upper() == "NONE":
                continue
            
            # Skip template/example lines
            if "importance_score" in line.lower() or "TYPE|SCORE|TAGS|CONTENT" in line:
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
                logger.debug(f"Extracted memory: {memory.content[:50]}...")
            except ValueError as e:
                logger.warning(f"Skipping invalid memory line (value error): {line}")
            except Exception as e:
                logger.error(f"Error parsing memory line: {line} - {e}")
        return memories




