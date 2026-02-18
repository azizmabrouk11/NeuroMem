"""
Performance benchmarks.
Measures latency for store and search operations.
"""

import time
import numpy as np
from core.brain import Brain
from models.memory import MemoryType


class PerformanceEvaluator:
    
    def evaluate(self, user_id: str = "perf_eval", n: int = 50) -> dict:
        """Benchmark store and search latency."""
        brain = Brain(user_id=user_id)
        
        # Benchmark store
        store_times = []
        for i in range(n):
            start = time.perf_counter()
            brain.remember(
                f"Test memory number {i}",
                memory_type=MemoryType.SEMANTIC
            )
            store_times.append(time.perf_counter() - start)
        
        # Benchmark search
        search_times = []
        for i in range(n):
            start = time.perf_counter()
            brain.recall(f"test query {i}", top_k=5)
            search_times.append(time.perf_counter() - start)
        
        return {
            "store_latency_p50": np.percentile(store_times, 50) * 1000,  # ms
            "store_latency_p95": np.percentile(store_times, 95) * 1000,
            "search_latency_p50": np.percentile(search_times, 50) * 1000,
            "search_latency_p95": np.percentile(search_times, 95) * 1000,
            "n_operations": n
        }