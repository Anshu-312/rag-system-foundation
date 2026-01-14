from sentence_transformers import CrossEncoder

# Load the cross-encoder model for reranking
_reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank(query: str, initial_chunks: list, top_n: int = 5):

    # 1. Extract strings from objects
    passages = [
        chunk.page_content if hasattr(chunk, 'page_content') else str(chunk)
        for chunk in initial_chunks
    ]

    # 2. Prepare pairs for the CrossEncoder
    pairs = [(query, passage) for passage in passages]

    # 3. Predict scores
    scores = _reranker.predict(pairs)
    
    # 4. Combine chunks with scores and sort
    # We use initial_chunks here so we return the original objects (with metadata)
    ranked = sorted(
        zip(initial_chunks, scores),
        key=lambda x: x[1],
        reverse=True
    )

    # 5. Return the top N chunks
    return [chunk for chunk, _ in ranked[:top_n]]