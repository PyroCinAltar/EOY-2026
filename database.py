import sqlite3

DB_NAME = "scores.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        time REAL NOT NULL
    )
    """)

    conn.commit()
    conn.close()


def add_score(name, time):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute(
        "INSERT INTO scores (name, time) VALUES (?, ?)",
        (name, time)
    )

    conn.commit()
    conn.close()


def get_top_scores(limit=10):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute(
        "SELECT name, time FROM scores ORDER BY time ASC LIMIT ?",
        (limit,)
    )

    results = c.fetchall()
    conn.close()

    return results