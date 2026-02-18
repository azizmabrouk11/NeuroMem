"""
Retrieval quality evaluation using ranx.
"""

import json
from ranx import Qrels, Run, evaluate
from core.brain import Brain
from models.memory import MemoryType

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

        for case in self.test_cases:
            memory_ids = []
            for content in case["memories"]:
                memory = brain.remember(
                    content=content,
                    memory_type=MemoryType.SEMANTIC
                )
                memory_ids.append(memory.id)
        
            for query in case["queries"]:
                query_id = query["query_id"]

                qrels_dict[query_id] = {
                    memory_ids[int(idx)]: score
                    for idx, score in query["relevance"].items()
                }
                results = brain.recall(query["query"], top_k=10)

                run_dict[query_id] = {
                    
                    r.memory.id: r.final_score
                    for r in results
                    } 
                
                qrels = Qrels(qrels_dict)
                run = Run(run_dict, name="ai_brain")
                return evaluate(
                    
                qrels, run,
                metrics=["precision@3", "recall@5", "ndcg@3", "mrr", "map"]

                )