import sqlite3
from datetime import datetime

class ProgressManager:
    def __init__(self, conn):
        self.conn = conn

    def update(self, word_id, correct):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT learned_tier, needs_work_tier
            FROM progress WHERE word_id=?
        """, (word_id,))
        row = cur.fetchone() or (0, 0)

        learned, needs = row

        if correct:
            learned = min(learned + 1, 3)
            needs = 0
        else:
            needs = min(needs + 1, 3)
            learned = 0

        cur.execute("""
            INSERT OR REPLACE INTO progress
            (word_id, learned_tier, needs_work_tier, last_seen)
            VALUES (?, ?, ?, ?)
        """, (word_id, learned, needs, datetime.now()))

        self.conn.commit()
