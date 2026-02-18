"""
Main evaluation entry point.
Runs all evaluations and generates report.
"""

from evaluation.evaluators.eval_retrieval import RetrievalEvaluator
from evaluation.evaluators.eval_dedup import DeduplicationEvaluator
from evaluation.evaluators.eval_performance import PerformanceEvaluator
from evaluation.reports.report_generator import ReportGenerator
from datetime import datetime
import json


def run_all(test_cases_path: str = "evaluation/data/test_cases.json"):
    """Run complete evaluation suite."""
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "retrieval": None,
        "deduplication": None,
        "performance": None
    }
    
    # 1. Retrieval evaluation
    print("Running retrieval evaluation...")
    retrieval_eval = RetrievalEvaluator(test_cases_path)
    results["retrieval"] = retrieval_eval.evaluate()
    
    # 2. Deduplication evaluation
    print("Running deduplication evaluation...")
    dedup_eval = DeduplicationEvaluator()
    results["deduplication"] = dedup_eval.evaluate()
    
    # 3. Performance benchmarks
    print("Running performance benchmarks...")
    perf_eval = PerformanceEvaluator()
    results["performance"] = perf_eval.evaluate()
    
    # 4. Generate report
    report = ReportGenerator(results)
    report.print_report()
    report.save_results()
    
    return results


if __name__ == "__main__":
    run_all()