def recall_at_k(retrieved_chunks: list[str], expected_keywords: list[str]) -> bool:
    text_chunks = [chunk["text"] for chunk in retrieved_chunks] 
    joined = " ".join(text_chunks).lower()
    return all(keyword.lower() in joined for keyword in expected_keywords)