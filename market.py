class MarketData:

    def __init__(self):
        self.connected = False
        self.symbol = "XAUUSD"
        self.timeframe = "M15"

    def connect(self):
        self.connected = True
        return True

    def disconnect(self):
        self.connected = False

    def status(self):
        return self.connected

    def get_symbol(self):
        return self.symbol

    def set_symbol(self, symbol):
        self.symbol = symbol.upper()

    def get_timeframe(self):
        return self.timeframe

    def set_timeframe(self, timeframe):
        self.timeframe = timeframe.upper()
