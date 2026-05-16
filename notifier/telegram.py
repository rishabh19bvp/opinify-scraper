import os
import requests
from db.models import get_recent_by_domain, mark_alerted
from config import DOMAIN_KEYWORDS, SPIKE_THRESHOLD

DOMAIN_EMOJI = {
    "transport":      "🚌",
    "environment":    "🌳",
    "healthcare":     "🏥",
    "governance":     "🏛️",
    "infrastructure": "🔧",
    "general":        "📌",
}


def send_telegram(message):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, data={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}, timeout=10)
    except Exception as e:
        print(f"[Telegram] Send failed: {e}")


def check_and_alert():
    for domain in DOMAIN_KEYWORDS.keys():
        items = get_recent_by_domain(domain, hours=3)
        if len(items) >= SPIKE_THRESHOLD:
            ids    = [item[0] for item in items]
            emoji  = DOMAIN_EMOJI.get(domain, "📌")

            message = (
                f"{emoji} *Opinify Civic Spike — {domain.title()}*\n\n"
                f"{len(items)} items in the last 3 hours\n\n"
                f"*Top stories:*\n"
            )
            for item in items[:5]:
                title = item[1][:70]
                url   = item[2] or ""
                message += f"• [{title}]({url})\n"
            message += f"\n💡 *Poll opportunity:* Consider launching a poll about {domain} in Pune today."

            send_telegram(message)
            mark_alerted(ids)
            print(f"[Telegram] Alert sent for domain: {domain} ({len(items)} items)")
