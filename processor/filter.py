import re
from config import CIVIC_KEYWORDS, DOMAIN_KEYWORDS, SCORE_WEIGHTS, COMPLAINT_SIGNALS


def _strip_html(text):
    """Remove HTML tags and decode common entities."""
    text = re.sub(r'<[^>]+>', ' ', text)
    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
    return re.sub(r'\s+', ' ', text).strip()


def tag_and_score(text, source="unknown", upvotes=0, comments=0):
    # Strip HTML first — Reddit RSS summaries are HTML blobs
    clean = _strip_html(text)

    # For Reddit use only the first 200 chars (title region) to avoid
    # matching URL parameters and image alt text in the body blob
    if source == "reddit-rss":
        signal_text = clean[:200].lower()
    else:
        signal_text = clean.lower()

    text_lower = clean.lower()

    matched_civic = [kw for kw in CIVIC_KEYWORDS if kw in signal_text]
    if not matched_civic:
        return None

    # Require complaint signal for Reddit — filters lifestyle/travel posts
    matched_signals = [s for s in COMPLAINT_SIGNALS if s in signal_text]
    is_complaint = len(matched_signals) > 0
    if source == "reddit-rss" and not is_complaint:
        return None

    domain = "general"
    best_domain_count = 0
    for d, keywords in DOMAIN_KEYWORDS.items():
        hits = sum(1 for kw in keywords if kw in text_lower)
        if hits > best_domain_count:
            best_domain_count = hits
            domain = d

    keyword_density = min(len(matched_civic) / 10, 1.0)
    upvote_score  = min(upvotes / 100, 1.0) if source == "reddit-rss" else 0.5
    comment_score = min(comments / 50, 1.0) if source == "reddit-rss" else 0.3

    score = (
        upvote_score    * SCORE_WEIGHTS["reddit_upvotes"] +
        comment_score   * SCORE_WEIGHTS["reddit_comments"] +
        0.7             * SCORE_WEIGHTS["news_recency"] +
        keyword_density * SCORE_WEIGHTS["keyword_density"]
    )

    return {
        "domain":       domain,
        "score":        round(score, 3),
        "keywords":     ",".join(matched_civic[:5]),
        "is_complaint": is_complaint,   # True = real person complaining
    }
