"""
Manual deduplication testing.
Tests if similar memories are properly merged.
"""

from core.brain import Brain
from models.memory import MemoryType


def test_deduplication():
    print("=" * 60)
    print("DEDUPLICATION TEST")
    print("=" * 60)
    
    brain = Brain(user_id="test_dedup")
    
    # Test Case 1: Very similar memories (should merge)
    print("\n📌 Test 1: Very similar memories")
    print("-" * 60)
    mem1 = brain.remember("User loves pizza", memory_type=MemoryType.SEMANTIC)
    print(f"✓ Memory 1: '{mem1.content}'")
    print(f"  ID: {mem1.id}, access_count: {mem1.access_count}")
    
    mem2 = brain.remember("User enjoys pizza", memory_type=MemoryType.SEMANTIC)
    print(f"\n✓ Memory 2: '{mem2.content}'")
    print(f"  ID: {mem2.id}, access_count: {mem2.access_count}")
    
    if mem1.id == mem2.id:
        print(f"\n✅ MERGED! Same ID, access_count increased to {mem2.access_count}")
    else:
        print(f"\n❌ NOT MERGED! Different IDs: {mem1.id} vs {mem2.id}")
    
    # Test Case 2: Similar but different enough (should NOT merge)
    print("\n\n📌 Test 2: Similar but different topics")
    print("-" * 60)
    mem3 = brain.remember("User loves spicy food", memory_type=MemoryType.SEMANTIC)
    print(f"✓ Memory 3: '{mem3.content}'")
    print(f"  ID: {mem3.id}, access_count: {mem3.access_count}")
    
    if mem3.id != mem1.id:
        print(f"\n✅ CORRECT! Different memory stored (spicy food ≠ pizza)")
    else:
        print(f"\n❌ WRONG! Should be different memory")
    
    # Test Case 3: Completely different (should NOT merge)
    print("\n\n📌 Test 3: Completely different content")
    print("-" * 60)
    mem4 = brain.remember("User is learning Python programming", memory_type=MemoryType.SEMANTIC)
    print(f"✓ Memory 4: '{mem4.content}'")
    print(f"  ID: {mem4.id}")
    
    if mem4.id not in [mem1.id, mem3.id]:
        print(f"\n✅ CORRECT! New memory stored (programming ≠ food)")
    else:
        print(f"\n❌ WRONG! Should be different memory")
    
    # Summary
    print("\n\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    # Query for different topics to see all memories
    food_results = brain.recall("food preferences", top_k=10)
    programming_results = brain.recall("programming skills", top_k=10)
    
    all_memories = {}
    for result in food_results + programming_results:
        all_memories[result.memory.id] = result.memory
    
    print(f"Total unique memories stored: {len(all_memories)}")
    print("\nMemory details:")
    for i, (mem_id, mem) in enumerate(all_memories.items(), 1):
        print(f"  {i}. '{mem.content}'")
        print(f"     ID: {mem_id[:8]}..., access_count: {mem.access_count}")
    
    # Expected results
    print("\n" + "=" * 60)
    print("EXPECTED: 3 unique memories")
    print("  1. 'User loves pizza' (access_count: 1 - merged)")
    print("  2. 'User loves spicy food' (access_count: 0)")
    print("  3. 'User is learning Python programming' (access_count: 0)")
    print("=" * 60)


if __name__ == "__main__":
    test_deduplication()