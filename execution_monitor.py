import time
import requests

SERVER = "http://127.0.0.1:8000"


def monitor():
    while True:
        try:
            response = requests.post(
                f"{SERVER}/execution/monitor",
                timeout=10
            )

            print(response.json())

        except Exception as e:
            print("Execution Monitor Error:", e)

        time.sleep(5)


if __name__ == "__main__":
    print("Execution Monitor Started...")
    monitor()
