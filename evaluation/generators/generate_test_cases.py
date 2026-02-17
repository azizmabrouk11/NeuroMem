# evaluation/generate_test_cases.py

import json
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from openai import OpenAI
from config.settings import settings

def generate_test_cases(n: int = 20) -> list:
    """Generate test cases using LLM."""
    
    client = OpenAI(
        base_url=settings.ollama_base_url,
        api_key="ollama"  # Dummy key for Ollama
    )
    
    prompt = f"""Generate {n} test cases for a personal AI memory system evaluation.

Each test case should have:
- A scenario name
- 5-7 realistic personal memories about a user
- 2 queries with relevance scores (2=highly relevant, 1=somewhat, 0=not relevant)

Return ONLY valid JSON in this exact format:
[
  {{
    "scenario": "food_preferences",
    "memories": [
      "User loves spicy Indian food",
      "User is allergic to peanuts",
      "User is learning Python",
      "User had pizza yesterday",
      "User hates mushrooms"
    ],
    "queries": [
      {{
        "query_id": "food_q1",
        "query": "What food does the user like?",
        "relevance": {{
          "0": 2,
          "3": 1,
          "1": 0,
          "2": 0,
          "4": 0
        }}
      }}
    ]
  }}
]

Generate diverse scenarios covering:
- Food preferences
- Work/skills
- Personal facts
- Health information
- Hobbies/interests
- Location/travel
- Family/relationships"""

    response = client.chat.completions.create(
        model=settings.ollama_model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates test data in JSON format. Only return valid, complete JSON arrays. Always close all brackets and braces properly."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=8000
    )
    
    # Parse JSON from response
    text = response.choices[0].message.content
    
    # Remove markdown code blocks if present
    text = text.replace("```json", "").replace("```", "").strip()
    
    # Extract JSON array from text (find the outermost [ ... ])
    start_idx = text.find('[')
    end_idx = text.rfind(']')
    
    if start_idx != -1 and end_idx != -1:
        text = text[start_idx:end_idx+1]
    
    try:
        test_cases = json.loads(text)
        return test_cases
    except json.JSONDecodeError as e:
        print(f"\n❌ JSON parsing error: {e}")
        print(f"Response preview (first 500 chars):\n{text[:500]}")
        print(f"\nResponse end (last 500 chars):\n{text[-500:]}")
        raise


def generate_test_cases_batch(total: int = 50, batch_size: int = 5) -> list:
    """Generate test cases in batches to avoid token limit issues."""
    all_cases = []
    
    num_batches = (total + batch_size - 1) // batch_size
    
    for i in range(num_batches):
        remaining = total - len(all_cases)
        current_batch_size = min(batch_size, remaining)
        
        print(f"Generating batch {i+1}/{num_batches} ({current_batch_size} cases)...")
        
        try:
            cases = generate_test_cases(n=current_batch_size)
            all_cases.extend(cases)
            print(f"  ✓ Generated {len(cases)} cases (total: {len(all_cases)}/{total})")
        except Exception as e:
            print(f"  ✗ Batch {i+1} failed: {e}")
            continue
    
    return all_cases


if __name__ == "__main__":
    print("Generating test cases...")
    cases = generate_test_cases_batch(total=120, batch_size=5)
    
    with open("evaluation/data/test_cases.json", "w") as f:
        json.dump(cases, f, indent=2)
    
    print(f"\n✅ Generated {len(cases)} test cases → evaluation/data/test_cases.json")