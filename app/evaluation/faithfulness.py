def is_faithful(answer: str, context_chunks: list) -> bool:
    extracted_texts = [
        chunk.page_content if hasattr(chunk, 'page_content') else 
        (chunk.get("page_content") or chunk.get("text") or str(chunk))
        if isinstance(chunk, dict) else str(chunk)
        for chunk in context_chunks
    ]
    context = " ".join(extracted_texts).lower()
    answer_sentences = answer.lower().split(".")

    for sentence in answer_sentences:
        if sentence.strip() and sentence.strip() not in context:
            return False

    return True
