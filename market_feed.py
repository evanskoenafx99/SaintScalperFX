import os
import requests


TWELVE_API_KEY = os.getenv("TWELVE_API_KEY", "")

SYMBOL = "XAU/USD"
INTERVAL = "15min"


def get_market_data():

    if not TWELVE_API_KEY:
        return {
            "symbol": SYMBOL,
            "timeframe": INTERVAL,
            "bid": 0,
            "ask": 0,
            "candles": [],
            "error": "Missing Twelve Data API key"
        }


    url = "https://api.twelvedata.com/time_series"

    params = {
        "symbol": SYMBOL,
        "interval": INTERVAL,
        "outputsize": 200,
        "apikey": TWELVE_API_KEY
    }


    try:
        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        data = response.json()

        candles = []

        for candle in data.get("values", []):
            candles.append({
                "open": float(candle["open"]),
                "high": float(candle["high"]),
                "low": float(candle["low"]),
                "close": float(candle["close"])
            })


        return {
            "symbol": SYMBOL,
            "timeframe": INTERVAL,
            "bid": candles[-1]["close"] if candles else 0,
            "ask": candles[-1]["close"] if candles else 0,
            "candles": candles
        }


    except Exception as e:

        return {
            "symbol": SYMBOL,
            "timeframe": INTERVAL,
            "bid": 0,
            "ask": 0,
            "candles": [],
            "error": str(e)
        }
