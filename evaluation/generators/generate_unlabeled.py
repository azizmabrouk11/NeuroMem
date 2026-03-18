# evaluation/generators/generate_unlabeled.py

"""
Generate unlabeled scenarios for Label Studio.
LLM creates memories + queries, YOU label relevance.
"""

import json
from ai.llm import LLMClient
from loguru import logger


GENERATION_PROMPT = """Generate 10 diverse personal memory test scenarios.

REQUIREMENTS:
1. Each scenario represents ONE person
2. Each scenario has 5-7 varied memories about that person
3. Each scenario has 2-3 SPECIFIC questions someone might ask
4. DO NOT include relevance scores - just memories and questions

DIVERSITY REQUIREMENTS:
- Mix memory types: facts, preferences, events, habits, skills
- Mix topics: food, work, health, hobbies, family, tech, travel, etc.
- Make queries SPECIFIC and realistic (not vague like "tell me about user")

GOOD EXAMPLES:

Scenario 1 - Food & Diet:
Memories:
- User is severely allergic to peanuts
- User loves spicy Thai cuisine
- User became vegetarian in 2023
- User drinks 3 cups of coffee daily
- User is trying to reduce sugar intake

Queries:
- What foods should I absolutely avoid serving the user?
- What type of cuisine does the user prefer?
- What dietary restrictions does the user have?

Scenario 2 - Work & Skills:
Memories:
- User works as a senior software engineer at Google
- User specializes in machine learning and Python
- User has 8 years of experience in tech
- User is learning Rust programming
- User mentors junior developers

Queries:
- What programming languages does the user know?
- Where does the user work?
- What is the user's area of expertise?

GENERATE 10 SCENARIOS with this structure:

Return ONLY valid JSON (no markdown, no code blocks):
[
  {
    "scenario": "food_allergies_and_diet",
    "memories": [
      "User is severely allergic to peanuts",
      "User loves spicy Thai cuisine",
      "User became vegetarian in 2023",
      "User drinks 3 cups of coffee daily",
      "User is trying to reduce sugar intake"
    ],
    "queries": [
      "What foods should I absolutely avoid serving the user?",
      "What type of cuisine does the user prefer?",
      "What dietary restrictions does the user have?"
    ]
  },
  {
    "scenario": "work_and_technical_skills",
    "memories": [
      "User works as a senior software engineer at Google",
      "User specializes in machine learning and Python",
      "User has 8 years of experience in tech",
      "User is learning Rust programming",
      "User mentors junior developers"
    ],
    "queries": [
      "What programming languages does the user know?",
      "Where does the user work?",
      "What is the user's area of expertise?"
    ]
  }
]

IMPORTANT TOPICS TO COVER (pick different ones for each scenario):
- Food preferences and allergies
- Work and career
- Health and fitness
- Technology and gadgets
- Hobbies and interests
- Travel and location
- Family and relationships
- Education and learning
- Daily habits and routines
- Entertainment (movies, music, books, games)

Generate 10 diverse scenarios now:
"""


class UnlabeledDataGenerator:
    """Generate unlabeled test scenarios using LLM."""
    
    def __init__(self):
        self.llm = LLMClient()
    
    def generate_batch(self, num_scenarios: int = 10) -> list:
        """Generate one batch of scenarios."""
        
        logger.info(f"Generating {num_scenarios} scenarios...")
        
        response = self.llm.generate_response(
            GENERATION_PROMPT,
            temperature=0.8,  # Higher creativity
            max_tokens=4000
        )
        
        # Clean response (remove markdown if present)
        response = response.strip()
        if response.startswith("```json"):
            response = response[7:]  # Remove ```json
        if response.startswith("```"):
            response = response[3:]  # Remove ```
        if response.endswith("```"):
            response = response[:-3]  # Remove trailing ```
        response = response.strip()
        
        try:
            scenarios = json.loads(response)
            logger.info(f"✅ Generated {len(scenarios)} scenarios")
            return scenarios
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response: {e}")
            logger.error(f"Response was: {response[:500]}...")
            return []
    
    def generate_dataset(self, total_scenarios: int = 100) -> list:
        """Generate full dataset in batches."""
        
        all_scenarios = []
        batches = (total_scenarios + 9) // 10  # Round up
        
        for i in range(batches):
            logger.info(f"Batch {i+1}/{batches}...")
            batch = self.generate_batch(num_scenarios=10)
            
            if batch:
                all_scenarios.extend(batch)
            
            # Stop if we have enough
            if len(all_scenarios) >= total_scenarios:
                break
        
        return all_scenarios[:total_scenarios]
    
    def save(self, scenarios: list, output_path: str):
        """Save scenarios to JSON."""
        with open(output_path, 'w') as f:
            json.dump(scenarios, f, indent=2)
        
        total_queries = sum(len(s['queries']) for s in scenarios)
        logger.info(f"✅ Saved {len(scenarios)} scenarios ({total_queries} queries)")
        logger.info(f"   Output: {output_path}")


if __name__ == "__main__":
    generator = UnlabeledDataGenerator()
    
    # Generate 100 scenarios
    scenarios = generator.generate_dataset(total_scenarios=100)
    
    # Save
    generator.save(scenarios, "evaluation/data/unlabeled_100.json")
    
    # Stats
    print(f"\n{'='*60}")
    print(f"Generated {len(scenarios)} scenarios")
    print(f"Total queries: {sum(len(s['queries']) for s in scenarios)}")
    print(f"Avg memories per scenario: {sum(len(s['memories']) for s in scenarios) / len(scenarios):.1f}")
    print(f"Avg queries per scenario: {sum(len(s['queries']) for s in scenarios) / len(scenarios):.1f}")
    print(f"{'='*60}")