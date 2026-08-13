import time
from datetime import datetime

from mt5_bridge import MT5Bridge
from core.trade_lifecycle import TradeLifecycle
from trade_manager import TradeManager
from core.action_history import ActionHistory


class TradeLifecycleWorker:

    def __init__(self):

        self.bridge = MT5Bridge()
        self.lifecycle = TradeLifecycle()
        self.manager = TradeManager()
        self.history = ActionHistory()

        self.running = False


    def log(self, message):

        print(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}"
        )


    def connect(self):

        if self.bridge.is_connected():

            return True

        self.log("Connecting to SaintBridge...")

        return self.bridge.connect("saintbridge")


    def execute_action(
        self,
        decision,
        position
    ):

        action = decision.get("action")

        if action == "HOLD":

            return {
                "status": "SKIPPED",
                "reason": "No action required"
            }

        if position is None:

            return {
                "status": "FAILED",
                "reason": "Position not found"
            }

        confirmation = self.manager.execute_management_action(
            action=action,
            ticket=position.get("ticket")
        )

        if confirmation.get("success"):

            return {
                "status": "CONFIRMED",
                "reason": confirmation.get("reason")
            }

        return {
            "status": "FAILED",
            "reason": confirmation.get(
                "reason",
                "Execution failed"
            )
        }


    def run_once(self):

        if not self.connect():

            return {
                "status": "error",
                "message": "Broker connection failed"
            }

        positions = self.bridge.get_positions()

        lifecycle = self.lifecycle.sync_positions(
            positions
        )

        management = self.manager.manage_positions(
            positions
        )

        execution = []

        for decision in management:

            matched = None

            for position in positions:

                if (
                    position["symbol"] == decision["symbol"]
                ):

                    matched = position
                    break

            result = self.execute_action(
                decision,
                matched
            )

            self.history.record(
                decision["trade_id"],
                decision["action"],
                result["status"],
                result["reason"]
            )

            execution.append({

                "trade_id": decision["trade_id"],
                "action": decision["action"],
                "status": result["status"],
                "reason": result["reason"]

            })

        return {

            "status": "success",
            "positions_checked": len(positions),
            "lifecycle": lifecycle,
            "management": management,
            "execution": execution

        }


    def run(self, interval=5):

        self.running = True

        self.log("SaintScalperFX Worker Started")

        while self.running:

            try:

                result = self.run_once()

                self.log(
                    f"Cycle complete | Positions: {result.get('positions_checked', 0)} | Status: {result.get('status')}"
                )

            except Exception as e:

                self.log(f"Worker Error: {e}")

            time.sleep(interval)


    def stop(self):

        self.running = False

        self.bridge.disconnect()

        self.log("Worker Stopped")


if __name__ == "__main__":

    worker = TradeLifecycleWorker()

    try:

        worker.run(interval=5)

    except KeyboardInterrupt:

        worker.stop()
