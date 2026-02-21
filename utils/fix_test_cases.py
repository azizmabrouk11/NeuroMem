import json

# Load test cases
with open('evaluation/data/test_cases.json', 'r') as f:
    data = json.load(f)

fixed_count = 0
for i, case in enumerate(data):
    num_memories = len(case['memories'])
    
    for query in case['queries']:
        # Get valid indices (must be within range)
        old_relevance = query['relevance'].copy()
        new_relevance = {}
        
        for idx_str, score in old_relevance.items():
            idx = int(idx_str)
            if idx < num_memories:
                new_relevance[idx_str] = score
        
        if old_relevance != new_relevance:
            query['relevance'] = new_relevance
            fixed_count += 1
            print(f"Fixed scenario {i} ({case['scenario']}), query {query['query_id']}")
            print(f"  Memories: {num_memories}, Old indices: {list(old_relevance.keys())} → New: {list(new_relevance.keys())}")

# Save fixed test cases
with open('evaluation/data/test_cases.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"\n✅ Fixed {fixed_count} queries with invalid indices")
