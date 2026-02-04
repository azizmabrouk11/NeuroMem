# NeuroMem - LLM Memory System 🧠

A sophisticated long-term memory system for AI agents using Google Gemini embeddings, Qdrant vector database, and intelligent retrieval mechanisms.

## Overview

NeuroMem provides AI agents with the ability to maintain persistent, contextual memory across conversations. By leveraging Gemini's text-embedding-004 model and Qdrant vector database, the system enables agents to recall relevant information, learn from past interactions, and build meaningful, long-term relationships with users.

## ✨ Key Features

- **Persistent Memory**: Store and retrieve conversations and user facts
- **Semantic Search**: Find relevant memories using Gemini embeddings (768-dimensional vectors)
- **Batch Processing**: Efficient batch embedding for multiple memories
- **Memory Importance Scoring**: Prioritize significant information
- **Temporal Decay**: Gradually forget outdated information
- **Context-Aware Retrieval**: Build intelligent context for AI responses
- **Memory Reasoning**: Analyze and connect related memories
- **Qdrant Integration**: Fast and scalable vector similarity search

## 🎯 Use Cases

- **Personal AI Assistant**: Remembers preferences, past conversations, and user context
- **Smart Chatbot**: Maintains conversation history and learns from interactions
- **AI Tutor**: Tracks student progress, learning patterns, and knowledge gaps
- **Customer Support**: Recalls previous issues and customer preferences
- **Research Assistant**: Connects information across multiple sessions

## 🏗️ Architecture

```
NeuroMem/
├── ai/              # AI model integrations and LLM interfaces
├── app/             # Application logic and API endpoints
├── config/          # Configuration files and settings (Gemini, Qdrant)
│   └── settings.py  # Centralized configuration management
├── core/            # Core memory system logic
├── db/              # Database connections and vector store
│   └── vectore_store.py  # Qdrant vector database operations
├── intelligence/    # Reasoning and memory analysis
├── memory/          # Memory storage and retrieval
│   ├── store.py     # High-level memory storage interface
│   └── encoding/    # Embedding generation
│       ├── base.py  # Abstract embedder interface
│       └── gemini.py  # Google Gemini embedding implementation
├── models/          # Data models and schemas
│   ├── memory.py    # Memory data model
│   └── user.py      # User data model
├── tests/           # Unit and integration tests
└── utils/           # Helper functions and utilities
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Qdrant (Vector Database) - Running locally or via Qdrant Cloud
- Google Gemini API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/NeuroMem.git
cd NeuroMem
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your Gemini API key and Qdrant configuration
```

Required environment variables:
```env
GEMINI_API_KEY=your_gemini_api_key_here
EMBEDDING_MODEL=models/text-embedding-004
EMBEDDING_DIMENSION=768
LLM_MODEL=gemini-1.5-flash

QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION_NAME=ai_brain_memories
```

### Quick Start

```python
from memory.store import MemoryStore
from memory.encoding.gemini import GeminiEmbedder
from db.vectore_store import VectorStore

# Initialize components
embedder = GeminiEmbedder()
vector_store = VectorStore()
memory_store = MemoryStore(embedder, vector_store)

# Store a single memory
memory = memory_store.store_memory(
    content="User prefers dark mode interface",
    user_id=123,
    importance_score=0.8,
    tags=["preferences", "ui"]
)

# Store multiple memories efficiently (batch embedding)
memories_data = [
    {"content": "Likes Python programming", "user_id": 123},
    {"content": "Works in AI/ML field", "user_id": 123}
]
stored_memories = memory_store.store_memory_batch(memories_data)

# Retrieve relevant memories
results = vector_store.search_similar_memories(
    query_embedding=embedder.embed("What are user preferences?"),
    top_k=5
)
```

## 🔧 Core Technologies

- **Google Gemini**: text-embedding-004 model for 768-dimensional semantic vectors
- **Qdrant**: High-performance vector database for similarity search
- **FastAPI**: Modern web framework for building APIs
- **Pydantic**: Data validation and settings management
- **Memory Architecture**: 
  - `BaseEmbedder`: Abstract interface for embedding providers
  - `GeminiEmbedder`: Gemini implementation with batch processing and retry logic
  - `MemoryStore`: High-level memory management with metadata support
  - `VectorStore`: Qdrant integration for vector operations

## 📖 Documentation

- [API Reference](docs/api.md)
- [Configuration Guide](docs/configuration.md)
- [Memory System Design](docs/architecture.md)
- [Examples](docs/examples.md)

## 🧪 Testing

Run the test suite:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest --cov=. tests/
```

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting PRs.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by research in cognitive architectures and human memory systems
- Built on top of excellent open-source projects in the AI/ML ecosystem

## 📬 Contact

For questions, feedback, or collaboration opportunities, please open an issue or reach out.

---

**Note**: This is a research and educational project. For production use, ensure proper security, privacy, and compliance measures are implemented.
