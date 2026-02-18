"""
Test Ollama embeddings.
"""

from memory.encoding.ollama import OllamaEmbedder

def test_ollama_embeddings():
    print("Testing Ollama embeddings...")
    
    try:
        embedder = OllamaEmbedder()
        
        # Test single embedding
        text = "Hello, this is a test"
        embedding = embedder.embed(text)
        
        print(f"✓ Successfully generated embedding")
        print(f"  Text: '{text}'")
        print(f"  Dimension: {len(embedding)}")
        print(f"  First 5 values: {embedding[:5]}")
        
        # Test batch
        texts = ["First text", "Second text", "Third text"]
        embeddings = embedder.embed_batch(texts)
        
        print(f"\n✓ Successfully generated batch embeddings")
        print(f"  Number of texts: {len(texts)}")
        print(f"  Number of embeddings: {len(embeddings)}")
        
        # Test dimension
        dim = embedder.get_dimension()
        print(f"\n✓ Embedding dimension: {dim}")
        
        print("\n✅ All tests passed! Ollama embeddings are working!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure:")
        print("1. Ollama is running: docker-compose up -d ollama")
        print("2. Model is pulled: docker exec -it ollama ollama pull nomic-embed-text")
        print("3. .env has: EMBEDDING_PROVIDER=ollama")

if __name__ == "__main__":
    test_ollama_embeddings()
