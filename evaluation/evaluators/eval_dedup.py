"""
Deduplication evaluation.
Tests if online dedup catches similar memories.
"""

from core.brain import Brain
from models.memory import MemoryType

class DeduplicationEvaluator:
    DEDUP_CASES = [
        {
            "memories": [
                "User loves spicy Indian food",
                "User really enjoys spicy Indian cuisine",    # Should merge (very similar)
                "User likes spicy dishes from India",         # Should merge (very similar)
            ],
            "expected_count": 1  # Should end up with 1 memory
        },
        {
            "memories": [
                "User is learning Python programming",
                "User is learning Python",                     # Should merge (almost identical)
                "User likes pizza",                             # Should NOT merge
            ],
            "expected_count": 2  # 1 Python memory + 1 food memory
        }
    ]

    def evaluate(self, user_id: str = "dedup_eval_user") -> dict:
        """
        Evaluates deduplication by adding similar memories and checking count.
        Returns a dictionary with results for each case.
        """
        total_cases = len(self.DEDUP_CASES)
        correct = 0
        
        for i, case in enumerate(self.DEDUP_CASES, 1):
            # Create separate brain for each test case to avoid mixing memories
            test_user = f"{user_id}_case_{i}"
            brain = Brain(user_id=test_user)
            
            # Store memories
            for content in case["memories"]:
                brain.remember(content, memory_type=MemoryType.SEMANTIC)
            
            # Count actual memories stored (direct count from database)
            actual_count = brain.count_memories()
            
            if actual_count == case["expected_count"]:
                correct += 1
        
        return {
            "accuracy": correct / total_cases if total_cases > 0 else 0,
            "total_cases": total_cases,
            "correct": correct
        }