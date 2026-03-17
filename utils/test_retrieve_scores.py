"""Small retrieval test script for inspecting memory scores.

Usage examples:
    python utils/test_retrieve_scores.py --query "what food do I like?"
    python utils/test_retrieve_scores.py --query "project deadline" --user-id aziz --top-k 5
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


# Ensure project root is importable when running this file directly.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.brain import Brain


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Retrieve similar memories and print score breakdown."
    )
    parser.add_argument(
        "--query",
        required=True,
        help="Search query text used to retrieve memories.",
    )
    parser.add_argument(
        "--user-id",
        default="eval_user",
        help="User ID whose memories will be searched.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=5,
        help="Number of results to fetch (script prints up to top 5).",
    )
    parser.add_argument(
        "--min-similarity",
        type=float,
        default=0.5,
        help="Minimum similarity threshold (0.0-1.0).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    brain = Brain(user_id=args.user_id)

    results = brain.recall(
        query=args.query,
        top_k=max(args.top_k, 5),
        min_similarity=args.min_similarity,
    )

    top_results = results[:5]

    if not top_results:
        print("No memories found.")
        return

    print(f"Query: {args.query}")
    print(f"User: {args.user_id}")
    print(f"Showing top {len(top_results)} memories (requested top_k={args.top_k})")
    print("=" * 72)

    for idx, result in enumerate(top_results, start=1):
        memory = result.memory
        preview = memory.content.replace("\n", " ").strip()
        if len(preview) > 90:
            preview = f"{preview[:87]}..."

        print(f"[{idx}] {preview}")
        print(f"  Similarity Score: {result.similarity_score:.4f}")
        print(f"  Importance Score: {memory.importance_score:.4f}")
        print(f"  Final Score:      {result.final_score:.4f}")
        print()


if __name__ == "__main__":
    main()
