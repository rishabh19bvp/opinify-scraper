import os
from dotenv import load_dotenv
load_dotenv()

from apscheduler.schedulers.background import BackgroundScheduler
from db.models import init_db
from scraper.rss import scrape_rss
from scraper.news import scrape_news
from notifier.telegram import check_and_alert
from api.digest import app


def run_all_scrapers():
    print("\n--- Scraper run started ---")
    scrape_rss()
    scrape_news()
    check_and_alert()
    print("--- Scraper run complete ---\n")


if __name__ == "__main__":
    init_db()

    run_all_scrapers()

    scheduler = BackgroundScheduler()
    scheduler.add_job(run_all_scrapers, "interval", hours=1)
    scheduler.start()

    port = int(os.getenv("FLASK_PORT", 5050))
    print(f"Digest API running at http://localhost:{port}/digest")
    app.run(host="0.0.0.0", port=port)
