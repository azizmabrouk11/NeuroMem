"""
Convert Label Studio export JSON into NeuroMem evaluation test-case format.

Input format: list of Label Studio tasks (project export JSON)
Output format: evaluation/data/test_cases.json compatible structure
"""

import argparse
import json
from collections import OrderedDict

from loguru import logger


def _extract_choice_score(task: dict) -> int:
    """Extract numeric relevance score from first annotation choice."""
    annotations = task.get("annotations", [])
    if not annotations:
        return 0

    first_annotation = annotations[0]
    results = first_annotation.get("result", [])
    if not results:
        return 0

    value = results[0].get("value", {})
    choices = value.get("choices", [])
    if not choices:
        return 0

    try:
        return int(choices[0])
    except (TypeError, ValueError):
        return 0


def convert_from_label_studio(input_path: str, output_path: str) -> list[dict]:
    """
    Convert Label Studio exported tasks into NeuroMem test-case structure.
    """
    with open(input_path, encoding="utf-8-sig") as f:
        tasks = json.load(f)

    scenarios = OrderedDict()
    skipped = 0

    for task in tasks:
        data = task.get("data", {})
        scenario_id = data.get("scenario_id")
        query_id = data.get("query_id")
        query_text = data.get("query")
        memory_idx = data.get("memory_idx")
        all_memories = data.get("all_memories")

        if (
            scenario_id is None
            or query_id is None
            or query_text is None
            or memory_idx is None
            or not isinstance(all_memories, list)
            or not all_memories
        ):
            skipped += 1
            continue

        try:
            mem_idx = int(memory_idx)
        except (TypeError, ValueError):
            skipped += 1
            continue

        if mem_idx < 0 or mem_idx >= len(all_memories):
            skipped += 1
            continue

        score = _extract_choice_score(task)

        if scenario_id not in scenarios:
            scenarios[scenario_id] = {
                "scenario": scenario_id,
                "memories": all_memories,
                "queries": OrderedDict(),
            }

        scenario_bucket = scenarios[scenario_id]

        # Keep a stable memory ordering for a scenario.
        if scenario_bucket["memories"] != all_memories:
            scenario_bucket["memories"] = all_memories

        if query_id not in scenario_bucket["queries"]:
            scenario_bucket["queries"][query_id] = {
                "query_id": query_id,
                "query": query_text,
                "relevance": {str(i): 0 for i in range(len(all_memories))},
            }

        scenario_bucket["queries"][query_id]["relevance"][str(mem_idx)] = score

    output = []
    for scenario in scenarios.values():
        output.append(
            {
                "scenario": scenario["scenario"],
                "memories": scenario["memories"],
                "queries": list(scenario["queries"].values()),
            }
        )

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    logger.info(f"Converted scenarios: {len(output)}")
    logger.info(f"Input tasks: {len(tasks)}")
    logger.info(f"Skipped tasks: {skipped}")
    logger.info(f"Output written to: {output_path}")

    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert Label Studio export JSON to NeuroMem evaluation format."
    )
    parser.add_argument(
        "--input-path",
        default="evaluation/data/project-1-at-2026-03-18-02-30-cc045d7f.json",
        help="Path to Label Studio export JSON",
    )
    parser.add_argument(
        "--output-path",
        default="evaluation/data/test_cases_from_label_studio.json",
        help="Path for converted NeuroMem test cases JSON",
    )
    args = parser.parse_args()

    convert_from_label_studio(args.input_path, args.output_path)
