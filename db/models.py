import sqlite3
from datetime import datetime, timedelta

DB_PATH = "opinify.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            source       TEXT NOT NULL,
            title        TEXT NOT NULL,
            url          TEXT,
            body         TEXT,
            domain       TEXT,
            score        REAL DEFAULT 0,
            upvotes      INTEGER DEFAULT 0,
            comments     INTEGER DEFAULT 0,
            raw_keywords TEXT,
            scraped_at   TEXT NOT NULL,
            alerted      INTEGER DEFAULT 0,
            is_complaint INTEGER DEFAULT 0,
            lead_sent    INTEGER DEFAULT 0
        )
    """)
    # Migrate existing DB — add columns if missing
    try:
        conn.execute("ALTER TABLE items ADD COLUMN is_complaint INTEGER DEFAULT 0")
    except Exception:
        pass
    try:
        conn.execute("ALTER TABLE items ADD COLUMN lead_sent INTEGER DEFAULT 0")
    except Exception:
        pass
    conn.execute("""
        CREATE TABLE IF NOT EXISTS spikes (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            domain      TEXT,
            topic       TEXT,
            item_count  INTEGER,
            detected_at TEXT
        )
    """)
    conn.commit()
    conn.close()


def insert_item(source, title, url, body, domain, score, upvotes=0, comments=0, keywords="", is_complaint=False):
    conn = sqlite3.connect(DB_PATH)
    existing = conn.execute("SELECT id FROM items WHERE url = ?", (url,)).fetchone()
    if not existing:
        conn.execute("""
            INSERT INTO items (source, title, url, body, domain, score, upvotes, comments, raw_keywords, scraped_at, is_complaint)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (source, title, url, body, domain, score, upvotes, comments, keywords, datetime.utcnow().isoformat(), int(is_complaint)))
        conn.commit()
    conn.close()


def get_unsent_leads(source_prefix="reddit", hours=6):
    """Fresh complaint posts not yet sent — deduped by URL."""
    conn = sqlite3.connect(DB_PATH)
    cutoff = (datetime.utcnow() - timedelta(hours=hours)).isoformat()
    rows = conn.execute("""
        SELECT MIN(id), title, url, domain FROM items
        WHERE source LIKE ? AND is_complaint = 1 AND lead_sent = 0 AND scraped_at > ?
        GROUP BY url
        ORDER BY MIN(scraped_at) DESC
    """, (f"{source_prefix}%", cutoff)).fetchall()
    conn.close()
    return rows


def mark_leads_sent(ids):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(f"UPDATE items SET lead_sent = 1 WHERE id IN ({','.join('?'*len(ids))})", ids)
    conn.commit()
    conn.close()


def get_today_top(limit=5):
    conn = sqlite3.connect(DB_PATH)
    today = datetime.utcnow().date().isoformat()
    rows = conn.execute("""
        SELECT title, url, domain, score, source
        FROM items
        WHERE scraped_at LIKE ?
        ORDER BY score DESC
        LIMIT ?
    """, (f"{today}%", limit)).fetchall()
    conn.close()
    return [{"title": r[0], "url": r[1], "domain": r[2], "score": round(r[3], 2), "source": r[4]} for r in rows]


def get_digest_items(hours=8, limit_per_domain=4):
    """Items from last N hours grouped by domain — for digest messages."""
    conn = sqlite3.connect(DB_PATH)
    cutoff = (datetime.utcnow() - timedelta(hours=hours)).isoformat()
    rows = conn.execute("""
        SELECT id, title, url, domain, source, score
        FROM items
        WHERE scraped_at > ?
          AND source != 'quora'
        ORDER BY domain, score DESC
    """, (cutoff,)).fetchall()
    conn.close()

    grouped = {}
    seen_per_domain = {}
    for row in rows:
        id_, title, url, domain, source, score = row
        if domain not in grouped:
            grouped[domain] = []
            seen_per_domain[domain] = 0
        if seen_per_domain[domain] < limit_per_domain:
            grouped[domain].append((id_, title, url, source))
            seen_per_domain[domain] += 1
    return grouped


def get_recent_by_domain(domain, hours=3):
    conn = sqlite3.connect(DB_PATH)
    cutoff = (datetime.utcnow() - timedelta(hours=hours)).isoformat()
    rows = conn.execute("""
        SELECT id, title, url FROM items
        WHERE domain = ? AND scraped_at > ? AND alerted = 0
    """, (domain, cutoff)).fetchall()
    conn.close()
    return rows


def mark_alerted(ids):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(f"UPDATE items SET alerted = 1 WHERE id IN ({','.join('?'*len(ids))})", ids)
    conn.commit()
    conn.close()
