import sqlite3
from datetime import datetime

from mt5_bridge import MT5Bridge
from core.risk_guardian import RiskGuardian


class ExecutionWorker:

    def __init__(self):

        self.db = "users.db"

        self.mt5 = MT5Bridge()

        self.risk = RiskGuardian()



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


            allowed = self.check_permission(
                order["user_id"]
            )


            if not allowed:

                cursor.execute("""
                UPDATE execution_queue
                SET status='REJECTED'
                WHERE id=?
                """,
                (order["id"],))


                results.append({

                    "id": order["id"],

                    "status": "REJECTED",

                    "reason": "Trading permission denied"

                })

                continue



            risk_check = self.risk.check_trade(
                order["direction"],
                [
                    {
                        "high": float(order["entry"]),
                        "low": float(order["entry"])
                    }
                ],
                float(order["entry"]),
                float(order["entry"])
            )


            if not risk_check["allowed"]:

                cursor.execute("""
                UPDATE execution_queue
                SET status='REJECTED'
                WHERE id=?
                """,
                (order["id"],))


                results.append({

                    "id": order["id"],

                    "status": "REJECTED",

                    "reason": risk_check["reason"]

                })

                continue



            connected = self.mt5.connect(
                "saintbridge"
            )


            if not connected:

                status = "FAILED"

                reason = "MT5 bridge connection failed"


            else:

                opened = self.mt5.place_order(

                    order["symbol"],

                    order["direction"],

                    0.01,

                    order["stop_loss"],

                    order["take_profit"]

                )


                if opened:

                    status = "OPENED"

                    reason = "Trade opened successfully"

                    self.save_trade(order)


                else:

                    status = "FAILED"

                    reason = "Broker rejected order"



            cursor.execute("""
            UPDATE execution_queue
            SET status=?
            WHERE id=?
            """,
            (
                status,
                order["id"]
            ))


            results.append({

                "id": order["id"],

                "status": status,

                "reason": reason

            })


        conn.commit()

        conn.close()


        return results



    def save_trade(self, order):

        conn = sqlite3.connect(self.db)

        cursor = conn.cursor()


        cursor.execute("""
        INSERT INTO trades
        (
            user_id,
            symbol,
            direction,
            entry,
            status,
            created_at
        )

        VALUES (?, ?, ?, ?, ?, ?)

        """,
        (
            order["user_id"],
            order["symbol"],
            order["direction"],
            order["entry"],
            "OPEN",
            datetime.now()
        ))


        conn.commit()

        conn.close()



    def check_permission(self, user_id):

        conn = sqlite3.connect(self.db)

        cursor = conn.cursor()


        cursor.execute("""
        SELECT status
        FROM subscriptions
        WHERE user_id=?
        ORDER BY id DESC
        LIMIT 1
        """,
        (user_id,))

        subscription = cursor.fetchone()



        cursor.execute("""
        SELECT auto_trade
        FROM trading_settings
        WHERE user_id=?
        """,
        (user_id,))

        settings = cursor.fetchone()



        cursor.execute("""
        SELECT status
        FROM trading_accounts
        WHERE user_id=?
        """,
        (user_id,))

        account = cursor.fetchone()


        conn.close()


        return (
            subscription
            and subscription[0] == "ACTIVE"
            and settings
            and settings[0] == "ON"
            and account
            and account[0] == "CONNECTED"
        )
