import importlib


class MT5Bridge:

    def __init__(self):
        self.connected = False
        self.account = None
        self.broker = None
        self.bridge = None


    def connect(self, broker_name, credentials=None):

        self.broker = broker_name.lower()

        try:

            module = importlib.import_module(
                f"bridge.{self.broker}"
            )

            self.bridge = module.Broker()

            self.connected = self.bridge.connect(credentials)

            if self.connected:
                self.account = self.bridge.get_account()

            return self.connected

        except Exception as e:

            print("Bridge Error:", e)

            self.connected = False

            return False


    def disconnect(self):

        if self.bridge:

            self.bridge.disconnect()

        self.connected = False


    def is_connected(self):

        return self.connected


    def get_account(self):

        if self.bridge:

            return self.bridge.get_account()

        return None


    def get_candles(
        self,
        symbol="XAUUSD",
        timeframe="M15",
        bars=200
    ):

        if not self.bridge:

            return []

        return self.bridge.get_candles(
            symbol,
            timeframe,
            bars
        )


    def place_order(
        self,
        symbol,
        signal,
        lot,
        sl,
        tp
    ):

        if not self.bridge:

            return False

        return self.bridge.place_order(
            symbol,
            signal,
            lot,
            sl,
            tp
        )


    def close_trade(self, ticket):

        if not self.bridge:

            return False

        return self.bridge.close_trade(ticket)
