import os, json, sqlite3
from datetime import datetime

DB_PATH = os.getenv("DB_PATH", "data/db.sqlite")

def _ensure_dirs():
    d = os.path.dirname(DB_PATH)
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)

def init_db():
    _ensure_dirs()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT NOT NULL,
        payload TEXT NOT NULL,
        report TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def save_report(payload: dict, report_text: str) -> int:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO reports (created_at, payload, report) VALUES (?, ?, ?)",
        (datetime.utcnow().isoformat(), json.dumps(payload), report_text)
    )
    conn.commit()
    rid = cur.lastrowid
    conn.close()
    return rid

def list_reports(limit: int = 10):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, created_at FROM reports ORDER BY id DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return [{"id": r[0], "created_at": r[1]} for r in rows]

def get_report(report_id: int):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, created_at, payload, report FROM reports WHERE id = ?", (report_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return {"id": row[0], "created_at": row[1], "payload": json.loads(row[2]), "report": row[3]}
