import requests
import time

TWELVE_API_KEY = "3fe85ef54ad5432e8361353bf1511a12"

SYMBOL = "XAU/USD"
INTERVAL = "15min"

_last_market = {
    "symbol": SYMBOL,
    "timeframe": INTERVAL,
    "bid": 0,
    "ask": 0,
    "candles": []
}


def get_market_data():

    global _last_market

    url = "https://api.twelvedata.com/time_series"

    params = {
        "symbol": SYMBOL,
        "interval": INTERVAL,
        "outputsize": 200,
        "apikey": TWELVE_API_KEY
    }

    for _ in range(3):

        try:

            response = requests.get(
                url,
                params=params,
                timeout=10
            )

            response.raise_for_status()

            data = response.json()

            if "status" in data and data["status"] == "error":
                print("Twelve Data error:", data.get("message"))
                return _last_market

            values = data.get("values", [])

            if values:

                candles = []

                for candle in values:

                    candles.append({
                        "open": float(candle["open"]),
                        "high": float(candle["high"]),
                        "low": float(candle["low"]),
                        "close": float(candle["close"])
                    })

                # Twelve Data returns newest -> oldest.
                # AI analysis should receive oldest -> newest.
                candles.reverse()

                latest_price = candles[-1]["close"]

                _last_market = {
                    "symbol": SYMBOL,
                    "timeframe": INTERVAL,
                    "bid": latest_price,
                    "ask": latest_price,
                    "candles": candles
                }

                return _last_market

        except Exception as e:

            print("Twelve Data connection error:", e)

        time.sleep(1)

    return _last_market
