import csv
import sqlite3

def import_words(csv_path, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    with open(csv_path, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute("""
                INSERT OR REPLACE INTO words
                (word, definition, origin, phonetic, sentence)
                VALUES (?, ?, ?, ?, ?)
            """, (
                row["word"],
                row["definition"],
                row["origin"],
                row["phonetic"],
                row["sentence"]
            ))

    conn.commit()
    conn.close()
