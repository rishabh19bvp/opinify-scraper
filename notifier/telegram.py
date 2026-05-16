import os
import requests
from db.models import get_recent_by_domain, mark_alerted, get_unsent_leads, mark_leads_sent
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


def send_engagement_leads():
    """Send individual Reddit complaint posts as engagement leads."""
    leads = get_unsent_leads(source_prefix="reddit", hours=6)
    if not leads:
        return

    ids = [l[0] for l in leads]
    message = "🎯 *Opinify Engagement Leads — Reddit Complaints*\n\n"
    message += f"{len(leads)} fresh complaint posts to engage with:\n\n"

    for lead in leads[:8]:
        _, title, url, domain = lead
        emoji = DOMAIN_EMOJI.get(domain, "📌")
        message += f"{emoji} [{title[:70]}]({url})\n"
        message += f"↳ _Reply: \"We're tracking this on Opinify — vote here to push action!\"_\n\n"

    send_telegram(message)
    mark_leads_sent(ids)
    print(f"[Telegram] Engagement leads sent: {len(leads)} Reddit complaint posts")


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
