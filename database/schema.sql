CREATE TABLE IF NOT EXISTS words (
    id INTEGER PRIMARY KEY,
    word TEXT UNIQUE NOT NULL,
    definition TEXT,
    origin TEXT,
    phonetic TEXT,
    sentence TEXT
);

CREATE TABLE IF NOT EXISTS progress (
    word_id INTEGER PRIMARY KEY,
    learned_tier INTEGER DEFAULT 0,
    needs_work_tier INTEGER DEFAULT 0,
    last_seen DATETIME,
    FOREIGN KEY(word_id) REFERENCES words(id)
);
