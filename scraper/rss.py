import feedparser
from config import RSS_QUERIES
from processor.filter import tag_and_score
from db.models import insert_item


def scrape_rss():
    count = 0
    for query in RSS_QUERIES:
        url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}+when:1d&hl=en-IN&gl=IN&ceid=IN:en"
        feed = feedparser.parse(url)
        for entry in feed.entries:
            text = f"{entry.title} {entry.get('summary', '')}"
            result = tag_and_score(text, source="rss")
            if result:
                insert_item(
                    source="rss",
                    title=entry.title,
                    url=entry.link,
                    body=entry.get("summary", "")[:500],
                    domain=result["domain"],
                    score=result["score"],
                    keywords=result["keywords"],
                )
                count += 1
    print(f"[RSS] {count} civic items stored")
