import sqlite3

from mt5_bridge import MT5Bridge


DATABASE = "users.db"


class TradeManager:

    def __init__(self):

        self.database = DATABASE
        self.bridge = MT5Bridge()


    def get_open_trades(self):

        conn = sqlite3.connect(self.database)
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute("""
        SELECT *
        FROM trades
        WHERE status='OPEN'
        ORDER BY created_at DESC
        """)

        trades = cursor.fetchall()

        conn.close()

        return [dict(t) for t in trades]


    def evaluate_trade(self, trade, position):

        profit = position.get("profit", 0)

        action = "HOLD"
        reason = "Trade within parameters"

        if profit > 0:

            action = "PROTECT"
            reason = "Trade is profitable"

        elif profit < 0:

            action = "MONITOR"
            reason = "Trade currently negative"

        return {

            "trade_id": trade["id"],
            "symbol": trade["symbol"],
            "action": action,
            "profit": profit,
            "reason": reason

        }


    def manage_positions(self, positions):

        trades = self.get_open_trades()

        results = []

        for trade in trades:

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

                results.append(
                    self.evaluate_trade(
                        trade,
                        matched
                    )
                )

            else:

                results.append({

                    "trade_id": trade["id"],
                    "symbol": trade["symbol"],
                    "action": "CLOSED",
                    "profit": 0,
                    "reason": "Position not found"

                })

        return results


    def execute_management_action(

        self,
        action,
        ticket=None,
        stop_loss=None,
        take_profit=None

    ):

        connected = self.bridge.connect(
            "saintbridge"
        )

        if not connected:

            return {

                "success": False,
                "reason": "Broker connection failed"

            }


        if action == "HOLD":

            return {

                "success": True,
                "reason": "No action required"

            }


        return self.bridge.execute_with_confirmation(

            action=action,
            ticket=ticket,
            stop_loss=stop_loss,
            take_profit=take_profit

        )
