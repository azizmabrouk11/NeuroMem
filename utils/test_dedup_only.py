"""Test only deduplication evaluation."""
from evaluation.evaluators.eval_dedup import DeduplicationEvaluator

print("Running Deduplication Evaluation...")
print("="*60)

evaluator = DeduplicationEvaluator()
results = evaluator.evaluate()

print(f"\nResults:")
print(f"  Accuracy: {results['accuracy']:.1%}")
print(f"  Correct: {results['correct']}/{results['total_cases']}")
print(f"\n{'✅ PASS' if results['accuracy'] == 1.0 else '❌ FAIL'}")
