def build_prompt(context_chunks: list[str], question: str) -> str:
    """
    Build a prompt for the language model by combining context chunks and the user's question.

    Args:
        context_chunks (list[str]): A list of context strings to include in the prompt.
        question (str): The user's question to be answered.

    Returns:
        str: The constructed prompt string.
    """
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