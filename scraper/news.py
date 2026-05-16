import requests
from bs4 import BeautifulSoup
from config import NEWS_SITES
from processor.filter import tag_and_score
from db.models import insert_item

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; OpinifyBot/1.0)"}


def scrape_news():
    count = 0
    for site in NEWS_SITES:
        try:
            res = requests.get(site["url"], headers=HEADERS, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")
            articles = soup.select(site["article_selector"])

            for article in articles[:20]:
                title_el = article.select_one(site["title_selector"])
                link_el = article.select_one(site["link_selector"])
                if not title_el:
                    continue
                title = title_el.get_text(strip=True)
                url = link_el["href"] if link_el else site["url"]
                if url.startswith("/"):
                    base = "/".join(site["url"].split("/")[:3])
                    url = base + url

                result = tag_and_score(title, source="news")
                if result:
                    insert_item(
                        source=site["name"],
                        title=title,
                        url=url,
                        body="",
                        domain=result["domain"],
                        score=result["score"],
                        keywords=result["keywords"],
                    )
                    count += 1
        except Exception as e:
            print(f"[News] Error scraping {site['name']}: {e}")
    print(f"[News] {count} civic items stored")
