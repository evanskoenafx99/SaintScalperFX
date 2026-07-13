class MT5Bridge:

    def __init__(self):

        self.connected = False
        self.account = None

    def connect(self):

        # Will connect to MT5 later
        self.connected = True

        return self.connected

    def disconnect(self):

        self.connected = False

    def is_connected(self):

        return self.connected

    def get_account(self):

        return self.account

    def get_candles(self, symbol="XAUUSD", timeframe="M15", bars=200):

        return []
