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
        return 0

def update_progress(self, word_id, correct):
    if correct:
        learned += 1
        needs = 0
    else:
        needs += 1
        learned = 0

    learned = min(3, learned)
    needs = min(3, needs)
