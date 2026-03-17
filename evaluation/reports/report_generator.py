"""
Generate readable evaluation reports.
"""

import json
from datetime import datetime


class ReportGenerator:
    
    def __init__(self, results: dict):
        self.results = results
    
    def print_report(self):
        """Print formatted report to console."""
        print("\n" + "="*50)
        print("AI BRAIN EVALUATION REPORT")
        print("="*50)
        
        # Retrieval
        r = self.results["retrieval"]
        print("\n📊 Retrieval Quality:")
        print(f"  Precision@3: {r['precision@3']:.3f}  {'✅' if r['precision@3'] > 0.7 else '❌'}")
        print(f"  Recall@5:    {r['recall@5']:.3f}  {'✅' if r['recall@5'] > 0.7 else '❌'}")
        print(f"  NDCG@3:      {r['ndcg@3']:.3f}  {'✅' if r['ndcg@3'] > 0.7 else '❌'}")
        print(f"  MRR:         {r['mrr']:.3f}  {'✅' if r['mrr'] > 0.7 else '❌'}")
        self._print_worst_retrieval_cases(r.get("worst_cases", []))
        
        # Deduplication
        d = self.results["deduplication"]
        print("\n🔄 Deduplication:")
        print(f"  Accuracy: {d['accuracy']:.1%}  {'✅' if d['accuracy'] > 0.85 else '❌'}")
        
        # Performance
        p = self.results["performance"]
        print("\n⚡ Performance:")
        print(f"  Store p95: {p['store_latency_p95']:.0f}ms  {'✅' if p['store_latency_p95'] < 500 else '❌'}")
        print(f"  Search p95: {p['search_latency_p95']:.0f}ms  {'✅' if p['search_latency_p95'] < 200 else '❌'}")
        
        print("\n" + "="*50)

    def _print_worst_retrieval_cases(self, worst_cases: list):
        """Print retrieval queries with the weakest ranking quality."""
        if not worst_cases:
            return

        print("\n  Worst Retrieval Cases:")
        for index, case in enumerate(worst_cases, start=1):
            print(f"    {index}. [{case['scenario']}] {case['query_id']}")
            print(f"       Query: {case['query']}")
            print(
                f"       NDCG@5: {case['ndcg@5']:.3f} | RR: {case['reciprocal_rank']:.3f}"
            )
            print("       Expected memories:")
            if case["expected_memories"]:
                for memory in case["expected_memories"]:
                    print(
                        f"         - rel={memory['relevance']} | {memory['content']}"
                    )
            else:
                print("         - None")

            print("       Top 5 retrieved:")
            if case["top_results"]:
                for result in case["top_results"]:
                    print(
                        "         "
                        f"#{result['rank']} "
                        f"rel={result['expected_relevance']} | "
                        f"importance={result['importance_score']:.4f} | "
                        f"score={result['final_score']:.4f} | "
                        f"similarity={result['similarity_score']:.4f} | "
                        f"{result['content']}"
                    )
            else:
                print("         - No retrieval results")
    
    def save_results(self):
        """Save results to file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"evaluation/data/results/eval_{timestamp}.json"
        
        with open(path, "w") as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n✅ Results saved to {path}")