"""
Memory importance scoring.
Determines how valuable a memory is based on content, type, and access patterns.
"""
from models.memory import Memory, MemoryType
import math
class MemoryScorer:
    """
    Calculates importance scores for memories.
    
    Factors considered:
    - Memory type (semantic facts are more important than episodic events)
    - Access frequency (frequently retrieved memories are important)
    - Content length (very short memories may be less important)
    """

    def __init__(
            self,
            semantic_weight: float = 1.2,
            episodic_weight: float = 1.0,
            min_content_length: int = 10
            ):
        
        """
        Args:
            semantic_weight: Multiplier for semantic memories (facts, preferences)
            episodic_weight: Multiplier for episodic memories (conversations, events)
            min_content_length: Minimum expected content length (characters)
        """

        self.semantic_weight = semantic_weight
        self.episodic_weight = episodic_weight
        self.min_content_length = min_content_length


    def calculate_importance(self, memory: Memory)->float:
        """
        Calculate base importance score for a memory.
        
        Returns score between 0.0 and 1.0
        """
        base_score =memory.importance_score
        type_multiplier = self._get_type_multiplier(memory.memory_type)
        length_factor = self._get_length_factor(memory.content)
        importance =base_score * type_multiplier * length_factor

        return max(0.0, min(importance, 1.0))  
    
    def calculate_access_boost(self, memory: Memory)->float:
        """
        Boost frequently accessed memories.
        
        Returns:
            Access boost multiplier (1.0 - 2.0)
        """
        boost = 1.0 + math.log1p(memory.access_count) * 0.1
        return min(boost, 2.0)
    
    def _get_type_multiplier(self, memory_type: MemoryType)->float:
        """
        Get importance multiplier based on memory type.
        
        Semantic memories (facts, preferences) are generally more important
        than episodic memories (specific events).
        """
        if memory_type == MemoryType.SEMANTIC:
            return self.semantic_weight
        elif memory_type == MemoryType.EPISODIC:
            return self.episodic_weight
        else:
            return 1.0
    
    def _get_length_factor(self, content: str)->float:
        """
        Penalize very short content.
        
        Very short memories (< min_content_length) might be incomplete
        or low-quality, so we reduce their importance slightly.
        """
        length = len(content.strip())
        if length >= self.min_content_length:
            return 1.0
        factor = 0.5 + (length / (2 *self.min_content_length))
        return max(factor, 0.5)
