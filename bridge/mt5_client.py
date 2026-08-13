"""
SaintScalperFX MT5 Client

This module will become the bridge between the AI and the
MetaTrader 5 terminal.

For now it provides a common interface so the rest of the
system can be built before the MT5 connection is added.
"""

import time


class MT5Client:

    def __init__(self):

        self.connected = False

        self.account = {
            "balance": 0.0,
            "equity": 0.0,
            "margin": 0.0,
            "free_margin": 0.0,
            "login": 0,
            "server": "",
            "name": ""
        }

        self.market = {
            "symbol": "",
            "bid": 0.0,
            "ask": 0.0,
            "timeframe": "",
            "candles": []
        }

        self.positions = []

    # ===================================
    # CONNECTION
    # ===================================

    def connect(self):

        self.connected = True
        return True

    def disconnect(self):

        self.connected = False

    def is_connected(self):

        return self.connected

    # ===================================
    # ACCOUNT
    # ===================================

    def update_account(self, account):

        self.account = account

    def get_account(self):

        return self.account

    # ===================================
    # MARKET
    # ===================================

    def update_market(self, market):

        self.market = market

    def get_market(self):

        return self.market

    # ===================================
    # POSITIONS
    # ===================================

    def update_positions(self, positions):

        self.positions = positions

    def get_positions(self):

        return self.positions

    # ===================================
    # TRADE PLACEHOLDERS
    # ===================================

    def open_trade(
        self,
        symbol,
        side,
        lot,
        sl,
        tp
    ):

        print(
            "[MT5]",
            "OPEN",
            symbol,
            side,
            lot,
            sl,
            tp
        )

        return {
            "success": True,
            "ticket": int(time.time())
        }

    def close_trade(self, ticket):

        print("[MT5] CLOSE", ticket)

        return True


mt5_client = MT5Client()
