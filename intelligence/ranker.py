"""
Memory ranking system.
Combines similarity, importance, recency, and access patterns into a final score.
"""

from typing import List
from loguru import logger

from models.memory import MemorySearchResult
from intelligence.scorer import MemoryScorer
from intelligence.decay import TemporalDecay
class MemoryRanker:
    """
    Re-ranks memory search results using multiple signals.
    
    Final score combines:
    - Similarity score (from vector search)
    - Importance score (from scorer)
    - Recency decay (from temporal decay)
    - Access frequency boost (from scorer)
    
    Weighted formula:
        final_score = (similarity * w1) + (importance * w2) + (recency * w3) + (access * w4)
    """
    def __init__(
            self,
            similarity_weight: float = 0.4,
            importance_weight: float = 0.3,
            recency_weight: float = 0.2,
            access_weight: float = 0.1
            ):
        """
        Args:
            similarity_weight: Weight for embedding similarity (0-1)
            importance_weight: Weight for importance score (0-1)
            recency_weight: Weight for temporal recency (0-1)
            access_weight: Weight for access frequency (0-1)
            
        Note: Weights should sum to 1.0 for normalized scores
        """
        if abs(similarity_weight + importance_weight + recency_weight + access_weight - 1) > 0.01:
            total = similarity_weight + importance_weight + recency_weight + access_weight
            logger.warning(f"Weights sum to {total}, not 1.0. Scores may be unnormalized.")
        
        self.similarity_weight = similarity_weight
        self.importance_weight = importance_weight
        self.recency_weight = recency_weight
        self.access_weight = access_weight
        
        self.scorer = MemoryScorer()
        self.decay = TemporalDecay()

    def rank_memories(self, search_results: List[MemorySearchResult])->List[MemorySearchResult]:
        """
        Re-rank search results using all intelligence signals.
        
        Args:
            search_results: List of MemorySearchResult from vector search
            
        Returns:
            Re-ranked list sorted by final_score (highest first)
        """
        if not search_results:
            return []
        
        for result in search_results:
            result.final_score = self._calculate_final_score(result)
        ranked_results = sorted(search_results, key=lambda r: r.final_score, reverse=True)
        logger.info(f"Re-ranked {len(ranked_results)} memories")
        return ranked_results
    def _calculate_final_score(self, result: MemorySearchResult)->float:
        """
        Calculate final score for a single search result.
        
        Combines:
        - similarity_score (from vector search)
        - importance (from memory scorer)
        - recency (from temporal decay)
        - access boost (from memory scorer)
        """
        memory = result.memory
        similarity_score = result.similarity_score
        importance = self.scorer.calculate_importance(memory)
        recency = self.decay.calculate_decay(memory)
        access_boost = self.scorer.calculate_access_boost(memory)
        final_score = (
            similarity_score * self.similarity_weight + 
            importance * self.importance_weight + 
            recency * self.recency_weight + 
            access_boost * self.access_weight
        )
        return final_score