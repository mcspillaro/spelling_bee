import sqlite3
from pathlib import Path
import sys
import os

def init_user_db(user_dir):
    user_dir = Path(user_dir)
    user_dir.mkdir(parents=True, exist_ok=True)

    db_path = user_dir / "progress.db"
    conn = sqlite3.connect(db_path)

    if hasattr(sys, '_MEIPASS'):
        schema_path = os.path.join(sys._MEIPASS, 'database', 'schema.sql')
    else:
        schema_path = 'database/schema.sql'

    with open(schema_path) as f:
        conn.executescript(f.read())

    return conn
