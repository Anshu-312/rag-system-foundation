from app.evaluation.test_cases import TEST_CASES
from app.evaluation.retrieval_metrics import recall_at_k
from app.services.ingestion.embedder import embed_text
from app.services.retrieval.vector_store import create_index, VectorStore
from app.core.config import settings

DIM = settings.dimension
index = create_index(DIM)
store = VectorStore.load(index)


def run_retrieval_evaluation(top_k: int = 4):
    results = []

    for case in TEST_CASES:
        query = case["query"]
        expected = case["expected_keywords"]

        query_vector = embed_text([query])[0]
        retrieved_chunks = store.search(query_vector, top_k)

        success = recall_at_k(retrieved_chunks, expected)

        results.append({
            "query": query,
            "recall@k": success,
            "retrieved_chunks": retrieved_chunks
        })

    return results

if __name__ == "__main__":
    results = run_retrieval_evaluation(top_k=4)

    print("\n=== RETRIEVAL EVALUATION RESULTS ===\n")
    for r in results:
        print(f"Query: {r['query']}")
        print(f"Recall@4: {r['recall@k']}")
        print("Retrieved chunks:")
        for c in r["retrieved_chunks"]:
            print("-", c["text"][:120], "...")
        print("-" * 50)