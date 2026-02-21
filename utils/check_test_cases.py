import json

with open('evaluation/data/test_cases.json') as f:
    data = json.load(f)

for i, case in enumerate(data):
    num_memories = len(case['memories'])
    print(f"\nScenario {i}: {case['scenario']}")
    print(f"  Memories: {num_memories}")
    
    for query in case['queries']:
        relevance_indices = [int(idx) for idx in query['relevance'].keys()]
        max_idx = max(relevance_indices) if relevance_indices else -1
        print(f"  Query {query['query_id']}: max relevance index = {max_idx}")
        
        if max_idx >= num_memories:
            print(f"    ❌ ERROR: Index {max_idx} out of range for {num_memories} memories!")
