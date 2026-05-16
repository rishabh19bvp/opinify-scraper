import os
import praw
from processor.filter import tag_and_score
from db.models import insert_item


def scrape_reddit():
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT", "opinify-scraper/1.0"),
    )
    subreddit = reddit.subreddit("pune")
    count = 0

    for post in subreddit.new(limit=100):
        text = f"{post.title} {post.selftext}"
        result = tag_and_score(text, source="reddit", upvotes=post.score, comments=post.num_comments)
        if result:
            insert_item(
                source="reddit",
                title=post.title,
                url=f"https://reddit.com{post.permalink}",
                body=post.selftext[:500],
                domain=result["domain"],
                score=result["score"],
                upvotes=post.score,
                comments=post.num_comments,
                keywords=result["keywords"],
            )
            count += 1

    print(f"[Reddit] {count} civic items stored")
