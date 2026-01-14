def keyword_score(query: str, text: str) -> int:
    score = 0

    for token in query.lower().split():
        if token in text.lower():
            score += 1
    return score 