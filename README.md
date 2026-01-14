# RAG System Foundation

This repository is a compact, educational RAG service implemented with FastAPI and FAISS. The codebase is intentionally small to make it easy to extend and experiment with ingestion, embedding, retrieval, reranking, prompt construction, and answer generation.

Concise architecture
- API: `app/main.py` exposes two endpoints — `POST /ingest` and `POST /ask`.
- Ingestion: `app/services/ingestion` contains `chunker.py` (text chunking) and `embedder.py` (SentenceTransformer embeddings).
- Storage: `app/services/retrieval/vector_store.py` wraps a FAISS index and persists text chunks alongside the index file.
- Retrieval & ranking: `vector_store.search` returns candidate chunks; `app/services/retrieval/reranker.py` (CrossEncoder) reranks them; `lexical.py` and `hybrid.py` provide simple lexical and hybrid helpers.
- RAG pipeline: `app/services/rag/pipeline.py` ties embedding, retrieval, reranking, prompt building, generation, and a faithfulness check.
- Generation: `app/services/generation/prompt.py` builds the LLM prompt; `llm_client.py` handles the model call.
- Evaluation: `app/evaluation/faithfulness.py` contains a basic mask-based faithfulness check.

Key Pydantic schemas (API surface)
- `IngestRequest` (app/schema/models.py): `documents: List[str]`, optional `metadata: dict`.
- `QueryRequest`: `query: str`, `top_k: int = 5`.
- `Source` model: `{ text: str, score: float }` used in responses.
- `AnswerResponse`: `{ answer: str, sources: List[Source] }`.

Notable recent edits (summary)
- Introduced a reranker using `sentence-transformers.CrossEncoder` at `app/services/retrieval/reranker.py` and integrated it into the pipeline.
- Added `lexical.py` and `hybrid.py` as simple retrieval utilities for lexical scoring and merging semantic/lexical results.
- Reworked `app/services/generation/prompt.py` to accept chunk objects and extract text safely from `page_content` or object string.
- Added `app/evaluation/faithfulness.py` to flag answers not supported by retrieved context.
- API/typing improvements:
	- `AnswerResponse.sources` now returns objects with `text` and `score`.
	- `QueryRequest.top_k` standardized to `int` with default `5`.
- Fixed several bugs and mismatches: `embed_text` call sites, `create_index` return value, use of `store.search` vs missing `retrieve` API, and prompt ordering.

How to run (quick)
1. Create & activate virtualenv and install:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Start server:

```powershell
uvicorn app.main:app --reload
```

3. Example payloads
- Ingest (curl):

```bash
curl -X POST http://127.0.0.1:8000/ingest -H "Content-Type: application/json" -d '{"documents": ["First document text.", "Second document text."] }'
```

- Ask (curl):

```bash
curl -X POST http://127.0.0.1:8000/ask -H "Content-Type: application/json" -d '{"query":"What is the topic?","top_k":5}'
```

Development notes & recommendations
- The CrossEncoder reranker loads a relatively large model; consider lazy loading or a feature flag to avoid startup cost in development.
- Add a small `scripts/` integration test to ingest fixed text and query to validate E2E behavior; I can add that for you.
- Add unit tests for `reranker`, `faithfulness`, and `hybrid` merging.
- `.vscode/` settings were added; I updated `.gitignore` to exclude the folder.

If you'd like, I can now:
- Commit and push the `.gitignore` and `README.md` updates.
- Add a `scripts/` example that runs an E2E ingest+ask flow and prints results.