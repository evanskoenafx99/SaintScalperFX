import sqlite3


class TradeLifecycle:


    def __init__(self):

        self.db = "users.db"


    def get_open_trades(self):

        conn = sqlite3.connect(self.db)
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute("""
        SELECT *
        FROM trades
        WHERE status='OPEN'
        """)

        trades = cursor.fetchall()

        conn.close()

        return [dict(t) for t in trades]


    def sync_positions(self, positions):

        open_trades = self.get_open_trades()

        results = []


        for trade in open_trades:

            matched = None


            for position in positions:

                if (
                    trade["symbol"] == position["symbol"]
                    and
                    trade["direction"] == position["direction"]
                ):

                    matched = position
                    break


            if matched:

                profit = matched.get("profit", 0)

                self.update_profit(
                    trade["id"],
                    profit
                )

                results.append({

                    "trade_id": trade["id"],
                    "status": "OPEN",
                    "symbol": trade["symbol"],
                    "profit": profit

                })

            else:

                self.close_trade(

                    trade_id=trade["id"],
                    exit_price="BROKER_CLOSED",
                    profit=0

                )

                results.append({

                    "trade_id": trade["id"],
                    "status": "CLOSED",
                    "symbol": trade["symbol"],
                    "profit": 0

                })


        return results


    def update_profit(

        self,
        trade_id,
        profit

    ):

        conn = sqlite3.connect(self.db)

        cursor = conn.cursor()

        cursor.execute("""

        UPDATE trades

        SET profit=?

        WHERE id=?

        """, (

            profit,
            trade_id

        ))

        conn.commit()

        conn.close()


    def close_trade(

        self,
        trade_id,
        exit_price,
        profit

    ):

        conn = sqlite3.connect(self.db)

        cursor = conn.cursor()

        cursor.execute("""

        UPDATE trades

        SET
            exit=?,
            profit=?,
            status='CLOSED'

        WHERE id=?

        """, (

            exit_price,
            profit,
            trade_id

        ))

        conn.commit()

        conn.close()
