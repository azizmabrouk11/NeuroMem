<div align="center">

# NeuroMem

### Memory Layer for AI Assistants

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Vector DB](https://img.shields.io/badge/Vector_DB-Qdrant-DC244C?style=for-the-badge)](https://qdrant.tech/)
[![LLM](https://img.shields.io/badge/LLM-Ollama%20%7C%20Gemini-0F172A?style=for-the-badge)](https://ollama.com/)
[![Evaluation](https://img.shields.io/badge/Eval-ranx-059669?style=for-the-badge)](https://amenra.github.io/ranx/)

Persistent memory, semantic retrieval, and evaluation tooling for building assistants that remember users over time.

</div>

---

## Why NeuroMem

NeuroMem gives your assistant a practical long-term memory stack:

- Store user facts and events as structured memories.
- Retrieve relevant memories with semantic search + ranking.
- Use memory in chat responses automatically.
- Evaluate retrieval quality with reproducible test cases.
- Convert Label Studio annotations into evaluation-ready datasets.

## Core Capabilities

| Capability | What it does |
|---|---|
| Memory storage | Stores episodic and semantic memories with metadata |
| Smart retrieval | Combines similarity with importance and recency signals |
| Chat integration | Runs retrieve -> respond -> extract -> store loop |
| Provider flexibility | Ollama and Gemini embedding/LLM options |
| Evaluation suite | Retrieval, deduplication, and performance evaluation |
| Dataset tooling | Label Studio conversion and dataset exploration scripts |

## System Architecture

```mermaid
flowchart TB
    U[User Message] --> C[ChatManager]
    C --> B[Brain]
    B --> R[MemoryRetriever]
    B --> S[MemoryStore]
    R --> V[(Qdrant)]
    S --> V
    C --> L[LLMClient]
    C --> E[MemoryExtractor]
    E --> S
```

## Repository Layout

```text
NeuroMem/
|- app/                  # CLI entrypoints
|- ai/                   # Chat and LLM integration
|- core/                 # Brain orchestrator
|- memory/               # Store/retrieve/extraction/embeddings
|- intelligence/         # Ranking, scoring, decay
|- db/                   # Qdrant vector store
|- models/               # Memory/user models
|- evaluation/           # Eval runners, evaluators, converters, data
|- config/               # Runtime settings
|- mcp_server/           # MCP server and tool wrappers
|- utils/                # Debug and validation scripts
|- docker-compose.yml    # NeuroMem + Ollama + Qdrant + Label Studio
```

---

## How to Use

### 1) Start the local services

```bash
docker compose up -d
```

This starts:

- `neuromem` MCP service
- `ollama` on `11434`
- `qdrant` on `6333`
- `label-studio` on `8080`

### 2) Create the Python environment and install dependencies

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3) Configure `.env`

Start with this local setup:

```env
llm_provider=ollama
ollama_base_url=http://localhost:11434/v1
ollama_model=qwen2.5:3b-instruct

embedding_provider=ollama
ollama_embedding_model=mxbai-embed-large

qdrant_host=localhost
qdrant_port=6333
qdrant_collection_name=ai_brain_memories
```

If you want Gemini instead, switch `llm_provider` and `embedding_provider` to `gemini` and add `gemini_api_key`.

### 4) Use the CLI

The CLI is the fastest way to store, search, delete, and inspect memories.

Store a memory:

```bash
python -m app.cli remember "User likes Ethiopian food" -u demo -t semantic -g food -g preference
```

Search memories:

```bash
python -m app.cli recall "what food does the user like?" -u demo -k 5
```

Delete a memory:

```bash
python -m app.cli forget mem_abc123 -u demo
```

Build LLM-ready context:

```bash
python -m app.cli context "What are my preferences?" -u demo
```

Open an interactive memory chat:

```bash
python -m app.cli chat -u demo
```

Show quick stats:

```bash
python -m app.cli stats -u demo
```

### 5) Use the Python API

```python
from core.brain import Brain
from models.memory import MemoryType

brain = Brain(user_id="alice")

brain.remember(
    content="Alice likes long-distance running",
    memory_type=MemoryType.SEMANTIC,
    importance_score=0.8,
    tags=["fitness"]
)

results = brain.recall("What sports does Alice do?", top_k=5)
for r in results:
    print(r.final_score, r.memory.content)
```

Use the Python API when you want to embed NeuroMem inside another service or workflow.

### 6) Run the MCP server

The MCP server exposes the same memory capabilities as tools for agent runtimes.

```bash
python -m app.cli mcp
```

Available MCP tools:

- `store_memory`
- `retrieve_memories`
- `get_context`
- `delete_memory`
- `chat`
- `extract_memories`

### 7) Run evaluation workflows

Run the full suite:

```bash
python -m evaluation.run_eval
```

Outputs include retrieval metrics (Precision@3, Recall@5, nDCG, MRR, MAP), deduplication metrics, and performance benchmarks.

Use custom test cases:

```bash
python -c "from evaluation.run_eval import run_all; run_all('evaluation/data/test_cases_from_label_studio.json')"
```

Convert a Label Studio export into the test-case format:

```bash
python -m evaluation.converters.from_label_studio \
  --input-path evaluation/data/project-1-at-2026-03-18-02-30-cc045d7f.json \
  --output-path evaluation/data/test_cases_from_label_studio.json
```

Create Label Studio tasks from unlabeled scenarios:

```bash
python -m evaluation.converters.to_label_studio
```

Evaluation inputs and outputs live under `evaluation/data/` and `evaluation/data/results/`.

Useful local checks:

The `utils/` folder contains helper scripts for debugging embeddings, retrieval scores, and deduplication experiments.

---

## Common Workflows

### Add a new memory

Store a fact or event with `remember`, then validate retrieval with `recall` or `context`.

### Build a memory-aware chat app

Use `core.brain.Brain` directly in Python or wrap it with `ai.chat.ChatManager` for conversational flows.

### Integrate with an agent platform

Run the MCP server and call the tools from your client using the same user IDs and memory workflow as the CLI.

---

## Providers and Configuration

Main settings are defined in `config/settings.py` and loaded from `.env`.

| Setting | Default | Notes |
|---|---|---|
| `llm_provider` | `ollama` | `ollama` or `gemini` |
| `embedding_provider` | `ollama` | `ollama` or `gemini` |
| `ollama_model` | `qwen2.5:3b-instruct` | Chat model |
| `ollama_embedding_model` | `mxbai-embed-large` | Embedding model |
| `qdrant_host` | `localhost` | Qdrant host |
| `qdrant_port` | `6333` | Qdrant port |
| `langsmith_tracing` | `false` | Optional tracing |

---

## Label Studio Notes

- Docker route is the easiest: `http://localhost:8080`.
- In Python environments >= 3.13, the project installs `label-studio-sdk` instead of full `label-studio` package due upstream build issues.
- If you need full local CLI on Windows, use Docker or a Python 3.12 virtual environment dedicated to Label Studio.

---

## Development

```bash
pytest
```

Useful utility scripts live under `utils/` for data checks, embedding checks, and evaluation debugging.

---

## License

MIT
