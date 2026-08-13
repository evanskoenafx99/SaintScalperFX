import sqlite3
from datetime import datetime


class ExecutionWorker:

    def __init__(self):
        self.db = "users.db"


    def process_orders(self):

        conn = sqlite3.connect(self.db)

        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()


        cursor.execute("""
        SELECT *
        FROM execution_queue
        WHERE status='PENDING'
        """)


        orders = cursor.fetchall()

        results = []


        for order in orders:


            # AI validation stage

            if order["direction"] not in ["BUY", "SELL"]:

                cursor.execute("""
                UPDATE execution_queue
                SET status='REJECTED'
                WHERE id=?
                """,
                (order["id"],))


                results.append({

                    "id": order["id"],
                    "status":"REJECTED",
                    "message":"Invalid direction"

                })

                continue



            # Move approved signal forward

            cursor.execute("""
            UPDATE execution_queue
            SET status='READY'
            WHERE id=?
            """,
            (order["id"],))


            results.append({

                "id": order["id"],

                "symbol": order["symbol"],

                "direction": order["direction"],

                "entry": order["entry"],

                "stop_loss": order["stop_loss"],

                "take_profit": order["take_profit"],

                "status":"READY",

                "message":"AI trade validated and ready for mobile execution"

            })


        conn.commit()

        conn.close()


        return results



    def update_status(self, trade_id, status):

        conn = sqlite3.connect(self.db)

        cursor = conn.cursor()


        cursor.execute("""
        UPDATE execution_queue
        SET status=?
        WHERE id=?
        """,
        (
            status,
            trade_id
        ))


        conn.commit()

        conn.close()


        return {

            "id": trade_id,

            "status": status,

            "updated": datetime.now().isoformat()

        }
