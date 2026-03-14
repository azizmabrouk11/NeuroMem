"""Quick test to verify LangSmith tracing is working."""

from ai.llm import LLMClient

print("Testing LangSmith tracing...")
print("\nInitializing LLM client...")

llm = LLMClient()

print("\nGenerating response...")
response = llm.generate_response(
    prompt="What is 2+2? Answer in one word.",
    system_instruction="You are a helpful assistant."
)

print(f"\nResponse: {response}")
print("\n✓ Test complete! Check LangSmith at: https://smith.langchain.com")
print("  Project: neuroMem")
