<div align="center">

# 🧠 NeuroMem

### *AI Memory System with Human-Like Intelligence*

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Qdrant](https://img.shields.io/badge/Vector_DB-Qdrant-red.svg)](https://qdrant.tech/)
[![Gemini](https://img.shields.io/badge/AI-Google_Gemini-4285F4.svg)](https://ai.google.dev/)
[![Ollama](https://img.shields.io/badge/AI-Ollama-000000.svg)](https://ollama.ai/)

*Give your AI agents persistent memory, contextual awareness, and intelligent recall*

[Quick Start](#-quick-start) • [Features](#-features) • [Demo](#-interactive-demo) • [Documentation](#-documentation) • [API](#-python-api)

---

</div>

## 📖 What is NeuroMem?

**NeuroMem** is a production-ready memory system for AI agents that mimics human memory. It enables your AI to remember conversations, learn preferences, and build long-term relationships with users.

### 🔌 Choose Your AI Backend

NeuroMem supports both cloud and self-hosted AI providers:

| Provider | Cost | Privacy | Speed | Best For |
|----------|------|---------|-------|----------|
| **🌩️ Gemini** | ~$1-2/month | Cloud | ⚡⚡⚡ Fast | Production, high-quality embeddings |
| **🏠 Ollama** | $0 (free) | 100% Local | ⚡⚡ Good | Privacy-first, cost-sensitive, development |
| **🔀 Hybrid** | ~$1/month | Mixed | ⚡⚡⚡ Best | Gemini embeddings + Ollama LLM |

**Recommendation:** Start with Ollama (free, private) for development, upgrade to Gemini for production if needed.

### ✨ Key Highlights

```python
# Simple, powerful API
brain = Brain(user_id="alice")
brain.remember("I love spicy food", tags=["preference", "food"])
memories = brain.recall("What does Alice like to eat?")
```

| Feature | Description |
|---------|-------------|
| 🎯 **Semantic Search** | Find relevant memories by meaning, not keywords (768-3072 dim embeddings) |
| 🧠 **Smart Ranking** | Multi-signal scoring: similarity + importance + recency + frequency |
| ⚡ **Fast & Scalable** | Sub-second queries with 50K-100K memories |
| 🔄 **Natural Forgetting** | Temporal decay - memories fade like human memory |
| 💬 **Chat Integration** | Built-in conversational AI with auto-memory extraction |
| 📦 **Batch Processing** | 10-50× faster operations with bulk API calls |
| 🎭 **Memory Types** | Episodic (events) vs Semantic (facts) classification |
| 🤖 **Dual LLM Support** | Choose between Google Gemini (cloud) or Ollama (self-hosted) |
| 🧪 **Evaluation Suite** | Comprehensive testing framework for retrieval, dedup & performance |
| 🛠️ **Production Ready** | Retry logic, error handling, comprehensive logging |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- [Qdrant](https://qdrant.tech/) (local or cloud)
- **Choose your AI provider:**
  - [Google Gemini API key](https://makersuite.google.com/app/apikey) (cloud, free tier available)
  - **OR** [Ollama](https://ollama.ai/) (self-hosted, fully free & private)

### Installation (5 minutes)

#### Option 1: Docker Compose (Recommended)

```bash
# 1. Clone repository
git clone https://github.com/azizmabrouk11/NeuroMem.git
cd NeuroMem

# 2. Start services (Ollama + Qdrant)
docker-compose up -d

# 3. Pull embedding model
docker exec -it ollama ollama pull nomic-embed-text
docker exec -it ollama ollama pull llama3.2

# 4. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 5. Install dependencies
pip install -r requirements.txt

# 6. Configure environment (Ollama default)
cp .env.example .env
# Edit .env if using Gemini

# 7. Test it!
python -m app.cli remember "I love Python" -u demo
python -m app.cli recall "programming" -u demo
```

#### Option 2: Manual Setup

```bash
# 1. Clone repository
git clone https://github.com/azizmabrouk11/NeuroMem.git
cd NeuroMem

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start Qdrant
docker run -p 6333:6333 qdrant/qdrant

# 5. For Ollama (self-hosted):
# Install from https://ollama.ai/ then:
ollama pull nomic-embed-text
ollama pull llama3.2

# OR for Gemini (cloud):
# Get API key from https://makersuite.google.com/app/apikey

# 6. Configure .env
cp .env.example .env
# Edit with your settings

# 7. Test it!
python -m app.cli remember "I love Python" -u demo
python -m app.cli recall "programming" -u demo
```

### Environment Setup

#### For Ollama (Self-Hosted - Default)

```env
# .env file
# LLM Provider
llm_provider=ollama
ollama_base_url=http://localhost:11434/v1
ollama_model=llama3.2

# Embedding Provider
embedding_provider=ollama
ollama_embedding_model=nomic-embed-text  # 768-dim, recommended

# Qdrant
qdrant_host=localhost
qdrant_port=6333
qdrant_collection_name=ai_brain_memories

# Memory Settings
decay_rate=0.01
similarity_threshold=0.7
```

#### For Gemini (Cloud)

```env
# .env file
# Gemini API
gemini_api_key=your-api-key-here
embedding_model=models/gemini-embedding-001
llm_model=gemini-2.5-flash

# Provider Selection
llm_provider=gemini
embedding_provider=gemini

# Qdrant
qdrant_host=localhost
qdrant_port=6333
qdrant_collection_name=ai_brain_memories

# Memory Settings
decay_rate=0.01
similarity_threshold=0.7
```

#### For Hybrid (Gemini Embeddings + Ollama LLM)

```env
# Best of both: Gemini's powerful embeddings + local LLM
embedding_provider=gemini
gemini_api_key=your-api-key-here
embedding_model=models/gemini-embedding-001

llm_provider=ollama
ollama_base_url=http://localhost:11434/v1
ollama_model=llama3.2
```

---

## 🎮 Interactive Demo

### Conversational Chat with Memory

```bash
python -m app.cli chat -u alice
```

```
💬 Memory Chat (User: alice)

You: Hi! I really love spicy Thai food
Assistant: Great to know! I'll remember your preference for spicy Thai cuisine.

You: What kind of food do I like?
Assistant: Based on our conversation, you love spicy Thai food!
```

The chat system automatically:
- 🔍 Retrieves relevant memories
- 💬 Generates contextual responses
- 📝 Extracts and stores new memories
- 🧠 Learns user preferences over time

---

## 🏗️ Architecture

<details open>
<summary><b>System Design</b></summary>

```
┌──────────────────────────────────────────────────────────────┐
│                       🧠 Brain (Core API)                    │
│                                                              │
│     remember()          recall()          forget()           │
│         │                  │                  │              │
└─────────┼──────────────────┼──────────────────┼──────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌──────────────────────────────────────────────────────────────┐
│                    💾 Memory Layer                           │
│                                                              │
│   MemoryStore ◄──────────────────────► MemoryRetriever      │
│   • Store memories                     • Search vectors      │
│   • Batch insert                       • Rank results        │
│   • Auto-extract                       • Update stats        │
└───────┬────────────────────────────────────────┬─────────────┘
        │                                        │
        ▼                                        ▼
┌──────────────────┐                  ┌──────────────────────┐
│  🤖 Gemini API   │                  │  🎯 Intelligence      │
│                  │                  │                      │
│  • Embeddings    │                  │  • Scorer           │
│    (3072-dim)    │                  │  • Ranker           │
│  • LLM           │                  │  • Temporal Decay   │
│  • Batch support │                  │  • Access tracking  │
└──────────────────┘                  └──────────────────────┘
        │                                        │
        └────────────────┬───────────────────────┘
                         ▼
                ┌─────────────────┐
                │  🗄️ Qdrant DB   │
                │                 │
                │  Vector Storage │
                │  Cosine Search  │
                └─────────────────┘
```

</details>

### Project Structure

```
NeuroMem/
├── 🧠 core/
│   └── brain.py              # Main API - remember(), recall(), forget()
│
├── 💾 memory/
│   ├── store.py              # Memory storage & batch operations
│   ├── retrieve.py           # Search & ranking
│   ├── extractor.py          # Auto-extract from conversations
│   └── encoding/
│       ├── base.py           # Embedder interface
│       ├── gemini.py         # Gemini implementation (3072-dim)
│       └── ollama.py         # Ollama implementation (768/1024/384-dim)
│
├── 🎯 intelligence/
│   ├── scorer.py             # Importance scoring
│   ├── ranker.py             # Multi-signal ranking (4 factors)
│   └── decay.py              # Temporal decay function
│
├── 🤖 ai/
│   ├── chat.py               # Conversational chat manager
│   └── llm.py                # LLM client (Ollama/Gemini)
│
├── 🗄️ db/
│   └── vectore_store.py      # Qdrant operations
│
├── 📊 models/
│   ├── memory.py             # Memory data models
│   └── user.py               # User models
│
├── 🧪 evaluation/
│   ├── run_eval.py           # Run all evaluations
│   ├── evaluators/
│   │   ├── eval_retrieval.py # Retrieval quality metrics
│   │   ├── eval_dedup.py     # Deduplication testing
│   │   └── eval_performance.py # Latency benchmarks
│   ├── reports/
│   │   └── report_generator.py # Generate evaluation reports
│   └── data/
│       ├── test_cases.json   # Test scenarios
│       └── results/          # Evaluation results
│
├── ⚙️ config/
│   └── settings.py           # Configuration (Pydantic)
│
└── 🖥️ app/
    └── cli.py                # Command-line interface
```

---

## 💻 Python API

### Basic Usage

```python
from core.brain import Brain
from models.memory import MemoryType

# Initialize for a user
brain = Brain(user_id="alice")

# Store memories
brain.remember(
    "Alice is a software engineer who loves Python",
    memory_type=MemoryType.SEMANTIC,
    importance_score=0.8,
    tags=["profession", "interests"]
)

# Retrieve memories
results = brain.recall(
    query="What does Alice do for work?",
    top_k=5,
    min_similarity=0.6
)

for result in results:
    print(f"[Score: {result.final_score:.2f}] {result.memory.content}")
    print(f"  Tags: {', '.join(result.memory.tags)}")
```

### Conversational Chat

```python
from ai.chat import ChatManager

# Initialize chat with memory
chat = ChatManager(
    user_id="alice",
    system_instruction="You are a helpful AI assistant with long-term memory."
)

# Have a conversation
response = chat.chat("I'm learning machine learning")
print(response)  # AI remembers this automatically

response = chat.chat("What am I learning?")
print(response)  # "You're learning machine learning!"
```

### Batch Operations (Fast!)

```python
# Batch store - single API call for embeddings
memories_data = [
    {"content": "User completed Python course", "user_id": "alice", "tags": ["learning"]},
    {"content": "Interested in AI", "user_id": "alice", "tags": ["interests"]},
    {"content": "Prefers morning work", "user_id": "alice", "tags": ["schedule"]}
]

stored = brain.memory_store.store_memory_batch(memories_data)
print(f"Stored {len(stored)} memories in ~1 second!")
```

### Advanced Filtering

```python
from models.memory import MemoryQuery

# Filter by memory type
semantic_only = brain.recall(
    "user facts",
    memory_types=[MemoryType.SEMANTIC],
    top_k=10
)

# Filter by tags
food_memories = brain.recall(
    "cuisine preferences",
    tags=["food", "preferences"]
)

# Time-based filtering (last 7 days)
query = MemoryQuery(
    query_text="recent activities",
    user_id="alice",
    time_window_days=7
)
recent = brain.memory_retriever.retrieve_memories(query)
```

### Get LLM Context

```python
# Get formatted context for LLM prompts
context = brain.get_context(
    query="What should I know about Alice?",
    max_memories=10
)

# Use in your prompts
prompt = f"""
{context}

Based on what you know, suggest a personalized project for Alice.
"""
```

---

## 🖥️ CLI Interface

### Commands

| Command | Description | Example |
|---------|-------------|---------|
| `remember` | Store a memory | `python -m app.cli remember "text" -u alice` |
| `recall` | Search memories | `python -m app.cli recall "query" -u alice` |
| `context` | Get LLM context | `python -m app.cli context "query" -u alice` |
| `chat` | Interactive chat | `python -m app.cli chat -u alice` |
| `forget` | Delete memory | `python -m app.cli forget <id> -u alice` |
| `stats` | View statistics | `python -m app.cli stats -u alice` |

### Examples

```bash
# Store a memory
python -m app.cli remember "I love spicy food" -u alice \
  -t semantic \
  -i 0.8 \
  -g food -g preferences

# Search memories
python -m app.cli recall "What food do I like?" -u alice \
  -k 5 \
  -s 0.7 \
  -t semantic

# Get LLM-ready context
python -m app.cli context "Tell me about Alice" -u alice -m 10

# Interactive chat with memory
python -m app.cli chat -u alice

# View statistics
python -m app.cli stats -u alice
```

### Sample Output

```
✓ Found 3 memories:

[1] I love spicy food
    Type: semantic | Score: 0.89 | Importance: 0.80
    Created: 2026-02-11 10:30:00
    Tags: food, preferences

[2] Had amazing Thai curry yesterday
    Type: episodic | Score: 0.76 | Importance: 0.65
    Created: 2026-02-10 18:45:00
    Tags: food, experience

[3] Allergic to peanuts
    Type: semantic | Score: 0.72 | Importance: 0.95
    Created: 2026-02-09 09:15:00
    Tags: health, allergy
```

---

## 🛠️ Utility Scripts

NeuroMem includes helpful utility scripts for common tasks:

### Reset Collection

When changing embedding models or dimensions, reset the Qdrant collection:

```bash
python utils/reset_collection.py
```

This deletes the existing collection and allows it to be recreated with the correct dimensions on next use.

### Test Embeddings

Verify your embedding provider is working correctly:

```bash
# Test Ollama embeddings
python utils/test_ollama_embed.py

# Test Gemini embeddings (legacy)
python utils/check_dim.py
```

### Debug Utilities

```bash
# Test deduplication in isolation
python utils/test_dedup_only.py

# Debug deduplication evaluation
python utils/debug_dedup_eval.py

# Manual deduplication testing
python utils/dedup_test_manually.py
```

### Common Tasks

```bash
# Switch from Gemini to Ollama
# 1. Update .env
echo "embedding_provider=ollama" >> .env
echo "ollama_embedding_model=nomic-embed-text" >> .env

# 2. Reset collection (dimensions changed: 3072 → 768)
python utils/reset_collection.py

# 3. Test
python -m app.cli remember "test" -u alice
python -m app.cli recall "test" -u alice
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `embedding_provider` | Embedding provider (`ollama` or `gemini`) | `ollama` | Yes |
| `llm_provider` | LLM provider (`ollama` or `gemini`) | `ollama` | Yes |
| **Gemini Settings** | | | |
| `gemini_api_key` | Google Gemini API key | - | If using Gemini |
| `embedding_model` | Gemini embedding model | `models/gemini-embedding-001` | No |
| `llm_model` | Gemini LLM model | `gemini-2.5-flash` | No |
| **Ollama Settings** | | | |
| `ollama_base_url` | Ollama API base URL | `http://localhost:11434/v1` | No |
| `ollama_model` | Ollama LLM model | `llama3.2` | No |
| `ollama_embedding_model` | Ollama embedding model | `nomic-embed-text` | No |
| **Qdrant Settings** | | | |
| `qdrant_host` | Qdrant host | `localhost` | No |
| `qdrant_port` | Qdrant port | `6333` | No |
| `qdrant_api_key` | Qdrant Cloud key | `None` | No |
| `qdrant_collection_name` | Collection name | `ai_brain_memories` | No |
| **Memory Settings** | | | |
| `decay_rate` | Memory decay rate | `0.01` | No |
| `similarity_threshold` | Min similarity score | `0.7` | No |
| `importance_threshold` | Min importance score | `0.3` | No |
| `max_working_memory` | Max memories in context | `10` | No |

#### Popular Ollama Embedding Models

| Model | Dimensions | Speed | Quality | Use Case |
|-------|------------|-------|---------|----------|
| `nomic-embed-text` | 768 | ⚡⚡⚡ Fast | ⭐⭐⭐ Good | **Recommended** for most use cases |
| `mxbai-embed-large` | 1024 | ⚡⚡ Medium | ⭐⭐⭐⭐ Excellent | High-quality retrieval |
| `all-minilm` | 384 | ⚡⚡⚡⚡ Very Fast | ⭐⭐ Fair | Simple tasks, low resources |
| `llama3.1` | Variable | ⚡ Slower | ⭐⭐⭐⭐⭐ Best | Research, highest quality |

### Custom Configuration

```python
from intelligence.ranker import MemoryRanker
from intelligence.decay import TemporalDecay

# Customize ranking weights (must sum to 1.0)
ranker = MemoryRanker(
    similarity_weight=0.5,   # Semantic similarity
    importance_weight=0.3,   # Memory importance
    recency_weight=0.15,     # How recent
    access_weight=0.05       # Access frequency
)

# Customize temporal decay
decay = TemporalDecay(decay_rate=0.02)  # Faster forgetting

# Apply to brain
brain.memory_retriever.ranker = ranker
```

---

## 🚀 Performance & Scaling

### Benchmarks

| Operation | Latency | Throughput |
|-----------|---------|------------|
| Single embedding | ~500ms | - |
| Batch (10) embeddings | ~800ms | **10× faster** |
| Batch (50) embeddings | ~1.5s | **50× faster** |
| Vector search (100K) | <50ms | - |
| End-to-end recall | ~550ms | - |
| Batch store (10) | ~1s | ~600/min |

### Capacity & Stability

| Scale | Memory Count | Query Time | Status | Use Case |
|-------|-------------|------------|--------|----------|
| **Small** | 0-10K | <100ms | ✅ Excellent | POC, Testing |
| **Medium** | 10K-100K | 100-500ms | ✅ **Recommended** | **Production** |
| **Large** | 100K-500K | 0.5-2s | ⚠️ Good | Enterprise (with optimization) |
| **Very Large** | 500K-2M | 2-10s | ⚠️ Fair | Requires architecture changes |

> **💡 Production Sweet Spot:** 50K-100K memories for optimal performance

### Optimization Tips

<details>
<summary><b>Best Practices</b></summary>

```python
# ✅ DO: Use batch operations
memory_store.store_memory_batch(memories_data)

# ❌ DON'T: Loop with single operations
for data in memories_data:
    memory_store.store_memory(**data)

# ✅ DO: Filter early
brain.recall("food", tags=["food"], memory_types=[MemoryType.SEMANTIC])

# ✅ DO: Set appropriate top_k
# Personal assistant: 5-10
# Research tool: 20-50
# Comprehensive: 50-100

# ✅ DO: Use Qdrant Cloud for production
# Managed, scalable, redundant
```

**Similarity Thresholds:**
- High precision: `0.7-0.9` (strict matches)
- Balanced: `0.5-0.7` (recommended)
- High recall: `0.3-0.5` (broad matches)

</details>

### Scaling Beyond 100K

For large deployments (>100K memories):

```python
# Add to config/settings.py
class Settings(BaseSettings):
    max_active_memories: int = 100_000
    memory_cleanup_days: int = 90
    max_query_results: int = 100
    enable_memory_archival: bool = True
```

**Enterprise Options:**
- PostgreSQL + pgvector migration
- Memory archival system
- Redis caching layer
- Qdrant Cloud auto-scaling

---

## 🧠 How It Works

### Intelligent Ranking

NeuroMem uses a sophisticated 4-signal scoring algorithm:

```python
final_score = (
    similarity_score * 0.4 +     # Semantic relevance
    importance_score * 0.3 +     # Memory importance
    recency_factor * 0.2 +       # How recent (decay)
    access_boost * 0.1           # Usage frequency
)
```

**Components:**

1. **Similarity** (0.0-1.0): Cosine similarity between query and memory embeddings
2. **Importance** (0.0-1.0): Base score × type multiplier × content factor
3. **Recency**: Exponential decay `exp(-decay_rate × days_elapsed)`
4. **Access**: Logarithmic boost `log(1 + access_count) / 5`

### Memory Flow

```
┌─────────────┐
│ User Input  │
└──────┬──────┘
       │
       ▼
┌──────────────────────┐
│ Embed with Gemini    │  (~500ms)
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Vector Search        │  (<50ms for 100K)
│ (Qdrant)             │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Intelligent Ranking  │  (real-time)
│ • Similarity         │
│ • Importance         │
│ • Recency            │
│ • Access frequency   │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Update Access Stats  │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Return Ranked Results│
└──────────────────────┘
```

---

## 🎯 Use Cases

| Industry | Application | Benefits |
|----------|-------------|----------|
| 🤖 **Personal AI** | Assistants, Companions | Long-term relationships, preference learning |
| 💬 **Customer Support** | Service bots, Help desks | Customer history, consistent experience |
| 🎓 **Education** | Tutors, Learning platforms | Progress tracking, adaptive paths |
| 📚 **Research** | Literature tools, Analysis | Cross-reference, connect ideas |
| 🎨 **Creative** | Writing assistants, Content tools | Context consistency, idea connectivity |
| 🧪 **Development** | Code assistants, Debugging | Project context, solution memory |
| 🏥 **Healthcare** | Patient assistants, Care management | Medical history, preference memory |

---

## 🔧 Troubleshooting

<details>
<summary><b>Common Issues & Solutions</b></summary>

### Vector Dimension Mismatch
```bash
Error: expected dim: 768, got 3072
```
**Solution:**
```env
# Make sure embedding dimensions match your model
# For Ollama with nomic-embed-text (768):
embedding_provider=ollama
ollama_embedding_model=nomic-embed-text

# For Gemini (3072):
embedding_provider=gemini
embedding_model=models/gemini-embedding-001
```
```bash
# Reset collection when changing embedding models
python utils/reset_collection.py
```

### Ollama Connection Error
```bash
Error: Connection refused to localhost:11434
```
**Solution:**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not, start Ollama service or:
docker-compose up -d ollama

# Pull required models
ollama pull nomic-embed-text
ollama pull llama3.2
```

### Model Not Found (404)
```bash
Error: models/gemini-1.5-pro is not found
```
**Solution:**
```env
llm_model=gemini-2.5-flash
```

### Qdrant Connection Refused
```bash
# Check if Qdrant is running
docker ps | grep qdrant

# Start if not running
docker-compose up -d qdrant
# OR
docker run -p 6333:6333 qdrant/qdrant
```

# Start if not running
docker run -p 6333:6333 qdrant/qdrant
```

### Import Errors
```python
# ✅ Correct (new SDK)
from google import genai
from typing import List

# ❌ Wrong (deprecated)
import google.generativeai as genai
from types import List
```

### Enable Debug Logging
```python
from loguru import logger
import sys

logger.remove()
logger.add(sys.stderr, level="DEBUG")

brain = Brain(user_id="test")
```

### Health Check
```python
# Test all components
from db.vectore_store import VectorStore
from memory.encoding.gemini import GeminiEmbedder
from memory.encoding.ollama import OllamaEmbedder
from config.settings import settings

# Test Qdrant
vs = VectorStore()
print("✓ Qdrant connected")

# Test Embedder (based on your config)
if settings.embedding_provider == "ollama":
    embedder = OllamaEmbedder()
    print("✓ Using Ollama embeddings")
else:
    embedder = GeminiEmbedder()
    print("✓ Using Gemini embeddings")

vec = embedder.embed("test")
print(f"✓ Embedder working ({len(vec)} dimensions)")
```

</details>

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest --cov=core --cov=memory --cov=intelligence tests/

# Run specific test
pytest tests/test_brain.py -v

# Run with output
pytest tests/ -s -v
```

### Test Structure
```
tests/
├── test_brain.py           # End-to-end tests
├── test_memory_store.py    # Storage tests
├── test_retrieval.py       # Search & ranking tests
├── test_embedder.py        # Embedding tests
└── test_chat.py            # Chat integration tests
```

---

## 📊 Evaluation Framework

NeuroMem includes a comprehensive evaluation suite to measure and track system performance.

### Running Evaluations

```bash
# Run complete evaluation suite
python -m evaluation.run_eval

# This will test:
# - Retrieval quality (precision, recall, nDCG)
# - Deduplication effectiveness
# - Performance benchmarks (latency, throughput)
```

### Evaluation Components

#### 1. Retrieval Quality (`eval_retrieval.py`)

Measures how accurately the system retrieves relevant memories using information retrieval metrics.

**Metrics:**
- **Precision@K**: Accuracy of top-K results
- **Recall@K**: Coverage of relevant memories
- **nDCG**: Normalized Discounted Cumulative Gain
- **MAP**: Mean Average Precision
- **MRR**: Mean Reciprocal Rank

**Test Scenarios**: (from `test_cases.json`)
- Food preferences
- Work history
- Medical information
- Travel experiences
- Learning activities
- ...and more (3300+ test queries)

```bash
# Example output
Retrieval Metrics:
  nDCG@10: 0.847
  Precision@5: 0.823
  MAP: 0.791
  MRR: 0.895
```

#### 2. Deduplication Testing (`eval_dedup.py`)

Tests the system's ability to detect and merge similar/duplicate memories.

**Test Cases:**
- Near-identical memories (should merge)
- Semantically similar memories (should merge)
- Distinct memories (should NOT merge)

```python
# Example test case
memories = [
    "User loves spicy Indian food",
    "User really enjoys spicy Indian cuisine",  # Similar → merge
    "User likes pizza"                           # Different → keep
]
# Expected: 2 memories (1 Indian food + 1 pizza)
```

#### 3. Performance Benchmarks (`eval_performance.py`)

Measures system latency and throughput under load.

**Metrics:**
- Store operation latency (p50, p95, p99)
- Search operation latency (p50, p95, p99)
- Batch operation speedup
- Throughput (ops/second)

```bash
# Example output
Performance Benchmarks (n=50):
  Store Latency:
    p50: 245ms
    p95: 312ms
  Search Latency:
    p50: 98ms
    p95: 156ms
```

### Evaluation Results

Results are automatically saved to `evaluation/data/results/` with timestamps:

```
evaluation/data/results/
├── eval_20260218_171151.json
├── eval_20260219_064006.json
└── eval_20260219_070526.json
```

### Custom Test Cases

Add your own test cases to `evaluation/data/test_cases.json`:

```json
{
  "scenario": "my_custom_test",
  "memories": [
    "First memory to store",
    "Second memory to store"
  ],
  "queries": [
    {
      "query_id": "test_q1",
      "query": "What should I retrieve?",
      "relevance": {
        "0": 2,  // First memory: highly relevant
        "1": 0   // Second memory: not relevant
      }
    }
  ]
}
```

### Continuous Evaluation

Recommended workflow for production systems:

```bash
# 1. Baseline evaluation before changes
python -m evaluation.run_eval

# 2. Make your changes (tuning, new features, etc.)

# 3. Re-evaluate
python -m evaluation.run_eval

# 4. Compare results
python -m evaluation.reports.compare_results \
  eval_20260218_171151.json \
  eval_20260219_064006.json
```

---

## 💰 Cost Estimation

### Option 1: Fully Self-Hosted (Ollama + Local Qdrant)

| Service | Usage | Cost |
|---------|-------|------|
| **Ollama** | Unlimited | **$0** (self-hosted) |
| **Qdrant** | Local deployment | **$0** (self-hosted) |
| **Hardware** | GPU/CPU | Your existing infrastructure |
| **Total** | 100K memories/month | **$0** |

**Requirements:**
- 8GB RAM minimum (16GB recommended)
- GPU optional but recommended for faster embeddings
- ~10GB disk space for models

### Option 2: Gemini + Local Qdrant

| Service | Usage | Cost |
|---------|-------|------|
| **Gemini Embeddings** | 100K embeds | ~$1 |
| **Gemini LLM** | ~1K calls | ~$0.50 |
| **Qdrant** | Local deployment | **$0** |
| **Total** | 100K memories/month | **~$1.50/month** |

### Option 3: Fully Cloud (Gemini + Qdrant Cloud)

| Service | Usage | Cost |
|---------|-------|------|
| **Gemini Embeddings** | 100K embeds | ~$1 |
| **Gemini LLM** | ~1K calls | ~$0.50 |
| **Qdrant Cloud** | 100K vectors | $25-50 |
| **Total** | 100K memories/month | **~$26-52/month** |

### Option 4: Hybrid (Gemini Embeddings + Ollama LLM)

| Service | Usage | Cost |
|---------|-------|------|
| **Gemini Embeddings** | 100K embeds | ~$1 |
| **Ollama LLM** | Unlimited | **$0** (self-hosted) |
| **Qdrant** | Local deployment | **$0** |
| **Total** | 100K memories/month | **~$1/month** |

### Free Tier Options

- **Gemini**: 15 requests/min free tier (sufficient for POC/development)
- **Ollama**: Completely free, unlimited (self-hosted)
- **Qdrant**: Local deployment unlimited & free
- **Development Cost: $0** (using Ollama + local Qdrant)

---

## ❓ FAQ

### Which embedding provider should I use?

**For Development/Testing:**
- Use **Ollama** (free, fast setup, no API keys)

**For Production:**
- **Privacy-critical**: Ollama (100% local, no data leaves your infrastructure)
- **Best quality**: Gemini (state-of-the-art embeddings, 3072 dimensions)
- **Best value**: Hybrid (Gemini embeddings + Ollama LLM)

### Can I switch providers later?

Yes, but you must reset the collection when changing embedding providers:

```bash
# 1. Update .env with new provider
# 2. Reset collection
python utils/reset_collection.py
# 3. Re-index your memories
```

**Note:** Switching only the LLM provider (not embeddings) requires no reset.

### What are the embedding dimensions?

| Provider | Model | Dimensions | Quality |
|----------|-------|------------|---------|
| Gemini | gemini-embedding-001 | 3072 | ⭐⭐⭐⭐⭐ Excellent |
| Ollama | nomic-embed-text | 768 | ⭐⭐⭐⭐ Very Good |
| Ollama | mxbai-embed-large | 1024 | ⭐⭐⭐⭐ Very Good |
| Ollama | all-minilm | 384 | ⭐⭐⭐ Good |

### Can I use different models?

Yes! Configure in `.env`:

```env
# Ollama: Use any model from https://ollama.ai/library
ollama_embedding_model=nomic-embed-text
ollama_model=llama3.2  # or llama3.1, mistral, phi3, etc.

# Gemini: Use any Gemini model
llm_model=gemini-2.5-flash  # or gemini-1.5-pro, etc.
```

### How do I run completely offline?

```env
# .env - 100% local, zero internet required
embedding_provider=ollama
llm_provider=ollama
qdrant_host=localhost
```

Make sure Ollama and Qdrant are running locally.

### What hardware do I need for Ollama?

**Minimum:**
- 8GB RAM
- 4 CPU cores
- 10GB disk space

**Recommended:**
- 16GB RAM
- 8+ CPU cores
- NVIDIA GPU (optional, 3-5× faster embeddings)
- 20GB disk space

### How do I use a GPU with Ollama?

The included `docker-compose.yml` already configures GPU support:

```bash
docker-compose up -d
```

For manual setup:
```bash
# Install NVIDIA Container Toolkit first
# Then run Ollama with GPU
docker run -d --gpus=all -p 11434:11434 ollama/ollama
```

### Is my data private with Ollama?

**Yes!** When using Ollama:
- All embeddings generated locally
- All LLM inference local
- No data sent to external APIs
- No telemetry or tracking

Perfect for:
- Healthcare (HIPAA compliance)
- Financial services
- Personal journaling
- Any privacy-sensitive application

---

## 🗺️ Roadmap

| Version | Status | Key Features |
|---------|--------|--------------|
| **v1.0** | ✅ Live | Core memory, Gemini + Ollama support, Qdrant, Batch ops, Chat, Evaluation suite |
| **v1.1** | 🚧 Q1 2026 | Memory consolidation, Auto-linking, Analytics dashboard |
| **v1.2** | 📋 Q2 2026 | FastAPI REST API, LangChain integration, Web UI |
| **v1.3** | 📋 Q3 2026 | Multi-modal, Encryption, Multi-language |
| **v2.0** | 🔮 Q4 2026 | Enterprise features, RBAC, Advanced scaling |

<details>
<summary><b>Detailed Roadmap</b></summary>

**v1.1 - Enhanced Intelligence**
- Memory consolidation (merge similar)
- Automatic relationship graphs
- Smart chunking for long content
- Analytics dashboard
- Adaptive importance scoring

**v1.2 - Integrations**
- FastAPI REST API
- LangChain integration
- Web-based memory browser
- AutoGPT plugin
- Webhook support

**v1.3 - Advanced Features**
- Multi-modal (images, audio)
- End-to-end encryption
- Multi-language support
- Auto-refresh/versioning
- Advanced pruning

**v2.0 - Enterprise**
- Team/org memory spaces
- RBAC & advanced permissions
- Horizontal scaling
- Hybrid search (vector + full-text)
- Disaster recovery

</details>

---

## 🤝 Contributing

We love contributions! Here's how:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing`
3. **Commit** changes: `git commit -m 'Add amazing feature'`
4. **Push** to branch: `git push origin feature/amazing`
5. **Open** a Pull Request

### Guidelines
- ✅ Write tests for new features
- ✅ Follow existing code style
- ✅ Update documentation
- ✅ Keep PRs focused

### Areas for Contribution
- 🐛 Bug fixes
- ✨ New features
- 📚 Documentation
- 🧪 Test coverage
- 🎨 UI/CLI improvements
- 🚀 Performance optimizations

---

## ⚠️ Production Checklist

Before deploying to production:

### Security & Privacy
- [ ] 🔐 Implement authentication (API keys/OAuth2)
- [ ] 🔒 Encrypt sensitive memory content
- [ ] 🏠 For privacy: Use Ollama (fully local) instead of cloud APIs
- [ ] 🌍 For cloud: Ensure GDPR/compliance with data processing agreements
- [ ] 🔑 Rotate API keys regularly (if using cloud services)

### Infrastructure
- [ ] 📊 Add monitoring (Prometheus/Grafana)
- [ ] 💾 Set up automated backups (Qdrant snapshots)
- [ ] 🌍 Use Qdrant Cloud for scaling (or self-host with redundancy)
- [ ] 🔄 Implement rate limiting
- [ ] 🚨 Configure alerting

### Operations
- [ ] 📝 Set up structured logging
- [ ] 🧪 Load testing (target scale)
- [ ] 📈 Run evaluation suite baseline
- [ ] 🔄 Set up CI/CD pipeline
- [ ] 📚 Document runbooks for common issues

### Privacy-First Deployment (Recommended)

For maximum privacy and cost savings:
```env
# 100% local - no data leaves your infrastructure
embedding_provider=ollama
llm_provider=ollama
qdrant_host=localhost  # or your private network
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file.

```
Copyright (c) 2026 NeuroMem Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 🙏 Acknowledgments

**Inspiration:**
- Cognitive psychology research (episodic vs semantic memory)
- Ebbinghaus forgetting curve
- Vector database innovations

**Built With:**
- [Google Gemini](https://ai.google.dev/) - Cloud embeddings & LLM
- [Ollama](https://ollama.ai/) - Self-hosted LLM & embeddings
- [Qdrant](https://qdrant.tech/) - Vector database
- [Pydantic](https://docs.pydantic.dev/) - Data validation
- [Click](https://click.palletsprojects.com/) - CLI framework
- [ranx](https://amenra.github.io/ranx/) - Information retrieval evaluation

**Special Thanks:**
- The AI/ML open-source community
- Early testers and contributors
- Cognitive science research community

---

<div align="center">

## 🌟 Star Us on GitHub!

If NeuroMem helps your project, please give us a star!

[![GitHub stars](https://img.shields.io/github/stars/azizmabrouk11/NeuroMem?style=social)](https://github.com/azizmabrouk11/NeuroMem)
[![GitHub forks](https://img.shields.io/github/forks/azizmabrouk11/NeuroMem?style=social)](https://github.com/azizmabrouk11/NeuroMem/fork)

### Made with ❤️ for the AI Community

*Building the future of AI memory, one vector at a time*

**[⬆ Back to Top](#-neuromem)** • **[Report Issue](https://github.com/azizmabrouk11/NeuroMem/issues)** • **[Get Started](#-quick-start)**

</div>
