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
            alerted      INTEGER DEFAULT 0
        )
    """)
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


def insert_item(source, title, url, body, domain, score, upvotes=0, comments=0, keywords=""):
    conn = sqlite3.connect(DB_PATH)
    existing = conn.execute("SELECT id FROM items WHERE url = ?", (url,)).fetchone()
    if not existing:
        conn.execute("""
            INSERT INTO items (source, title, url, body, domain, score, upvotes, comments, raw_keywords, scraped_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (source, title, url, body, domain, score, upvotes, comments, keywords, datetime.utcnow().isoformat()))
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
