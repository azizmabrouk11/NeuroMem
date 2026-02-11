"""
Conversational chat with memory integration.
Handles the full loop: retrieve → generate → extract → store.
"""
from typing import List, Optional
from loguru import logger

from core.brain import Brain
from ai.llm import LLMClient
from memory.extractor import MemoryExtractor

class ChatManager:
    """
    Chat system with persistent memory.
    
    Flow:
    1. User sends message
    2. Retrieve relevant memories
    3. Build context from memories
    4. Generate LLM response with context
    5. Extract new memories from conversation
    6. Store new memories
    7. Return response
    """
    def __init__(
            self,
            user_id: str,
            system_instruction: Optional[str] = None
    ):
        """
        Initialize chat for a user.
        
        Args:
            user_id: User identifier
            system_instruction: System-level instructions for the LLM
        """
        self.user_id = user_id
        self.system_instruction = system_instruction or self._default_system_instruction()
        self.brain = Brain(user_id=user_id)
        self.llm_client = LLMClient() 
        self.memory_extractor = MemoryExtractor()

        self.conversation_history: List[dict] = []
        logger.info(f"MemoryChat initialized for user: {user_id}")

    def chat(self,
            user_message: str,
            auto_extract: bool = True, 
            max_context_memories: int = 10
            ) -> str:
        """
        Send a message and get a response.
        
        Args:
            user_message: User's message
            auto_extract: Automatically extract and store memories
            max_context_memories: Max memories to include in context
            
        Returns:
            Assistant's response
        """
        try:
             
            logger.info(f"User message: {user_message}")

            context = self.brain.get_context(
                query=user_message,
                max_memories=max_context_memories
            )
            response = self.llm_client.generate_response(
                prompt=user_message,
                context=context,
                system_instruction=self.system_instruction
            )
            logger.info(f"Assistant response: {response[:100]}...")

            if auto_extract:
                    self._extract_and_store(user_message, response)
            
            self.conversation_history.append({
                    "role": "user",
                    "content": user_message
                })
            self.conversation_history.append({
                    "role": "assistant",
                    "content": response
                })
            return response
        except Exception as e:
            logger.error(f"Error during chat: {e}")
            return "Sorry, something went wrong."
        
    def _extract_and_store(
              
            self,
            user_message: str,
            assistant_message: str
            ):
        """
        Extract memories from conversation and store them.
        """
        try:
            drafts = self.memory_extractor.extract_memories(user_message, assistant_message)
            if not drafts:
                logger.info("No memories extracted from conversation.")
                return
            for draft in drafts:
                memory = draft.to_memory(user_id=self.user_id)
                self.brain.remember(
                    content=memory.content,
                    memory_type=memory.memory_type,
                    importance_score=memory.importance_score,
                    tags=memory.tags
                )
                logger.debug(f"Stored memory: {draft.content[:50]}...")

            logger.info(f"Extracted and stored {len(drafts)} memories from conversation.")
        except Exception as e:
            logger.error(f"Error extracting/storing memories: {e}")


    def reset_conversation(self):
        """Clear conversation history (but keep stored memories)."""
        self.conversation_history = []
        logger.info("Conversation history reset")
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the conversation history."""
        if not self.conversation_history:
            return "No conversation yet."
        
        lines = []
        for msg in self.conversation_history:
            role = "You" if msg["role"] == "user" else "Assistant"
            lines.append(f"{role}: {msg['content']}")
        
        return "\n".join(lines)
    
    def _default_system_instruction(self) -> str:
        """Default system instruction for the LLM."""
        return """You are a helpful AI assistant with long-term memory.
You can remember information about the user from past conversations.
When relevant memories are provided in the context, use them to personalize your responses.
Be natural, helpful, and conversational."""
             



