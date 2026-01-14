def is_faithful(answer: str, context_chunks: list[str]) -> bool:
    context = " ".join(context_chunks).lower()
    answer_sentences = answer.lower().split(".")

    for sentence in answer_sentences:
        if sentence.strip() and sentence.strip() not in context:
            return False

    return True
