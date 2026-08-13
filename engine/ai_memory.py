import sqlite3
import os
from datetime import datetime


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE = os.path.join(
    PROJECT_ROOT,
    "users.db"
)


class AIMemory:

    def __init__(self):
        self.create_table()


    def connect(self):
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn


    def create_table(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ai_memory (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            symbol TEXT,
            signal TEXT,
            confidence REAL,

            session TEXT,
            trend TEXT,

            liquidity INTEGER,
            fvg INTEGER,
            orderblock INTEGER,

            entry REAL,
            exit REAL,

            profit REAL,

            result TEXT,

            created_at TEXT

        )
        """)

        conn.commit()
        conn.close()



    def save_trade(self, data):

        conn = self.connect()
        cursor = conn.cursor()


        cursor.execute("""
        INSERT INTO ai_memory (

            symbol,
            signal,
            confidence,
            session,
            trend,
            liquidity,
            fvg,
            orderblock,
            entry,
            exit,
            profit,
            result,
            created_at

        )

        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)

        """, (

            data.get("symbol",""),
            data.get("signal","WAIT"),
            data.get("confidence",0),

            data.get("session",""),
            data.get("trend",""),

            int(data.get("liquidity",False)),
            int(data.get("fvg",False)),
            int(data.get("orderblock",False)),

            data.get("entry",0),
            data.get("exit",0),

            data.get("profit",0),

            data.get("result","UNKNOWN"),

            datetime.utcnow().isoformat()

        ))


        conn.commit()
        conn.close()



    def statistics(self):

        conn = self.connect()
        cursor = conn.cursor()


        total = cursor.execute(
            "SELECT COUNT(*) FROM ai_memory"
        ).fetchone()[0]


        wins = cursor.execute(
            """
            SELECT COUNT(*)
            FROM ai_memory
            WHERE result='WIN'
            """
        ).fetchone()[0]


        losses = cursor.execute(
            """
            SELECT COUNT(*)
            FROM ai_memory
            WHERE result='LOSS'
            """
        ).fetchone()[0]


        accuracy = 0

        if total > 0:
            accuracy = round(
                (wins / total) * 100,
                2
            )


        conn.close()


        return {

            "total_trades": total,

            "wins": wins,

            "losses": losses,

            "accuracy": accuracy

        }



ai_memory = AIMemory()
