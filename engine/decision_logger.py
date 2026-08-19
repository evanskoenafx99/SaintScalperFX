import json
import os
from datetime import datetime


LOG_FILE = "logs/decision_history.json"


class DecisionLogger:

    def __init__(self):
        os.makedirs("logs", exist_ok=True)


    def save(self, decision):

        entry = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            **decision
        }


        history = []


        if os.path.exists(LOG_FILE):

            try:
                with open(LOG_FILE, "r") as f:
                    history = json.load(f)

            except Exception:
                history = []


        history.append(entry)


        with open(LOG_FILE, "w") as f:
            json.dump(
                history,
                f,
                indent=4
            )


        print("Decision saved.")
