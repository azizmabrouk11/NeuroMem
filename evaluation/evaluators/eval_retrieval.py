"""
Retrieval quality evaluation using ranx.
"""

import json
import math
from typing import Dict, List

from ranx import Qrels, Run, evaluate
from core.brain import Brain
from models.memory import MemoryType


def _dcg(relevances: List[int], k: int) -> float:
    """Compute discounted cumulative gain for the top-k ranked relevances."""
    score = 0.0
    for rank, relevance in enumerate(relevances[:k], start=1):
        if relevance <= 0:
            continue
        score += relevance / math.log2(rank + 1)
    return score


def _ndcg_at_k(relevances: List[int], ideal_relevances: List[int], k: int) -> float:
    """Compute normalized discounted cumulative gain at k."""
    ideal_dcg = _dcg(sorted(ideal_relevances, reverse=True), k)
    if ideal_dcg == 0:
        return 0.0
    return _dcg(relevances, k) / ideal_dcg


def _reciprocal_rank(relevances: List[int]) -> float:
    """Compute reciprocal rank for the first relevant retrieved item."""
    for rank, relevance in enumerate(relevances, start=1):
        if relevance > 0:
            return 1.0 / rank
    return 0.0

class RetrievalEvaluator:
    """
    Evaluator for retrieval quality of the AI memory system.
    """
    def __init__(self, test_cases_path: str):
        with open(test_cases_path) as f:
            self.test_cases = json.load(f)

    def evaluate(self) -> dict:
        """
        Evaluate retrieval quality using ranx.
        Returns a dictionary of evaluation metrics.
        """
        brain = Brain(user_id="eval_user")
        qrels_dict = {}
        run_dict = {}
        query_diagnostics = []

        for case_index, case in enumerate(self.test_cases):
            scenario = case.get("scenario", "unknown")
            memory_ids = []
            memory_contents = {}
            for content in case["memories"]:
                memory = brain.remember(
                    content=content,
                    memory_type=MemoryType.SEMANTIC
                )
                memory_ids.append(memory.id)
                memory_contents[memory.id] = memory.content
        
            for query in case["queries"]:
                query_id = query["query_id"]
                query_key = f"{scenario}_{case_index}_{query_id}"
                expected_relevance = {
                    memory_ids[int(idx)]: score
                    for idx, score in query["relevance"].items()
                }

                qrels_dict[query_key] = expected_relevance
                results = brain.recall(query["query"], top_k=10)

                run_dict[query_key] = {
                    r.memory.id: r.final_score
                    for r in results
                }

                retrieved_relevances = [
                    expected_relevance.get(result.memory.id, 0)
                    for result in results
                ]
                ideal_relevances = list(expected_relevance.values())
                query_diagnostics.append(
                    self._build_query_diagnostic(
                        scenario=scenario,
                        query_id=query_key,
                        query_text=query["query"],
                        expected_relevance=expected_relevance,
                        memory_contents=memory_contents,
                        results=results,
                        retrieved_relevances=retrieved_relevances,
                        ideal_relevances=ideal_relevances,
                    )
                )
        
        # Evaluate after processing all scenarios and queries
        qrels = Qrels(qrels_dict)
        run = Run(run_dict, name="ai_brain")
        metrics = evaluate(
            qrels, run,
            metrics=["precision@3", "recall@5", "ndcg@3", "mrr", "map"]
        )
        metrics["worst_cases"] = sorted(
            query_diagnostics,
            key=lambda item: (item["ndcg@5"], item["reciprocal_rank"], -item["best_expected_relevance"])
        )[:3]
        return metrics

    def _build_query_diagnostic(
        self,
        scenario: str,
        query_id: str,
        query_text: str,
        expected_relevance: Dict[str, int],
        memory_contents: Dict[str, str],
        results,
        retrieved_relevances: List[int],
        ideal_relevances: List[int],
    ) -> dict:
        """Build per-query diagnostic details for the worst-case report."""
        expected_memories = [
            {
                "memory_id": memory_id,
                "content": memory_contents.get(memory_id, "<missing memory>"),
                "relevance": relevance,
            }
            for memory_id, relevance in sorted(
                expected_relevance.items(), key=lambda item: item[1], reverse=True
            )
            if relevance > 0
        ]
        top_results = []
        for rank, result in enumerate(results[:5], start=1):
            memory = result.memory
            top_results.append(
                {
                    "rank": rank,
                    "memory_id": memory.id,
                    "content": memory.content,
                    "importance_score": memory.importance_score,
                    "similarity_score": result.similarity_score,
                    "final_score": result.final_score,
                    "expected_relevance": expected_relevance.get(memory.id, 0),
                }
            )

        return {
            "scenario": scenario,
            "query_id": query_id,
            "query": query_text,
            "ndcg@5": _ndcg_at_k(retrieved_relevances, ideal_relevances, 5),
            "reciprocal_rank": _reciprocal_rank(retrieved_relevances),
            "best_expected_relevance": max(ideal_relevances, default=0),
            "expected_memories": expected_memories,
            "top_results": top_results,
        }