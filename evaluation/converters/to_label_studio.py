# evaluation/converters/to_label_studio.py

"""
Convert unlabeled scenarios to Label Studio import format.
"""

import json
from loguru import logger


def convert_to_label_studio(unlabeled_path: str, output_path: str):
    """
    Convert unlabeled scenarios to Label Studio tasks.
    
    Each (query, memory) pair becomes one task to label.
    """
    with open(unlabeled_path) as f:
        scenarios = json.load(f)
    
    tasks = []
    
    for scenario in scenarios:
        scenario_id = scenario["scenario"]
        memories = scenario["memories"]
        queries = scenario["queries"]
        
        for q_idx, query_text in enumerate(queries):
            query_id = f"{scenario_id}_q{q_idx}"
            
            # Create one task per (query, memory) pair
            for mem_idx, memory_text in enumerate(memories):
                task = {
                    "data": {
                        # Displayed to user
                        "query": query_text,
                        "memory": memory_text,
                        
                        # Metadata (hidden, used for reconstruction)
                        "scenario_id": scenario_id,
                        "query_id": query_id,
                        "query_idx": q_idx,
                        "memory_idx": mem_idx,
                        
                        # Store all memories for context (optional)
                        "all_memories": memories
                    }
                }
                tasks.append(task)
    
    with open(output_path, 'w') as f:
        json.dump(tasks, f, indent=2)
    
    logger.info(f"✅ Created {len(tasks)} labeling tasks")
    logger.info(f"   From {len(scenarios)} scenarios")
    logger.info(f"   Output: {output_path}")
    
    return len(tasks)


if __name__ == "__main__":
    num_tasks = convert_to_label_studio(
        "evaluation/data/unlabeled_100.json",
        "evaluation/data/label_studio_tasks.json"
    )
    
    print(f"\n{'='*60}")
    print(f"Ready to import to Label Studio!")
    print(f"Tasks: {num_tasks}")
    print(f"File: evaluation/data/label_studio_tasks.json")
    print(f"\nEstimated labeling time: {num_tasks * 2 / 60:.0f} minutes")
    print(f"(at 2 seconds per task with keyboard shortcuts)")
    print(f"{'='*60}")