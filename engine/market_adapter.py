"""
SaintScalperFX Market Adapter

Universal market data layer.

Current sources:
- TwelveData
- Future MT5/Broker API

The AI engine will always read from this adapter,
not directly from a broker or data provider.
"""

import time


class MarketAdapter:

    def __init__(self):

        self.market = {
            "symbol": "",
            "timeframe": "",
            "bid": 0,
            "ask": 0,
            "candles": [],
            "source": "NONE",
            "updated": 0
        }


    # ==========================
    # UPDATE MARKET DATA
    # ==========================

    def update(
        self,
        symbol,
        timeframe,
        bid,
        ask,
        candles,
        source="UNKNOWN"
    ):

        self.market = {

            "symbol": symbol,

            "timeframe": timeframe,

            "bid": float(bid),

            "ask": float(ask),

            "candles": candles,

            "source": source,

            "updated": time.time()

        }


        return self.market



    # ==========================
    # GET CURRENT MARKET
    # ==========================

    def get_market(self):

        return self.market



    # ==========================
    # CHECK MARKET HEALTH
    # ==========================

    def is_ready(self):

        if self.market["bid"] <= 0:
            return False

        if len(self.market["candles"]) == 0:
            return False

        return True



    # ==========================
    # BROKER FORMAT PLACEHOLDER
    # ==========================

    def from_mt5(
        self,
        symbol,
        timeframe,
        tick,
        candles
    ):

        return self.update(

            symbol=symbol,

            timeframe=timeframe,

            bid=tick.get("bid",0),

            ask=tick.get("ask",0),

            candles=candles,

            source="MT5"

        )



    # ==========================
    # TWELVEDATA FORMAT
    # ==========================

    def from_twelvedata(self, data):

        return self.update(

            symbol=data.get("symbol",""),

            timeframe=data.get("timeframe",""),

            bid=data.get("bid",0),

            ask=data.get("ask",0),

            candles=data.get("candles",[]),

            source="TWELVEDATA"

        )


# Global adapter instance

market_adapter = MarketAdapter()
