import sqlite3
from datetime import datetime


DATABASE = "users.db"


class ActionHistory:


    def __init__(self):

        self.database = DATABASE



    def record(
        self,
        trade_id,
        action,
        status,
        reason
    ):

        conn = sqlite3.connect(
            self.database
        )

        cursor = conn.cursor()


        cursor.execute("""
        CREATE TABLE IF NOT EXISTS trade_actions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            trade_id INTEGER,

            action TEXT,

            status TEXT,

            reason TEXT,

            created_at TEXT

        )
        """)


        cursor.execute("""
        INSERT INTO trade_actions
        (
            trade_id,
            action,
            status,
            reason,
            created_at
        )

        VALUES (?, ?, ?, ?, ?)
        """,
        (
            trade_id,
            action,
            status,
            reason,
            datetime.now()
        ))


        conn.commit()

        conn.close()


        return True
