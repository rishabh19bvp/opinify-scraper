from config import CIVIC_KEYWORDS, DOMAIN_KEYWORDS, SCORE_WEIGHTS


def tag_and_score(text, source="unknown", upvotes=0, comments=0):
    text_lower = text.lower()

    matched = [kw for kw in CIVIC_KEYWORDS if kw in text_lower]
    if not matched:
        return None

    domain = "general"
    best_domain_count = 0
    for d, keywords in DOMAIN_KEYWORDS.items():
        hits = sum(1 for kw in keywords if kw in text_lower)
        if hits > best_domain_count:
            best_domain_count = hits
            domain = d

    keyword_density = min(len(matched) / 10, 1.0)
    upvote_score = min(upvotes / 100, 1.0) if source == "reddit" else 0.5
    comment_score = min(comments / 50, 1.0) if source == "reddit" else 0.3

    score = (
        upvote_score    * SCORE_WEIGHTS["reddit_upvotes"] +
        comment_score   * SCORE_WEIGHTS["reddit_comments"] +
        0.7             * SCORE_WEIGHTS["news_recency"] +
        keyword_density * SCORE_WEIGHTS["keyword_density"]
    )

    return {
        "domain":   domain,
        "score":    round(score, 3),
        "keywords": ",".join(matched[:5]),
    }
