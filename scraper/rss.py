import feedparser
from config import RSS_QUERIES, REDDIT_RSS_FEEDS
from processor.filter import tag_and_score
from db.models import insert_item


def _process_feed(url, source_label):
    count = 0
    feed = feedparser.parse(url)
    for entry in feed.entries:
        text = f"{entry.title} {entry.get('summary', '')}"
        result = tag_and_score(text, source="rss")
        if result:
            insert_item(
                source=source_label,
                title=entry.title,
                url=entry.link,
                body=entry.get("summary", "")[:500],
                domain=result["domain"],
                score=result["score"],
                keywords=result["keywords"],
            )
            count += 1
    return count


def scrape_rss():
    count = 0

    # Google News RSS
    for query in RSS_QUERIES:
        url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}+when:1d&hl=en-IN&gl=IN&ceid=IN:en"
        count += _process_feed(url, "google-news")
    print(f"[Google News RSS] {count} civic items stored")

    # Reddit public RSS — no API key needed
    reddit_count = 0
    for feed_url in REDDIT_RSS_FEEDS:
        reddit_count += _process_feed(feed_url, "reddit-rss")
    print(f"[Reddit RSS] {reddit_count} civic items stored")

    return count + reddit_count
