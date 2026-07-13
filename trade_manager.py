class TradeManager:

    def __init__(self):

        self.open_trades = []

    def add_trade(self, trade):

        self.open_trades.append(trade)

    def get_trades(self):

        return self.open_trades

    def close_trade(self, index):

        if index < len(self.open_trades):
            self.open_trades.pop(index)
