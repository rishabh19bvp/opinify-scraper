import os
from dotenv import load_dotenv
load_dotenv()

from apscheduler.schedulers.background import BackgroundScheduler
from db.models import init_db
from scraper.rss import scrape_rss
from scraper.news import scrape_news
from notifier.telegram import send_digest, send_outreach_leads
from api.digest import app


def run_scrapers():
    """Hourly — scrape all sources, store new items."""
    print("\n--- Scraper run started ---")
    scrape_rss()
    scrape_news()
    print("--- Scraper run complete ---\n")


def run_digest():
    """3x daily — send Telegram digest + outreach leads."""
    print("\n--- Digest run ---")
    send_digest()
    send_outreach_leads()
    print("--- Digest done ---\n")


if __name__ == "__main__":
    init_db()

    # Run immediately on startup
    run_scrapers()
    run_digest()

    scheduler = BackgroundScheduler()

    # Scrape every hour
    scheduler.add_job(run_scrapers, "interval", hours=1, id="scraper")

    # Digest at 8am, 2pm, 9pm IST (IST = UTC+5:30, so UTC 2:30, 8:30, 15:30)
    scheduler.add_job(run_digest, "cron", hour=2,  minute=30, id="digest_morning")
    scheduler.add_job(run_digest, "cron", hour=8,  minute=30, id="digest_afternoon")
    scheduler.add_job(run_digest, "cron", hour=15, minute=30, id="digest_evening")

    scheduler.start()

    port = int(os.getenv("FLASK_PORT", 5050))
    print(f"Digest API running at http://localhost:{port}/digest")
    app.run(host="0.0.0.0", port=port)
