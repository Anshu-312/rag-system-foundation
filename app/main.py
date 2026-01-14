from fastapi import FastAPI
from app.core.config import settings
from app.schema.models import IngestRequest, QueryRequest, AnswerResponse
from app.services.ingestion.chunker import chunk_text
from app.services.ingestion.embedder import embed_text
from app.services.retrieval.vector_store import create_index, VectorStore
from app.services.rag.pipeline import run_rag_pipeline

app = FastAPI(
    title="RAG API",
    description="An API for Retrieval-Augmented Generation (RAG) using FastAPI",
    version="0.1.0"
)

# Initialize the faiss index and creating vector store
index = create_index(settings.dimension)
store = VectorStore.load(index)

@app.post("/ingest", status_code=201, summary="Ingest text data into the vector store", tags=["Ingestion"], description="Ingest text data by chunking and embedding it, then storing it in the vector store.")
async def ingest(request: IngestRequest):
    chunks = []
    for text in request.documents:
        chunks.extend(chunk_text(text, settings.chunk_size, settings.chunk_overlap))

    vectors = embed_text(chunks)
    store.add(vectors, chunks)
    store.save()
    return {"message": f"Ingested {len(chunks)} chunks."}

@app.post("/ask", response_model=AnswerResponse, summary="Query the RAG system", tags=["Query"], description="Query the RAG system to get answers based on the ingested data.")
async def ask(request: QueryRequest):
    answer, sources = run_rag_pipeline(request.query, store, request.top_k)
    return {"answer": answer, "sources": sources}

@app.get("/")
async def root():
    return {"Welcome to the RAG API."}