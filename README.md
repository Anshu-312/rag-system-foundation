# RAG System Foundation

A minimal, opinionated foundation for building a Retrieval-Augmented Generation (RAG) service in Python.

This repository provides a small, end-to-end example demonstrating ingestion, embedding, vector storage, retrieval, and a simple LLM prompt pipeline. It's intended as a starting point for experiments, prototypes, and learning how the pieces of a RAG stack fit together.

Key features
- Ingest plain text documents, chunk them, and compute embeddings.
- Store vectors in a FAISS index with associated text chunks.
- Simple retrieval and prompt-building for LLM-driven answers.
- Small, easy-to-read codebase suitable for extension.

Quickstart

1. Create and activate a virtual environment (Windows example):

```powershell
python -m venv venv
venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

2. Run the API server:

```powershell
uvicorn app.main:app --reload
```

3. Ingest documents (POST `/ingest`) and query the system (POST `/ask`).

API Endpoints
- `POST /ingest` — Accepts JSON payload with `documents: List[str]` to chunk, embed, and store.
- `POST /ask` — Accepts `{ "query": "...", "top_k": 5 }` and returns an answer plus `sources` (list of text chunks used).

Project layout
- `app/main.py` — FastAPI entrypoint and route definitions.
- `app/services/ingestion` — Chunking and embedding helpers.
- `app/services/retrieval` — FAISS-backed vector store wrapper.
- `app/services/rag` — Simple pipeline that ties retrieval + prompt building + generation.
- `app/services/generation` — LLM client and prompt utilities.

Configuration
- Edit `app/core/config.py` (or set env vars) to configure model names, FAISS index path, and chunk sizes.

Data & privacy
- The `data/` directory (ignored by Git) is the suggested place for local datasets and ingested files. Do not commit sensitive data.

Contributing
- Open issues and pull requests are welcome. Keep changes small and focused.

License
- See `LICENSE` for license terms.

Questions or help
- If you want, I can add example curl commands or a tiny test script that ingests sample text and runs a query.