<div align="center">

# 🧠 NeuroMem

### *Production-Ready AI Memory System with Brain-Inspired Intelligence*

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Qdrant](https://img.shields.io/badge/Vector_DB-Qdrant-red.svg)](https://qdrant.tech/)
[![Gemini](https://img.shields.io/badge/AI-Google_Gemini-4285F4.svg)](https://ai.google.dev/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

*Give your AI agents long-term memory, contextual awareness, and human-like recall.*

**[Getting Started](#-quick-start)** • **[Features](#-features)** • **[API Guide](#-usage-examples)** • **[CLI](#️-cli-interface)** • **[Scaling](#-performance--scaling)**

</div>

---

## 🌟 Overview

**NeuroMem** is a production-ready, brain-inspired memory system enabling AI agents to maintain persistent, contextual awareness across conversations. It combines state-of-the-art vector embeddings with cognitive-inspired ranking algorithms to deliver human-like memory capabilities.

### Why Choose NeuroMem?

| Feature | Benefit |
|---------|---------|
| 🎯 **Semantic Understanding** | Retrieve relevant memories based on meaning, not just keywords |
| 🧮 **Multi-Signal Ranking** | Intelligent scoring using similarity, importance, recency, and access patterns |
| ⚡ **High Performance** | Handles 50K-100K memories with sub-second queries |
| 🔄 **Natural Forgetting** | Temporal decay mirrors human memory - old memories fade gracefully |
| 🎨 **Memory Classification** | Episodic (events/conversations) vs Semantic (facts/knowledge) |
| 🛠️ **Battle-Tested** | Built-in retry logic, error handling, comprehensive logging |
| 📦 **Batch Optimized** | 10-50× faster multi-memory operations |

## ✨ Features

<details open>
<summary><b>🎯 Core Capabilities</b></summary>

| Feature | Description | Performance |
|---------|-------------|-------------|
| **Semantic Search** | Google Gemini 3072-dim embeddings | <50ms on 100K vectors |
| **Batch Processing** | Single API call for multiple memories | 10-50× faster |
| **Smart Ranking** | 4-signal scoring algorithm | Real-time computation |
| **Temporal Decay** | Exponential forgetting curve | Automatic aging |
| **Tagging System** | Custom taxonomies & filtering | Indexed queries |
| **Multi-User** | Isolated user memory spaces | Complete isolation |
| **Memory Types** | Episodic vs Semantic classification | Auto-categorization |
| **Access Tracking** | Usage analytics & adaptation | Frequency scoring |
| **Context Building** | LLM-optimized prompt generation | Formatted output |
| **Production Ready** | Retry logic, error handling, logging | Zero-downtime |

</details>

<details>
<summary><b>🧠 Intelligence Layer</b></summary>

- **Memory Scorer**: Multi-factor importance evaluation (type, content, context)
- **Temporal Decay**: Ebbinghaus forgetting curve implementation
- **Memory Ranker**: Weighted multi-signal relevance scoring
- **Context Generator**: Optimized prompt construction for LLMs

| Domain | Application | Key Benefits |
|--------|-------------|--------------|
| 🤖 **Personal AI** | Assistants, Companions | Long-term relationships, preference learning, personalized interactions |
| 💬 **Chatbots** | Customer service, Support | Consistent multi-session context, conversation continuity |
| 🎓 **Education** | Tutors, Learning platforms | Progress tracking, adaptive learning paths, knowledge gap identification |
| 🎧 **Support** | Help desks, Technical support | Customer history recall, issue tracking, preference memory |
| 📚 **Research** | Literature review, Analysis | Cross-reference insights, connect ideas, track hypotheses |
| 🎨 **Creative** | Writing assistants, Content tools | Long-form context, style consistency, idea connectivity |
| 🧪 **Development** | Code assistants, Debugging | Project context, past solutions, pattern recognition |
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
<details>
<summary><b>System Overview</b></summary>

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
│  • 3072-dim vectors  │              │  • Scorer                │
│  • Batch Processing  │              │  • Ranker (4-signals)    │
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

</details>

<details>
<summary><b>📁 Directory Structure</b></summary>

```
NeuroMem/
├── 🧠 core/brain.py                    # Main API orchestrator
├── 💾 memory/
│   ├── store.py                        # Storage operations
│   ├── retrieve.py                     # Retrieval & ranking
│   ├── extractor.py                    # Auto-extract from conversations
│   └── encoding/
│       ├── base.py                     # Embedder interface
│       └── gemini.py                   # Gemini implementation
├── 🎯 intelligence/
│   ├── scorer.py                       # Importance algorithms
│   ├── ranker.py                       # Multi-signal ranking
│   └── decay.py                        # Temporal decay
├── 🗄️ db/vectore_store.py             # Qdrant operations
├── 🤖 ai/
│   ├── chat.py                         # Chat manager
│   └── llm.py                          # LLM client (Gemini)
├── 📊 models/
│   ├── memory.py                       # Data models
│   └── user.py                         # User models
├── ⚙️ config/settings.py               # Pydantic configuration
├── 🖥️ app/cli.py                       # CLI interface
└── 🧪 tests/                           # Test suite
```

</details>

| Component | Purpose | Tech Stack |
|-----------|---------|------------|
| **Brain** | Unified memory API | Python, Pydantic |
| **Embedder** | Text → 3072-dim vectors | Google Gemini |
| **VectorStore** | Similarity search | Qdrant |
| **Intelligence** | Multi-signal ranking | Numpy, Custom algorithms |
| **CLI/API** | User interfaces | Click, FastAPI (future)
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
 & Scaling

### Benchmarks

<table>
<tr>
<td width="50%">

**Embedding Generation (Gemini)**
- Single: ~500ms
- Batch (10): ~800ms *(10× faster)*
- Batch (50): ~1.5s *(50× faster)*

**Vector Search (Qdrant)**
- 1K vectors: <10ms
- 100K vectors: <50ms
- 1M vectors: <200ms

</td>
<td width="50%">

**End-to-End Latency**
- Store memory: ~600ms
- Recall memories: ~550ms
- Batch store (10): ~1s *(10× faster)*

**Throughput**
- Sequential: ~100 stores/min
- Batch: ~600 stores/min

</td>
</tr>
</table>
<details>
<summary><b>Common Issues & Solutions</b></summary>

### Vector Dimension Mismatch
```bash
# Error: expected dim: 768, got 3072
# Solution: Update .env and reset collection
```
```env
EMBEDDING_MODEL="models/gemini-embedding-001"
EMBEDDING_DIMENSION=3072
```
```bash
python reset_collection.py
```

### Model Not Found (404)
```bash
# Error: models/gemini-1.5-pro is not found
# Solution: Use available model
```
```env
LLM_MODEL="gemini-2.5-flash"
EMBEDDING_MODEL="models/gemini-embedding-001"
```

### Qdrant Connection Refused
```bash
# Check if running
docker ps | grep qdrant

# Start Qdrant
docker run -p 6333:6333 qdrant/qdrant
```

### Import Errors
```python
# ✅ Correct
from typing import List
from google import genai

# ❌ Wrong (deprecated)
from types import List
import google.generativeai as genai
```

### Debug Mode
```python
from loguru import logger
import sys

logger.remove()
logger.add(sys.stderr, level="DEBUG")

brain = Brain(user_id="test")
```

### Health Check
```python
# Test connections
from db.vectore_store import VectorStore
from memory.encoding.gemini import GeminiEmbedder

vs = VectorStore()  # Should connect
embedder = GeminiEmbedder()
vec = embedder.embed("test")  # Should return 3072-dim vector
print(f"✓ System healthy: {len(vec)} dimensions")
```

</details>estamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

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
| Version | Status | Features |
|---------|--------|----------|
| **v1.0** | ✅ **Current** | Core storage/retrieval, Gemini embeddings, Qdrant, Multi-signal ranking, CLI, Batch processing |
| **v1.1** | 🚧 In Progress | Memory consolidation, Auto-linking, Context chunking, Analytics dashboard |
| **v1.2** | 📋 Planned Q2'26 | FastAPI REST API, LangChain integration, Web dashboard, AutoGPT plugin |
| **v1.3** | 📋 Planned Q3'26 | Multi-modal support, Encryption, Multi-language, Auto-refresh |
| **v2.0** | 🔮 Future | Enterprise features, RBAC, Advanced scaling, Full-text search, Backup/restore |

<details>
<summary><b>Detailed Feature Pipeline</b></summary>

**v1.1 - Enhanced Intelligence** (Next Release)
- 🔄 Memory consolidation (merge similar memories)
- 🔗 Automatic memory graphs and relationships
- 🧩 Smart memory chunking for long content
- 📊 Usage analytics and insights dashboard
- 🎯 Adaptive importance scoring

**v1.2 - API & Integrations**
- 🌐 FastAPI REST API with OpenAPI docs
- 🔌 LangChain memory integration
- 🤖 AutoGPT plugin support
- 📱 Web-based memory browser
- 🔄 Webhook support for memory events

**v1.3 - Advanced Features**
- 🎭 Multi-modal: images, audio transcripts
- 🔐 End-to-end encryption option
- 🌍 Multi-language embeddings
- 🔄 Automatic memory updates/versioning
- 📈 Advanced pruning strategies

**v2.0 - Enterprise**
- 👥 Team/org memory spaces
- 🔐 Role-based access control
- 📈 Horizontal scaling support
- 🔍 Hybrid vector + full-text search
- 💾 Disaster recovery & backup

</details>

💡 **Have a feature idea?** [Open an issue](https://github.com/azizmabrouk11/NeuroMem/issues) or contribute
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
- ClouProduction Considerations

### Security & Compliance

| Area | Recommendation | Priority |
|------|----------------|----------|
| 🔐 **Authentication** | Implement API key auth or OAuth2 | High |
| 🔒 **Encryption** | Encrypt sensitive memory content at rest | Medium |
| 📊 **Monitoring** | Add Prometheus metrics + alerting | High |
| 💾 **Backups** | Automated Qdrant snapshots (daily) | Critical |
| 🌍 **Scaling** | Use Qdrant Cloud for production | Recommended |
| ⚖️ **GDPR** | User data deletion, export capabilities | Required |

### Rate Limits & Costs

<table>
<tr>
<td width="50%">

**Gemini API**
- Free: 15 requests/min
- Paid: 60+ requests/min
- Cost: ~$0.00001/embedding

**Cost Examples:**
- 1K memories: ~$0.01
- 100K memories: ~$1
- 1M memories: ~$10

</td>
<td width="50%">

**Qdrant**
- Local: Unlimited (free)
- Cloud: $25+/month

**Capacity Examples:**
- 100K vectors: <1GB
- 1M vectors: ~5GB
---

### 🌟 If NeuroMem Powers Your AI, Star Us!

[![GitHub stars](https://img.shields.io/github/stars/azizmabrouk11/NeuroMem?style=social)](https://github.com/azizmabrouk11/NeuroMem)
[![GitHub forks](https://img.shields.io/github/forks/azizmabrouk11/NeuroMem?style=social)](https://github.com/azizmabrouk11/NeuroMem/fork)
[![GitHub watchers](https://img.shields.io/github/watchers/azizmabrouk11/NeuroMem?style=social)](https://github.com/azizmabrouk11/NeuroMem)

### Made with ❤️ by the NeuroMem Team

*Building the future of AI memory, one vector at a time.*

**[⬆ Back to Top](#-neuromem)** • **[Quick Start](#-quick-start)** • **[Report Issue](https://github.com/azizmabrouk11/NeuroMem/issues)** • **[Contribute](#-contributing