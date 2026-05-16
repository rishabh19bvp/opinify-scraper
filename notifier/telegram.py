import os
from datetime import datetime
import requests
from db.models import get_digest_items, get_unsent_leads, mark_leads_sent
from config import DOMAIN_KEYWORDS

DOMAIN_EMOJI = {
    "transport":      "🚌",
    "environment":    "🌳",
    "healthcare":     "🏥",
    "governance":     "🏛️",
    "infrastructure": "🔧",
    "general":        "📌",
}

SOURCE_LABEL = {
    "reddit-rss":          "Reddit 💬",
    "quora":               "Quora 💬",
    "google-news":         "Google News",
    "toi-pune":            "Times of India",
    "ie-pune":             "Indian Express",
    "hindustan-times-pune":"Hindustan Times",
    "Pune Mirror":         "Pune Mirror",
    "Maharashtra Times":   "Maharashtra Times",
}

# Sources where you can actually go and comment
COMMENTABLE_SOURCES = {"reddit-rss", "quora"}


def send_telegram(message):
    token   = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url     = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, data={
            "chat_id":    chat_id,
            "text":       message,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True,
        }, timeout=10)
    except Exception as e:
        print(f"[Telegram] Send failed: {e}")


def send_digest():
    """3x daily digest — grouped by domain with links."""
    hour = datetime.utcnow().hour
    if   hour < 12:  slot = "🌅 Morning"
    elif hour < 17:  slot = "☀️ Afternoon"
    else:            slot = "🌙 Evening"

    grouped = get_digest_items(hours=8, limit_per_domain=4)
    if not grouped:
        print("[Telegram] Digest: no items to send")
        return

    total = sum(len(v) for v in grouped.values())
    message = f"*{slot} Civic Digest — Pune*\n"
    message += f"_{total} issues from the last 8 hours_\n\n"

    for domain, items in grouped.items():
        if not items:
            continue
        emoji = DOMAIN_EMOJI.get(domain, "📌")
        message += f"{emoji} *{domain.title()}* ({len(items)})\n"
        for _, title, url, source in items:
            src   = SOURCE_LABEL.get(source, source)
            label = title[:65]
            message += f"• [{label}]({url}) _{src}_\n"
        message += "\n"

    message += "💡 _Pick an issue → create a poll on Opinify → share poll link in comments_"

    send_telegram(message)
    print(f"[Telegram] {slot} digest sent — {total} items across {len(grouped)} domains")


def send_outreach_leads():
    """Reddit complaint posts — go reply with Opinify poll link."""
    leads = get_unsent_leads(source_prefix="reddit", hours=8)
    if not leads:
        print("[Telegram] No new Reddit leads")
        return

    ids     = [l[0] for l in leads]
    message = "🎯 *Reddit Outreach — Go Reply*\n"
    message += f"_{len(leads)} Pune civic complaints to engage with_\n\n"

    for lead in leads[:6]:
        _, title, url, domain = lead
        emoji = DOMAIN_EMOJI.get(domain, "📌")
        message += f"{emoji} [{title[:70]}]({url})\n"

    message += (
        "\n↳ *Suggested reply:*\n"
        '_"We raised this on Opinify so Pune residents can vote collectively '
        'and push PMC to act. More votes = more pressure: opinify.co.in"_'
    )

    send_telegram(message)
    mark_leads_sent(ids)
    print(f"[Telegram] Outreach leads sent: {len(leads)} Reddit posts")
