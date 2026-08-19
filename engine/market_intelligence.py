from datetime import datetime


def analyze(candles, session=None):
    """
    SaintScalperFX Market Intelligence

    Higher-level market-context engine combining:
    - Market structure
    - HH / HL / LH / LL
    - High/low hierarchy
    - Liquidity
    - Manipulation clues
    - Institutional footprint
    - Price action
    - Trend
    - Kill-zone awareness
    """

    if len(candles) < 30:
        return {
            "engine": "Market Intelligence",
            "signal": "WAIT",
            "score": 0,
            "confidence": 0,
            "reason": "Not enough market data."
        }

    current = candles[-1]
    previous = candles[-2]

    highs = [c["high"] for c in candles]
    lows = [c["low"] for c in candles]
    closes = [c["close"] for c in candles]
    opens = [c["open"] for c in candles]

    current_close = current["close"]

    # --------------------------------------------------
    # HIGH / LOW HIERARCHY
    # --------------------------------------------------

    recent_high = max(highs[-20:])
    recent_low = min(lows[-20:])

    highest_high = max(highs)
    lowest_low = min(lows)

    previous_high = max(highs[-30:-1])
    previous_low = min(lows[-30:-1])

    # --------------------------------------------------
    # BASIC STRUCTURE
    # --------------------------------------------------

    hh = current["high"] > previous["high"]
    hl = current["low"] > previous["low"]

    lh = current["high"] < previous["high"]
    ll = current["low"] < previous["low"]

    bullish_structure = hh and hl
    bearish_structure = lh and ll

    # --------------------------------------------------
    # BREAK OF STRUCTURE
    # --------------------------------------------------

    bullish_bos = current_close > previous_high
    bearish_bos = current_close < previous_low

    # --------------------------------------------------
    # LIQUIDITY SWEEPS
    # --------------------------------------------------

    swept_high = current["high"] > previous_high
    swept_low = current["low"] < previous_low

    bearish_rejection = (
        swept_high and
        current_close < previous_high
    )

    bullish_rejection = (
        swept_low and
        current_close > previous_low
    )

    # --------------------------------------------------
    # PRICE ACTION
    # --------------------------------------------------

    body = abs(current["close"] - current["open"])
    candle_range = current["high"] - current["low"]

    if candle_range > 0:
        body_ratio = body / candle_range
    else:
        body_ratio = 0

    bullish_candle = current["close"] > current["open"]
    bearish_candle = current["close"] < current["open"]

    strong_bullish = (
        bullish_candle and
        body_ratio >= 0.60
    )

    strong_bearish = (
        bearish_candle and
        body_ratio >= 0.60
    )

    # --------------------------------------------------
    # DISPLACEMENT / INSTITUTIONAL FOOTPRINT
    # --------------------------------------------------

    previous_range = previous["high"] - previous["low"]

    bullish_displacement = (
        strong_bullish and
        candle_range > previous_range * 1.3
    )

    bearish_displacement = (
        strong_bearish and
        candle_range > previous_range * 1.3
    )

    institutional_buy = (
        bullish_rejection or
        bullish_displacement or
        bullish_bos
    )

    institutional_sell = (
        bearish_rejection or
        bearish_displacement or
        bearish_bos
    )

    # --------------------------------------------------
    # MANIPULATION MODEL
    # --------------------------------------------------

    manipulation = "NONE"

    if bullish_rejection:
        manipulation = "SELL_SIDE_SWEEP"

    elif bearish_rejection:
        manipulation = "BUY_SIDE_SWEEP"

    # --------------------------------------------------
    # TREND BIAS
    # --------------------------------------------------

    midpoint = (recent_high + recent_low) / 2

    if current_close > midpoint:
        trend = "BULLISH"
    elif current_close < midpoint:
        trend = "BEARISH"
    else:
        trend = "NEUTRAL"

    # --------------------------------------------------
    # SESSION / KILL ZONE
    # --------------------------------------------------

    hour = datetime.utcnow().hour

    current_session = "Closed"
    kill_zone = False

    if 0 <= hour < 7:
        current_session = "Asian"

    elif 7 <= hour < 12:
        current_session = "London"

        if 7 <= hour < 10:
            kill_zone = True

    elif 12 <= hour < 21:
        current_session = "New York"

        if 12 <= hour < 15:
            kill_zone = True

    # --------------------------------------------------
    # SIGNAL SCORING
    # --------------------------------------------------

    buy_score = 0
    sell_score = 0

    reasons = []

    if bullish_structure:
        buy_score += 10
        reasons.append("Bullish HH/HL structure")

    if bearish_structure:
        sell_score += 10
        reasons.append("Bearish LH/LL structure")

    if bullish_bos:
        buy_score += 15
        reasons.append("Bullish BOS")

    if bearish_bos:
        sell_score += 15
        reasons.append("Bearish BOS")

    if bullish_rejection:
        buy_score += 20
        reasons.append("Sell-side liquidity sweep")

    if bearish_rejection:
        sell_score += 20
        reasons.append("Buy-side liquidity sweep")

    if bullish_displacement:
        buy_score += 15
        reasons.append("Bullish displacement")

    if bearish_displacement:
        sell_score += 15
        reasons.append("Bearish displacement")

    if trend == "BULLISH":
        buy_score += 10

    elif trend == "BEARISH":
        sell_score += 10

    if kill_zone:
        if buy_score > sell_score:
            buy_score += 5
        elif sell_score > buy_score:
            sell_score += 5

    # --------------------------------------------------
    # FINAL SIGNAL
    # --------------------------------------------------

    signal = "WAIT"

    if buy_score >= 40 and buy_score > sell_score:
        signal = "BUY"

    elif sell_score >= 40 and sell_score > buy_score:
        signal = "SELL"

    score = max(buy_score, sell_score)

    confidence = min(score * 2, 95)

    # --------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------

    return {
        "engine": "Market Intelligence",

        "signal": signal,

        "score": score,

        "confidence": confidence,

        "buy_score": buy_score,

        "sell_score": sell_score,

        "trend": trend,

        "structure": {
            "hh": hh,
            "hl": hl,
            "lh": lh,
            "ll": ll,
            "bullish_structure": bullish_structure,
            "bearish_structure": bearish_structure,
            "bullish_bos": bullish_bos,
            "bearish_bos": bearish_bos
        },

        "liquidity": {
            "swept_high": swept_high,
            "swept_low": swept_low,
            "buy_side_sweep": bearish_rejection,
            "sell_side_sweep": bullish_rejection
        },

        "institutional_footprint": {
            "bullish": institutional_buy,
            "bearish": institutional_sell,
            "bullish_displacement": bullish_displacement,
            "bearish_displacement": bearish_displacement
        },

        "manipulation": manipulation,

        "price_action": {
            "body_ratio": round(body_ratio, 3),
            "strong_bullish": strong_bullish,
            "strong_bearish": strong_bearish
        },

        "levels": {
            "recent_high": recent_high,
            "recent_low": recent_low,
            "highest_high": highest_high,
            "lowest_low": lowest_low,
            "previous_high": previous_high,
            "previous_low": previous_low
        },

        "session": current_session,

        "kill_zone": kill_zone,

        "reason": ", ".join(reasons)
        if reasons
        else "No strong institutional setup."
    }
