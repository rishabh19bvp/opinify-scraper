from config import SCORE_WEIGHTS


def compute_score(upvotes=0, comments=0, keyword_density=0.0, source="unknown"):
    upvote_score = min(upvotes / 100, 1.0) if source == "reddit" else 0.5
    comment_score = min(comments / 50, 1.0) if source == "reddit" else 0.3

    return round(
        upvote_score    * SCORE_WEIGHTS["reddit_upvotes"] +
        comment_score   * SCORE_WEIGHTS["reddit_comments"] +
        0.7             * SCORE_WEIGHTS["news_recency"] +
        keyword_density * SCORE_WEIGHTS["keyword_density"],
        3,
    )
