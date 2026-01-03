import random
import sqlite3
from datetime import datetime

class WordManager:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)

    def get_session_words(self, count):
        words = self._fetch_words()
        weighted = []

        for word in words:
            weight = self._calculate_weight(word)
            if weight > 0:
                weighted.extend([word] * weight)

        return random.sample(weighted, count)

    def _calculate_weight(self, word):
        learned = word["learned_tier"]
        needs = word["needs_work_tier"]

        if learned >= 3:
            return 0
        if needs == 3:
            return 100
        if needs == 2:
            return 60
        if needs == 1:
            return 30
        if learned == 0:
            return 20
        if learned == 1:
            return 10
        if learned == 2:
            return 5
    def _fetch_words(self):
        self.conn.row_factory = sqlite3.Row
        cur = self.conn.cursor()
        cur.execute("""
            SELECT w.id, w.word, w.definition, w.origin, w.phonetic, w.sentence,
                   COALESCE(p.learned_tier, 0) as learned_tier,
                   COALESCE(p.needs_work_tier, 0) as needs_work_tier
            FROM words w
            LEFT JOIN progress p ON w.id = p.word_id
        """)
        return [dict(row) for row in cur.fetchall()]

    def update_progress(self, word_id, correct):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT learned_tier, needs_work_tier
            FROM progress WHERE word_id=?
        """, (word_id,))
        row = cur.fetchone()
        if row:
            learned, needs = row
        else:
            learned, needs = 0, 0

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
