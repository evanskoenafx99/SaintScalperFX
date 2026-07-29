import sqlite3


DATABASE = "users.db"


def init_database():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)


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


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subscriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        plan TEXT DEFAULT 'FREE',
        status TEXT DEFAULT 'ACTIVE',
        start_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        expiry_date TEXT
    )
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trading_accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        broker TEXT,
        account_type TEXT,
        account_number TEXT,
        status TEXT DEFAULT 'DISCONNECTED'
    )
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trading_settings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        mode TEXT DEFAULT 'NORMAL',
        risk TEXT DEFAULT '1%',
        auto_trade TEXT DEFAULT 'OFF'
    )
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        symbol TEXT,
        direction TEXT,
        entry TEXT,
        exit TEXT,
        profit TEXT,
        status TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)


    conn.commit()

    conn.close()



if __name__ == "__main__":

    init_database()

    print("✅ SaintCloud database ready")
