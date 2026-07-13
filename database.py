import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# Analysis history table
cursor.execute("""
CREATE TABLE IF NOT EXISTS analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT NOT NULL,
    signal TEXT,
    trend TEXT,
    confidence TEXT,
    reason TEXT,
    entry TEXT,
    stop_loss TEXT,
    take_profit TEXT,
    image TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS preferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT UNIQUE NOT NULL,
    market TEXT,
    timeframe TEXT,
    risk TEXT
)
""")
conn.commit()
conn.close()

print("✅ Database updated successfully!")
