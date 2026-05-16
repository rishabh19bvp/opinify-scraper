import feedparser
import requests
from config import RSS_QUERIES, REDDIT_RSS_FEEDS, DIRECT_RSS_FEEDS, QUORA_RSS_FEEDS
from processor.filter import tag_and_score
from db.models import insert_item

DEFAULT_HEADERS = {"User-Agent": "opinify-scraper/1.0 by rishabh19bvp"}


def _process_feed(url, source_label, headers=None):
    count = 0
    try:
        resp = requests.get(url, headers=headers or DEFAULT_HEADERS, timeout=10)
        resp.raise_for_status()
        feed = feedparser.parse(resp.content)
    except Exception as e:
        print(f"[{source_label}] Fetch error: {e}")
        return 0
    for entry in feed.entries:
        text = f"{entry.title} {entry.get('summary', '')}"
        result = tag_and_score(text, source=source_label)
        if result:
            insert_item(
                source=source_label,
                title=entry.title,
                url=entry.link,
                body=entry.get("summary", "")[:500],
                domain=result["domain"],
                score=result["score"],
                keywords=result["keywords"],
                is_complaint=result.get("is_complaint", False),
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

    # Reddit public RSS — proper user-agent required
    reddit_count = 0
    for feed_url in REDDIT_RSS_FEEDS:
        reddit_count += _process_feed(feed_url, "reddit-rss")
    print(f"[Reddit RSS] {reddit_count} civic items stored")

    # Direct RSS feeds (ToI, IE, HT)
    direct_count = 0
    for feed in DIRECT_RSS_FEEDS:
        direct_count += _process_feed(feed["url"], feed["name"])
    print(f"[Direct RSS] {direct_count} civic items stored")

    # Quora via Google RSS — real people's civic questions, commentable
    quora_count = 0
    for feed_url in QUORA_RSS_FEEDS:
        quora_count += _process_feed(feed_url, "quora")
    print(f"[Quora RSS] {quora_count} civic items stored")

    return count + reddit_count + direct_count + quora_count
