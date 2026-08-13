"""
SaintScalperFX Execution Listener

Listens for approved trades from the Cloud API and forwards
them to the MT5 client.

Current Status:
- Uses placeholder MT5 client
- Ready for live MT5 integration later
"""

import time
import requests

from bridge.mt5_client import mt5_client

CLOUD_URL = "http://127.0.0.1:8000"


class ExecutionListener:

    def __init__(self):

        self.running = False

    def poll(self):

        try:

            response = requests.get(
                f"{CLOUD_URL}/command",
                timeout=5
            )

            return response.json()

        except Exception as e:

            return {
                "command": "NONE",
                "error": str(e)
            }

    def execute(self, command):

        if command.get("command") == "NONE":
            return

        result = mt5_client.open_trade(
            symbol=command.get("symbol", ""),
            side=command.get("command", ""),
            lot=command.get("lot_size", 0.01),
            sl=command.get("stop_loss", 0),
            tp=command.get("take_profit", 0)
        )

        print(result)

    def start(self):

        self.running = True

        print("Execution Listener Started...")

        while self.running:

            command = self.poll()

            self.execute(command)

            time.sleep(2)


listener = ExecutionListener()


if __name__ == "__main__":
    listener.start()
