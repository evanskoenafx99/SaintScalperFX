"""
SaintScalperFX Bridge Launcher

Starts all bridge services.

Current:
- Execution Listener

Future:
- Saint Bridge
- Account Sync
- Position Sync
"""

import threading

from bridge.execution_listener import listener


def start_execution():

    listener.start()


def main():

    print("=" * 50)
    print(" SaintScalperFX Bridge")
    print("=" * 50)

    execution_thread = threading.Thread(
        target=start_execution,
        daemon=True
    )

    execution_thread.start()

    execution_thread.join()


if __name__ == "__main__":
    main()
