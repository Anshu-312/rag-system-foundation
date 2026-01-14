def hybrid_merge(
        semantic_chunks: list[str],
        lexical_chunks: list[str],
        alpha: float = 0.7
):
    seen = {}
    for chunk in semantic_chunks:
        seen[chunk] = alpha

    for chunk in lexical_chunks:
        seen[chunk] = seen.get(chunk, 0) + (1 - alpha)

    return sorted(seen.keys(), key=lambda x: seen[x], reverse=True)