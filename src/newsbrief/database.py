import sqlite3
from pathlib import Path
from datetime import datetime, timezone


DB_PATH = Path(__file__).resolve().parents[2]/"data"/"news_brief.sqlite3"

def initialize_database()-> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS sent_stories(
                url TEXT PRIMARY KEY,
                sent_at TEXT NOT NULL
            )
            """
        )
        connection.commit()
    finally:
        connection.close()

def get_sent_story_urls() ->  set[str]:
    connection = sqlite3.connect(DB_PATH)
    try:
        rows = connection.execute(
            """SELECT url FROM sent_stories"""
        ).fetchall()
        return {row[0] for row in rows}
    finally:
        connection.close()


def mark_story_sent(url: str) -> None:
    sent_at = datetime.now(timezone.utc).isoformat()

    connection = sqlite3.connect(DB_PATH)
    try:
        connection.execute(
            """
            INSERT OR IGNORE INTO sent_stories (url, sent_at)
            VALUES (?, ?)
            """,
            (url, sent_at),
        )
        connection.commit()
    finally:
        connection.close()
    
