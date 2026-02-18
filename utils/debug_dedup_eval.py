"""Debug deduplication evaluation."""
from core.brain import Brain
from models.memory import MemoryType

# Test Case 1
print("=" * 60)
print("Test Case 1: Food memories")
print("=" * 60)
brain = Brain(user_id="debug_case_1")

memories_to_store = [
    "User loves spicy Indian food",
    "User enjoys spicy dishes",
    "User prefers hot meals",
]

for i, content in enumerate(memories_to_store, 1):
    mem = brain.remember(content, memory_type=MemoryType.SEMANTIC)
    count = brain.count_memories()
    print(f"{i}. Stored: '{content}'")
    print(f"   Memory ID: {mem.id[:8]}...")
    print(f"   Total count now: {count}")
    print()

final_count = brain.count_memories()
print(f"Final count: {final_count}")
print(f"Expected: 1 (should merge)")
print(f"Result: {'✅ PASS' if final_count == 1 else '❌ FAIL'}")

print("\n" + "=" * 60)
print("Test Case 2: Mixed memories")
print("=" * 60)
brain2 = Brain(user_id="debug_case_2")

memories_to_store2 = [
    "User is learning Python",
    "User studies Python programming",
    "User loves spicy food",
]

for i, content in enumerate(memories_to_store2, 1):
    mem = brain2.remember(content, memory_type=MemoryType.SEMANTIC)
    count = brain2.count_memories()
    print(f"{i}. Stored: '{content}'")
    print(f"   Memory ID: {mem.id[:8]}...")
    print(f"   Total count now: {count}")
    print()

final_count2 = brain2.count_memories()
print(f"Final count: {final_count2}")
print(f"Expected: 2 (1 Python + 1 food)")
print(f"Result: {'✅ PASS' if final_count2 == 2 else '❌ FAIL'}")
