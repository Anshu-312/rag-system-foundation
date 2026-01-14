def build_prompt(reranked_chunks: list, question: str) -> str:
    """
    Build a prompt for the language model by combining context chunks and the user's question.

    Args:
        context_chunks (list[str]): A list of context strings to include in the prompt.
        question (str): The user's question to be answered.

    Returns:
        str: The constructed prompt string.
    """
    # 1. Extract text strings from the chunk objects
    context_chunks = [
        chunk.page_content if hasattr(chunk, 'page_content') else str(chunk)
        for chunk in reranked_chunks
    ]

    # 2. Join the strings
    context = "\n\n".join(context_chunks)
    
    return f"""
You are a factual assistant.
Answer ONLY using the context below.
If the answer is not present, say "I don't know".

Context:
{context}

Question:
{question}
"""