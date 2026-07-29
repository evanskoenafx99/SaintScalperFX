import sqlite3
from datetime import datetime


class ExecutionQueue:

    def __init__(self):

        self.db = "users.db"


    def add_order(self, user_id, order):

        conn = sqlite3.connect(self.db)

        cursor = conn.cursor()


        cursor.execute("""
        CREATE TABLE IF NOT EXISTS execution_queue (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            symbol TEXT,

            direction TEXT,

            entry TEXT,

            stop_loss TEXT,

            take_profit TEXT,

            status TEXT,

            created_at DATETIME

        )
        """)


        cursor.execute("""
        INSERT INTO execution_queue
        (
            user_id,
            symbol,
            direction,
            entry,
            stop_loss,
            take_profit,
            status,
            created_at
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?)

        """,
        (
            user_id,
            order.get("symbol"),
            order.get("signal"),
            order.get("entry"),
            order.get("stop_loss"),
            order.get("take_profit"),
            "PENDING",
            datetime.now()
        ))


        conn.commit()
        conn.close()


        return {

            "status":"queued",

            "message":"Order added to execution queue"

        }



    def get_pending(self):

        conn = sqlite3.connect(self.db)

        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()


        cursor.execute("""
        SELECT *
        FROM execution_queue
        WHERE status='PENDING'
        """)


        orders = cursor.fetchall()

        conn.close()


        return [dict(order) for order in orders]
