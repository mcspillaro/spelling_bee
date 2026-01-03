import sqlite3
from pathlib import Path

def init_user_db(user_dir):
    user_dir = Path(user_dir)
    user_dir.mkdir(parents=True, exist_ok=True)

    db_path = user_dir / "progress.db"
    conn = sqlite3.connect(db_path)

    with open("database/schema.sql") as f:
        conn.executescript(f.read())

    return conn
