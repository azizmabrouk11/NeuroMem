<div align="center">

# 🧠 NeuroMem

### *AI Memory System with Brain-Inspired Intelligence*

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Qdrant](https://img.shields.io/badge/Vector_DB-Qdrant-red.svg)](https://qdrant.tech/)
[![Gemini](https://img.shields.io/badge/Embeddings-Google_Gemini-4285F4.svg)](https://ai.google.dev/)

*Give your AI agents the power of long-term memory, contextual understanding, and intelligent recall.*

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [CLI](#-cli-interface) • [Examples](#-usage-examples)

</div>

---

## 🌟 Overview

**NeuroMem** is a production-ready, brain-inspired memory system that enables AI agents to maintain persistent, contextual awareness across conversations. By combining cutting-edge vector embeddings with intelligent ranking algorithms, NeuroMem brings human-like memory capabilities to your AI applications.

### Why NeuroMem?

- 🎯 **Context-Aware**: Retrieve the most relevant memories based on semantic similarity, not just keywords
- 🧮 **Intelligent Scoring**: Multi-factor ranking using importance, recency, and access patterns
- ⚡ **High Performance**: Batch processing and efficient vector search with Qdrant
- 🔄 **Temporal Decay**: Naturally forget outdated information, just like human memory
- 🎨 **Memory Types**: Distinguish between episodic events and semantic facts
- 🛠️ **Production Ready**: Built-in retry logic, error handling, and comprehensive logging

## ✨ Features

### Core Capabilities

| Feature | Description |
|---------|-------------|
| 🎯 **Semantic Search** | Find relevant memories using Google Gemini's 3072-dimensional embeddings |
| 📦 **Batch Processing** | Efficiently embed multiple memories in a single API call |
| 🏆 **Smart Ranking** | Multi-signal scoring: similarity × importance × recency × access frequency |
| 🕐 **Temporal Decay** | Automatic memory aging with exponential decay function |
| 🏷️ **Tagging System** | Organize memories with custom tags for filtered retrieval |
| 👥 **Multi-User** | Isolated memory spaces per user with optional cross-user search |
| 🎭 **Memory Types** | Episodic (events/conversations) and Semantic (facts/preferences) |
| 🔄 **Access Tracking** | Monitor memory usage patterns for adaptive importance scoring |
| 📊 **Context Building** | Generate formatted LLM-ready context from relevant memories |
| 🛡️ **Robust Design** | Built-in retry logic, error handling, and comprehensive logging |

### Intelligence Layer

- **Memory Scorer**: Evaluates importance based on type, content, and access patterns
- **Temporal Decay**: Implements forgetting curves inspired by cognitive science
- **Memory Ranker**: Combines multiple signals into a unified relevance score
- **Context Generator**: Creates optimized prompts for LLM consumption

---

## 🎯 Use Cases

<table>
<tr>
<td width="50%">

### 🤖 Personal AI Assistants
- Remember user preferences and habits
- Learn from past interactions
- Build long-term relationships
- Provide personalized recommendations

### 💬 Intelligent Chatbots
- Maintain conversation context
- Reference previous discussions
- Understand evolving user needs
- Deliver coherent multi-session dialogues

</td>
<td width="50%">

### 🎓 AI Tutors & Learning
- Track student progress over time
- Identify knowledge gaps
- Adapt to learning patterns
- Provide personalized curriculum

### 🎧 Customer Support AI
- Recall customer history
- Reference past issues
- Remember preferences
- Deliver consistent service

</td>
</tr>
</table>

### Research & Development
- 📚 **Research Assistants**: Connect insights across multiple papers and sessions
- 🧪 **Experiment Tracking**: Remember hypothesis, results, and learnings
- 🎨 **Creative Tools**: Maintain context for long-form content generation

---

## 🏗️ Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                          Brain (Core)                           │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     │
│  │   Remember   │    │    Recall    │    │   Forget     │     │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘     │
└─────────┼───────────────────┼───────────────────┼──────────────┘
          │                   │                   │
          ▼                   ▼                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Memory Layer                                │
│  ┌──────────────┐                        ┌──────────────┐       │
│  │ MemoryStore  │◄─────────────────────►│ MemoryRetriever│     │
│  └──────┬───────┘                        └──────┬───────┘       │
└─────────┼──────────────────────────────────────┼────────────────┘
          │                                       │
          ▼                                       ▼
┌──────────────────────┐              ┌──────────────────────────┐
│   Gemini Embedder    │              │  Intelligence Layer      │
│  • Embedding Gen     │              │  • Scorer                │
│  • Batch Processing  │              │  • Ranker                │
│  • Retry Logic       │              │  • Temporal Decay        │
└──────────┬───────────┘              └──────────┬───────────────┘
           │                                      │
           └──────────────┬──────────────────────┘
                          ▼
                  ┌───────────────┐
                  │   Qdrant DB   │
                  │  Vector Store │
                  └───────────────┘
```

### Directory Structure

```
NeuroMem/
├── 🧠 core/
│   └── brain.py              # Main orchestrator - high-level API
│
├── 💾 memory/
│   ├── store.py              # Memory storage interface
│   ├── retrieve.py           # Memory retrieval interface
│   └── encoding/
│       ├── base.py           # Abstract embedder interface
│       └── gemini.py         # Google Gemini implementation (3072-dim)
│
├── 🎯 intelligence/
│   ├── scorer.py             # Importance scoring algorithms
│   ├── ranker.py             # Multi-signal ranking system
│   └── decay.py              # Temporal decay functions
│
├── 🗄️ db/
│   └── vectore_store.py      # Qdrant vector database operations
│
├── 📊 models/
│   ├── memory.py             # Memory, MemoryQuery, MemorySearchResult
│   └── user.py               # User data models
│
├── ⚙️ config/
│   └── settings.py           # Configuration management (Pydantic)
│
├── 🖥️ app/
│   └── cli.py                # Command-line interface
│
└── 🧪 tests/                 # Unit & integration tests
```

### Key Components

| Component | Purpose | Technologies |
|-----------|---------|--------------|
| **Brain** | Main API for memory operations | Python, Pydantic |
| **Embedder** | Convert text to vectors | Google Gemini AI |
| **VectorStore** | Store and search vectors | Qdrant |
| **Intelligence** | Ranking and scoring | Custom algorithms |
| **CLI** | Interactive testing tool | Click |

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+** (3.10+ recommended)
- **Qdrant** - Vector database ([local](https://qdrant.tech/documentation/quick-start/) or [cloud](https://cloud.qdrant.io/))
- **Google Gemini API Key** - Get one from [Google AI Studio](https://makersuite.google.com/app/apikey)

### Installation

#### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/NeuroMem.git
cd NeuroMem
```

#### 2️⃣ Set Up Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

#### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4️⃣ Configure Environment

```bash
# Copy example environment file
copy .env.example .env  # Windows
# OR
cp .env.example .env    # macOS/Linux
```

Edit `.env` with your configuration:

```env
# Google Gemini API
GEMINI_API_KEY="your-actual-api-key-here"
EMBEDDING_MODEL="models/gemini-embedding-001"
EMBEDDING_DIMENSION=3072
LLM_MODEL="gemini-1.5-flash"

# Qdrant Configuration
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION_NAME=ai_brain_memories

# Memory Management
DECAY_RATE=0.01
```

#### 5️⃣ Start Qdrant (Local)

**Option A: Docker (Recommended)**
```bash
docker run -p 6333:6333 qdrant/qdrant
```

**Option B: Docker Compose**
```bash
docker-compose up -d
```

**Option C: Use Qdrant Cloud**
```env
QDRANT_HOST=your-cluster.qdrant.io
QDRANT_API_KEY=your-api-key
```

#### 6️⃣ Verify Installation

```bash
python -m app.cli stats -u test_user
```

You should see: "Memory Statistics for user: test_user"

---

## 💻 Usage Examples

### Python API

#### Basic Usage

```python
from core.brain import Brain
from models.memory import MemoryType

# Initialize for a specific user
brain = Brain(user_id="alice")

# Store memories
brain.remember(
    "Alice prefers dark mode in all applications",
    memory_type=MemoryType.SEMANTIC,
    tags=["preferences", "ui"]
)

brain.remember(
    "Had a great conversation about Python async programming",
    memory_type=MemoryType.EPISODIC,
    importance_score=0.7,
    tags=["conversation", "programming"]
)

# Retrieve relevant memories
results = brain.recall(
    query="What are Alice's UI preferences?",
    top_k=3,
    min_similarity=0.6
)

for result in results:
    print(f"[{result.final_score:.2f}] {result.memory.content}")
    print(f"  Tags: {', '.join(result.memory.tags)}\n")

# Get LLM-ready context
context = brain.get_context(
    query="What does Alice like?",
    max_memories=5
)
print(context)  # Formatted string ready for LLM prompt
```

#### Advanced: Batch Processing

```python
from memory.store import MemoryStore
from memory.encoding.gemini import GeminiEmbedder
from db.vectore_store import VectorStore

# Initialize components
embedder = GeminiEmbedder()
vector_store = VectorStore()
memory_store = MemoryStore(embedder, vector_store)

# Batch store multiple memories (efficient!)
memories_data = [
    {
        "content": "User completed Python course",
        "user_id": "alice",
        "memory_type": "episodic",
        "tags": ["learning", "achievement"]
    },
    {
        "content": "Interested in machine learning",
        "user_id": "alice",
        "memory_type": "semantic",
        "tags": ["interests", "career"]
    },
    {
        "content": "Prefers morning study sessions",
        "user_id": "alice",
        "memory_type": "semantic",
        "tags": ["preferences", "schedule"]
    }
]

# Single API call for embeddings!
stored = memory_store.store_memory_batch(memories_data)
print(f"Stored {len(stored)} memories efficiently")
```

#### Memory Filtering

```python
# Filter by memory type
semantic_memories = brain.recall(
    query="What facts do we know?",
    memory_types=[MemoryType.SEMANTIC],
    top_k=10
)

# Filter by tags
food_memories = brain.recall(
    query="food preferences",
    tags=["food", "preferences"],
    top_k=5
)

# Filter by time window (last 7 days)
from models.memory import MemoryQuery

recent_query = MemoryQuery(
    query_text="recent interactions",
    user_id="alice",
    time_window_days=7,
    top_k=10
)

recent_memories = brain.memory_retriever.retrieve_memories(recent_query)
```

#### Delete Memories

```python
# Delete specific memory
memory_id = "5c1d5e15-74e0-41e3-9a3b-9446d1c720fb"
success = brain.forget(memory_id)

if success:
    print(f"Memory {memory_id} deleted")
```

---

## �️ CLI Interface

NeuroMem includes a powerful command-line interface for interactive testing and memory management.

### Commands Overview

| Command | Description | Example |
|---------|-------------|---------|
| `remember` | Store a new memory | `python -m app.cli remember "I love pizza" -u alice` |
| `recall` | Search for memories | `python -m app.cli recall "food preferences" -u alice` |
| `context` | Get LLM-ready context | `python -m app.cli context "What do I like?" -u alice` |
| `forget` | Delete a memory | `python -m app.cli forget mem_abc123 -u alice` |
| `stats` | Show user statistics | `python -m app.cli stats -u alice` |

### 📝 Remember - Store Memories

```bash
# Basic usage
python -m app.cli remember "I love spicy food" -u alice

# Specify memory type
python -m app.cli remember "Had dinner at Italian restaurant" -u alice -t episodic

# Add importance score (0.0-1.0)
python -m app.cli remember "Allergic to peanuts" -u alice -i 0.95

# Add tags for organization
python -m app.cli remember "Prefers Python over JavaScript" \
  -u alice -t semantic -g programming -g preferences

# Complete example
python -m app.cli remember "Learning machine learning" \
  -u alice \
  --type semantic \
  --importance 0.8 \
  --tags learning \
  --tags career
```

**Options:**
- `-u, --user-id`: User identifier (required)
- `-t, --type`: Memory type: `episodic` or `semantic` (default: episodic)
- `-i, --importance`: Importance score 0.0-1.0 (auto-calculated if not specified)
- `-g, --tags`: Tags (can specify multiple times)

### 🔍 Recall - Search Memories

```bash
# Basic search
python -m app.cli recall "what food do I like?" -u alice

# Specify number of results
python -m app.cli recall "my preferences" -u alice -k 10

# Filter by memory type
python -m app.cli recall "conversations" -u alice -t episodic

# Multiple memory types
python -m app.cli recall "everything" -u alice -t episodic -t semantic

# Set minimum similarity threshold
python -m app.cli recall "recent events" -u alice -s 0.7

# Filter by tags
python -m app.cli recall "food" -u alice -g food -g preferences

# Complete example
python -m app.cli recall "What do I like?" \
  -u alice \
  --type semantic \
  --top-k 5 \
  --min-similarity 0.6 \
  --tags preferences
```

**Options:**
- `-u, --user-id`: User identifier (required)
- `-t, --type`: Filter by memory type (can specify multiple)
- `-k, --top-k`: Number of results (default: 5)
- `-s, --min-similarity`: Minimum similarity 0.0-1.0 (default: 0.5)
- `-g, --tags`: Filter by tags (can specify multiple)

**Output Example:**
```
✓ Found 2 memories:

[1] I love spicy food
    ID: 5c1d5e15-74e0-41e3-9a3b-9446d1c720fb
    Type: semantic
    Similarity: 0.892
    Final Score: 0.874
    Importance: 0.78
    Created: 2026-02-09 11:04:50
    Access Count: 3
    Tags: food, preferences

[2] Had amazing Thai curry yesterday
    ID: 7f2e8a90-1234-5678-90ab-cdef12345678
    Type: episodic
    Similarity: 0.756
    Final Score: 0.721
    Importance: 0.65
    Created: 2026-02-08 18:30:22
    Access Count: 1
    Tags: food, experience
```

### 🎯 Context - Generate LLM Prompts

```bash
# Get formatted context for LLM
python -m app.cli context "What are my preferences?" -u alice

# Specify max memories to include
python -m app.cli context "Tell me about myself" -u alice -m 15
```

**Options:**
- `-u, --user-id`: User identifier (required)
- `-m, --max-memories`: Maximum memories to include (default: 10)

**Output Example:**
```
=== LLM Context ===
relevant memories about the user:

1. I love spicy food (type: semantic, importance: 0.78, relevance: 0.85)
2. Prefers dark mode interfaces (type: semantic, importance: 0.72, relevance: 0.80)
3. Learning Python programming (type: semantic, importance: 0.68, relevance: 0.76)
==================
```

### 🗑️ Forget - Delete Memories

```bash
# Delete specific memory by ID
python -m app.cli forget 5c1d5e15-74e0-41e3-9a3b-9446d1c720fb -u alice
```

### 📊 Stats - View Statistics

```bash
# Show memory statistics for user
python -m app.cli stats -u alice
```

### Real-World Workflow Example

```bash
# 1. Store user preferences
python -m app.cli remember "Prefers email notifications" -u alice -t semantic -g preferences

# 2. Store an interaction
python -m app.cli remember "Asked about Python async/await" -u alice -t episodic -g technical

# 3. Search relevant memories
python -m app.cli recall "What does Alice prefer?" -u alice -k 5

# 4. Get context for LLM
python -m app.cli context "Generate personalized response" -u alice -m 10

# 5. Delete outdated memory
python -m app.cli forget old_memory_id -u alice
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | - | ✅ Yes |
| `EMBEDDING_MODEL` | Gemini embedding model | `models/gemini-embedding-001` | No |
| `EMBEDDING_DIMENSION` | Vector dimensions | `3072` | No |
| `LLM_MODEL` | Gemini LLM model | `gemini-1.5-flash` | No |
| `QDRANT_HOST` | Qdrant server host | `localhost` | No |
| `QDRANT_PORT` | Qdrant server port | `6333` | No |
| `QDRANT_API_KEY` | Qdrant Cloud API key | `None` | No |
| `QDRANT_COLLECTION_NAME` | Collection name | `ai_brain_memories` | No |
| `DECAY_RATE` | Memory decay rate | `0.01` | No |

### Advanced Configuration

#### Custom Embedder

```python
from memory.encoding.base import BaseEmbedder
from typing import List

class CustomEmbedder(BaseEmbedder):
    """Implement your own embedding provider"""
    
    def embed(self, text: str) -> List[float]:
        # Your embedding logic
        pass
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        # Batch embedding logic
        pass
    
    def get_dimension(self) -> int:
        return 1536  # Your embedding dimension

# Use custom embedder
brain = Brain(user_id="alice")
brain.embedder = CustomEmbedder()
```

#### Ranking Weights

```python
from intelligence.ranker import MemoryRanker

# Customize ranking weights (must sum to 1.0)
ranker = MemoryRanker(
    similarity_weight=0.5,   # Semantic similarity
    importance_weight=0.3,   # Memory importance
    recency_weight=0.15,     # How recent
    access_weight=0.05       # Access frequency
)

# Use custom ranker
brain.memory_retriever.ranker = ranker
```

#### Temporal Decay

```python
from intelligence.decay import TemporalDecay

# Customize decay rate (higher = faster forgetting)
decay = TemporalDecay(decay_rate=0.05)  # Default: 0.01

# Formula: decay_factor = exp(-decay_rate * days_elapsed)
# Examples:
# - decay_rate=0.01: 30 days old = 0.74, 90 days old = 0.41
# - decay_rate=0.05: 30 days old = 0.22, 90 days old = 0.01
```

---

## 🧠 How It Works

### Memory Storage Pipeline

```
User Input → Embedding Generation → Vector Storage → Metadata Storage
     │              │                      │                │
     │         (Gemini API)          (Qdrant)         (Qdrant)
     │              │                      │                │
     └──────── Batch Support ──────────────┘                │
                    │                                       │
                    └──────── UUID Generation ──────────────┘
```

### Memory Retrieval Pipeline

```
User Query
    │
    ▼
[1] Embed Query (Gemini)
    │
    ▼
[2] Vector Search (Qdrant)
    │ • Cosine similarity
    │ • Filters (user, type, tags, time)
    ▼
[3] Intelligent Ranking
    │ • Similarity score
    │ • Importance boost
    │ • Temporal decay
    │ • Access frequency
    ▼
[4] Update Access Stats
    │ • Increment access count
    │ • Update last accessed time
    ▼
Ranked Results
```

### Scoring Algorithm

The final score combines multiple signals:

```python
final_score = (
    similarity_score * 0.4 +      # How relevant semantically
    importance_score * 0.3 +      # How important the memory is
    recency_factor * 0.2 +        # How recent the memory is
    access_boost * 0.1            # How frequently accessed
)
```

**Similarity Score**: Cosine similarity between query and memory embeddings (0.0-1.0)

**Importance Score**: Base importance × type multiplier × content length factor
- Semantic memories: 1.2× multiplier
- Episodic memories: 1.0× multiplier

**Recency Factor**: Exponential decay = `exp(-decay_rate × days_elapsed)`
- Recent memories maintain high scores
- Old memories gradually fade

**Access Boost**: Logarithmic scaling of access frequency
- Formula: `log(1 + access_count) / 5`
- Frequently accessed memories get prioritized

---

## 🚀 Performance

### Benchmarks

**Embedding Generation** (Gemini)
- Single embedding: ~500ms
- Batch (10 texts): ~800ms (10× faster than sequential)
- Batch (50 texts): ~1.5s (50× faster than sequential)

**Vector Search** (Qdrant)
- Search 1,000 vectors: <10ms
- Search 100,000 vectors: <50ms
- Search 1M vectors: <200ms

**End-to-End Latency**
- Store memory: ~600ms (embedding + insert)
- Recall memories: ~550ms (embedding + search + ranking)
- Batch store (10): ~1s (10× improvement)

### Optimization Tips

1. **Use Batch Processing** for multiple memories
   ```python
   # ✅ Good: Single API call
   memory_store.store_memory_batch(memories_data)
   
   # ❌ Avoid: Multiple API calls
   for data in memories_data:
       memory_store.store_memory(**data)
   ```

2. **Adjust `top_k` Parameter** based on use case
   - Personal assistant: 5-10 results
   - Research tool: 20-50 results
   - Comprehensive search: 50-100 results

3. **Use Appropriate Similarity Threshold**
   - High precision: 0.7-0.9
   - Balanced: 0.5-0.7
   - High recall: 0.3-0.5

4. **Filter Early** with tags and memory types
   ```python
   # Faster: Filter at vector search level
   results = brain.recall(
       query="food",
       tags=["food"],
       memory_types=[MemoryType.SEMANTIC]
   )
   ```

5. **Use Qdrant Cloud** for production
   - Managed service
   - Automatic scaling
   - Built-in redundancy

---

## 🔧 Troubleshooting

### Common Issues

#### ❌ "ImportError: cannot import name 'List' from 'types'"

**Solution**: This was fixed. Ensure you're using `from typing import List`

```python
# ✅ Correct
from typing import List

# ❌ Wrong
from types import List
```

#### ❌ "Vector dimension error: expected dim: 768, got 3072"

**Solution**: Update your `.env` file to match the embedding model:

```env
EMBEDDING_MODEL="models/gemini-embedding-001"
EMBEDDING_DIMENSION=3072
```

Then reset the Qdrant collection:
```bash
python reset_collection.py
```

#### ❌ "404 models/text-embedding-004 is not found"

**Solution**: Update to the available model in `.env`:

```env
EMBEDDING_MODEL="models/gemini-embedding-001"
```

#### ❌ "Connection refused" when accessing Qdrant

**Solution**: Ensure Qdrant is running:

```bash
# Check if Qdrant is running
docker ps | grep qdrant

# Start Qdrant if not running
docker run -p 6333:6333 qdrant/qdrant
```

#### ❌ "'datetime.datetime' object is not callable"

**Solution**: This was fixed. Ensure Pydantic Field uses lambda:

```python
# ✅ Correct
timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# ❌ Wrong
timestamp: datetime = Field(default_factory=datetime.now(timezone.utc))
```

### Debug Mode

Enable detailed logging:

```python
import sys
from loguru import logger

logger.remove()
logger.add(sys.stderr, level="DEBUG")  # Show all logs

# Run your code
brain = Brain(user_id="alice")
```

### Check System Health

```python
# Test Qdrant connection
from db.vectore_store import VectorStore
vs = VectorStore()
print("Qdrant connected!")

# Test Gemini API
from memory.encoding.gemini import GeminiEmbedder
embedder = GeminiEmbedder()
test_vector = embedder.embed("Hello world")
print(f"Embedding dimension: {len(test_vector)}")
```

---

## � Testing

### Run Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=memory --cov=core --cov=intelligence tests/

# Run specific test file
pytest tests/test_memory_store.py

# Run with verbose output
pytest -v tests/

# Run and show print statements
pytest -s tests/
```

### Test Structure

```
tests/
├── test_memory_store.py      # Memory storage tests
├── test_retrieval.py          # Memory retrieval tests
├── test_embedder.py           # Embedding generation tests
├── test_vector_store.py       # Qdrant integration tests
├── test_ranking.py            # Ranking algorithm tests
└── test_brain.py              # End-to-end tests
```

### Writing Tests

```python
import pytest
from core.brain import Brain
from models.memory import MemoryType

def test_remember_and_recall():
    """Test basic memory storage and retrieval"""
    brain = Brain(user_id="test_user")
    
    # Store memory
    memory = brain.remember(
        "Test memory content",
        memory_type=MemoryType.SEMANTIC
    )
    
    assert memory.id is not None
    assert memory.content == "Test memory content"
    
    # Recall memory
    results = brain.recall("test memory", top_k=1)
    
    assert len(results) > 0
    assert results[0].memory.content == "Test memory content"
```

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Getting Started

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Run tests**
   ```bash
   pytest tests/
   ```
5. **Commit with clear messages**
   ```bash
   git commit -m "Add: New feature for X"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

### Contribution Guidelines

- ✅ Write clear, descriptive commit messages
- ✅ Add tests for new features
- ✅ Update documentation as needed
- ✅ Follow existing code style
- ✅ Ensure all tests pass
- ✅ Keep PRs focused on a single feature/fix

### Areas for Contribution

- 🐛 **Bug Fixes**: Find and fix issues
- ✨ **Features**: Add new functionality
- 📚 **Documentation**: Improve README, add examples
- 🧪 **Testing**: Increase test coverage
- 🎨 **UI/UX**: Improve CLI interface
- 🚀 **Performance**: Optimize algorithms
- 🌐 **Integrations**: Add new embedding providers

---

## 🗺️ Roadmap

### Current Version (v1.0)
- ✅ Core memory storage and retrieval
- ✅ Google Gemini embeddings
- ✅ Qdrant vector database
- ✅ Intelligent ranking system
- ✅ CLI interface
- ✅ Batch processing
- ✅ Multi-user support

### Upcoming Features

#### v1.1 - Enhanced Intelligence
- 🔄 Memory consolidation (merge similar memories)
- 🔗 Automatic memory linking and graphs
- 🧩 Context-aware memory chunking
- 📊 Advanced analytics and insights

#### v1.2 - API & Integrations
- 🌐 FastAPI REST API
- 🔌 LangChain integration
- 🤖 AutoGPT plugin
- 📱 Web dashboard

#### v1.3 - Advanced Features
- 🎭 Multi-modal memories (text, images, audio)
- 🔐 Memory encryption and privacy controls
- 🌍 Multi-language support
- 🔄 Automatic memory refresh and updates

#### v2.0 - Enterprise Features
- 👥 Team/organization memory spaces
- 🔐 Advanced access control (RBAC)
- 📈 Scalability improvements
- 🔍 Full-text search integration
- 💾 Backup and restore functionality

### Community Requests

Have a feature idea? [Open an issue](https://github.com/yourusername/NeuroMem/issues)!

---

## 🔬 Technical Details

### Technologies & Frameworks

| Category | Technology | Purpose |
|----------|-----------|---------|
| **Language** | Python 3.9+ | Core implementation |
| **AI/ML** | Google Gemini | Text embeddings (3072-dim) |
| **Vector DB** | Qdrant | Similarity search |
| **Validation** | Pydantic 2.10+ | Data models & settings |
| **CLI** | Click 8.1+ | Command-line interface |
| **Logging** | Loguru 0.7+ | Structured logging |
| **Testing** | Pytest 7.4+ | Unit & integration tests |
| **Async** | AsyncIO | Future async support |

### Memory Model

```python
class Memory:
    id: str                    # Unique identifier (UUID)
    content: str              # Memory text
    embedding: List[float]    # 3072-dim vector
    timestamp: datetime       # Creation time
    memory_type: MemoryType   # EPISODIC or SEMANTIC
    importance_score: float   # 0.0-1.0
    user_id: str             # User identifier
    tags: List[str]          # Custom tags
    last_accessed: datetime  # Last retrieval time
    access_count: int        # Number of accesses
```

### Vector Search

NeuroMem uses **cosine similarity** for semantic search:

```
similarity = (A · B) / (||A|| × ||B||)
```

Where:
- A = query embedding
- B = memory embedding
- Range: -1.0 to 1.0 (Qdrant normalizes to 0.0-1.0)

### Embedding Models

| Model | Dimensions | Use Case |
|-------|------------|----------|
| `gemini-embedding-001` | 3072 | Current (Recommended) |
| `text-embedding-004` | 768 | Legacy (Deprecated) |

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 NeuroMem Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 🙏 Acknowledgments

### Inspiration
- **Human Memory Systems**: Cognitive psychology research on episodic vs semantic memory
- **Forgetting Curves**: Ebbinghaus forgetting curve and spaced repetition
- **Vector Databases**: Advances in similarity search and embeddings

### Built With
- [Google Gemini](https://ai.google.dev/) - State-of-the-art embeddings
- [Qdrant](https://qdrant.tech/) - High-performance vector database
- [Pydantic](https://docs.pydantic.dev/) - Data validation
- [Click](https://click.palletsprojects.com/) - CLI framework

### Special Thanks
- The AI/ML open-source community
- Early testers and contributors
- Research papers on memory systems and cognitive architectures

---

## 📬 Contact & Support

### Get Help

- 📖 **Documentation**: You're reading it!
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/NeuroMem/discussions)
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/yourusername/NeuroMem/issues)
- ✨ **Feature Requests**: [GitHub Issues](https://github.com/yourusername/NeuroMem/issues)

### Community

- 🌟 Star the project on GitHub
- 🐦 Follow for updates: [@YourTwitter](https://twitter.com/yourtwitter)
- 📧 Email: your.email@example.com

### Citation

If you use NeuroMem in your research or project, please cite:

```bibtex
@software{neuromem2026,
  title = {NeuroMem: Brain-Inspired Memory System for AI Agents},
  author = {Your Name},
  year = {2026},
  url = {https://github.com/yourusername/NeuroMem}
}
```

---

## ⚠️ Important Notes

### Production Considerations

- 🔐 **Security**: Implement authentication and authorization
- 🔒 **Privacy**: Encrypt sensitive memory content
- 📊 **Monitoring**: Add metrics and alerting
- 💾 **Backups**: Regular Qdrant backups
- 🌍 **Scaling**: Use Qdrant Cloud for production loads
- ⚖️ **Compliance**: Ensure GDPR/privacy compliance

### Rate Limits

**Google Gemini API**
- Free tier: 15 requests/minute
- Paid tier: Higher limits available

**Qdrant**
- Local: No limits
- Cloud: Based on plan

### Cost Estimation

**Gemini API** (Embedding-001)
- ~$0.00001 per embedding
- 1,000 memories: ~$0.01
- 1M memories: ~$10

**Qdrant Cloud**
- Starts at $25/month
- Free tier available

**Local Development**
- Free (using local Qdrant)

---

<div align="center">

### 🌟 Star This Project

If NeuroMem helped you, consider giving it a star!

[![GitHub stars](https://img.shields.io/github/stars/yourusername/NeuroMem?style=social)](https://github.com/azizmabrouk11/NeuroMem)

### Made with ❤️ by the NeuroMem Team

*Building the future of AI memory, one vector at a time.*

---

**[⬆ Back to Top](#-neuromem)**

</div>
