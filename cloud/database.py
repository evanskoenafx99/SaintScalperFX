import sqlite3


DATABASE = "users.db"


def init_cloud_database():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()


    # Customer subscriptions
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


    # Connected trading accounts
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


    # AI trading preferences
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trading_settings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        mode TEXT DEFAULT 'NORMAL',
        risk TEXT DEFAULT '1%',
        auto_trade TEXT DEFAULT 'OFF'
    )
    """)


    # Trade history
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
    init_cloud_database()
    print("SaintCloud database ready")
