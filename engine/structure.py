def analyze(candles):
    if len(candles) < 20:
        return {
            "engine": "Structure",
            "signal": "WAIT",
            "score": 0,
            "confidence": 0,
            "reason": "Not enough candles."
        }

    highs = [float(c["high"]) for c in candles]
    lows = [float(c["low"]) for c in candles]
    closes = [float(c["close"]) for c in candles]
    opens = [float(c.get("open", c["close"])) for c in candles]

    current_close = closes[-1]
    current_open = opens[-1]

    # ---------------------------------------------------------
    # 1. Recent range
    # ---------------------------------------------------------
    swing_high = max(highs[-20:-1])
    swing_low = min(lows[-20:-1])

    range_size = swing_high - swing_low

    if range_size <= 0:
        return {
            "engine": "Structure",
            "signal": "WAIT",
            "score": 0,
            "confidence": 0,
            "reason": "Invalid market range."
        }

    # ---------------------------------------------------------
    # 2. Immediate candle structure
    # ---------------------------------------------------------
    hh = highs[-1] > highs[-2]
    hl = lows[-1] > lows[-2]
    lh = highs[-1] < highs[-2]
    ll = lows[-1] < lows[-2]

    # ---------------------------------------------------------
    # 3. Recent multi-candle structure
    #
    # Look beyond only the previous candle.
    # This allows the engine to recognize developing trends.
    # ---------------------------------------------------------
    recent_highs = highs[-6:]
    recent_lows = lows[-6:]

    higher_high_count = 0
    lower_high_count = 0
    higher_low_count = 0
    lower_low_count = 0

    for i in range(1, len(recent_highs)):
        if recent_highs[i] > recent_highs[i - 1]:
            higher_high_count += 1
        elif recent_highs[i] < recent_highs[i - 1]:
            lower_high_count += 1

        if recent_lows[i] > recent_lows[i - 1]:
            higher_low_count += 1
        elif recent_lows[i] < recent_lows[i - 1]:
            lower_low_count += 1

    # ---------------------------------------------------------
    # 4. Recent displacement
    #
    # Compare the latest candle body with recent average bodies.
    # ---------------------------------------------------------
    bodies = [
        abs(closes[i] - opens[i])
        for i in range(max(0, len(candles) - 10), len(candles) - 1)
    ]

    average_body = sum(bodies) / len(bodies) if bodies else 0
    current_body = abs(current_close - current_open)

    bullish_displacement = (
        current_close > current_open
        and average_body > 0
        and current_body >= average_body * 1.25
    )

    bearish_displacement = (
        current_close < current_open
        and average_body > 0
        and current_body >= average_body * 1.25
    )

    # ---------------------------------------------------------
    # 5. Position inside recent range
    #
    # Being close to one side of the range provides context
    # even before an absolute breakout occurs.
    # ---------------------------------------------------------
    range_position = (current_close - swing_low) / range_size

    near_high = range_position >= 0.75
    near_low = range_position <= 0.25

    # ---------------------------------------------------------
    # 6. True Break of Structure
    #
    # Keep the old breakout logic as strong confirmation,
    # but DON'T require it for every signal.
    # ---------------------------------------------------------
    bullish_bos = current_close > swing_high
    bearish_bos = current_close < swing_low

    # ---------------------------------------------------------
    # 7. Directional structure scoring
    # ---------------------------------------------------------
    bullish_score = 0
    bearish_score = 0

    bullish_reasons = []
    bearish_reasons = []

    # Immediate structure
    if hh:
        bullish_score += 12
        bullish_reasons.append("higher high")

    if hl:
        bullish_score += 12
        bullish_reasons.append("higher low")

    if lh:
        bearish_score += 12
        bearish_reasons.append("lower high")

    if ll:
        bearish_score += 12
        bearish_reasons.append("lower low")

    # Multi-candle structure
    if higher_high_count >= 2:
        bullish_score += 15
        bullish_reasons.append("developing higher highs")

    if higher_low_count >= 2:
        bullish_score += 15
        bullish_reasons.append("developing higher lows")

    if lower_high_count >= 2:
        bearish_score += 15
        bearish_reasons.append("developing lower highs")

    if lower_low_count >= 2:
        bearish_score += 15
        bearish_reasons.append("developing lower lows")

    # Displacement
    if bullish_displacement:
        bullish_score += 18
        bullish_reasons.append("bullish displacement")

    if bearish_displacement:
        bearish_score += 18
        bearish_reasons.append("bearish displacement")

    # Range context
    if near_high:
        bullish_score += 8
        bullish_reasons.append("price near range high")

    if near_low:
        bearish_score += 8
        bearish_reasons.append("price near range low")

    # Real BOS gets the strongest structural confirmation
    if bullish_bos:
        bullish_score += 25
        bullish_reasons.append("bullish break of structure")

    if bearish_bos:
        bearish_score += 25
        bearish_reasons.append("bearish break of structure")

    # ---------------------------------------------------------
    # 8. Determine structure
    # ---------------------------------------------------------
    signal = "WAIT"
    trend = "RANGING"
    structure = "Sideways"
    confidence = 35
    score = 0
    reason = "No clear directional structure."

    # Strong bullish structure
    if bullish_score >= 45 and bullish_score > bearish_score + 10:
        signal = "BUY"
        trend = "UPTREND"
        structure = "Bullish"
        score = min(bullish_score, 100)

        confidence = min(
            95,
            50 + int(score * 0.45)
        )

        reason = "Bullish structure: " + ", ".join(bullish_reasons)

    # Strong bearish structure
    elif bearish_score >= 45 and bearish_score > bullish_score + 10:
        signal = "SELL"
        trend = "DOWNTREND"
        structure = "Bearish"
        score = min(bearish_score, 100)

        confidence = min(
            95,
            50 + int(score * 0.45)
        )

        reason = "Bearish structure: " + ", ".join(bearish_reasons)

    # Developing but not yet directional enough
    else:
        if bullish_score > bearish_score:
            trend = "DEVELOPING_UP"
            structure = "Developing Bullish"
            score = bullish_score
            reason = (
                "Developing bullish structure: "
                + ", ".join(bullish_reasons)
                if bullish_reasons
                else "Bullish structure developing."
            )

        elif bearish_score > bullish_score:
            trend = "DEVELOPING_DOWN"
            structure = "Developing Bearish"
            score = bearish_score
            reason = (
                "Developing bearish structure: "
                + ", ".join(bearish_reasons)
                if bearish_reasons
                else "Bearish structure developing."
            )

        else:
            score = 0

    # ---------------------------------------------------------
    # 9. CHOCH detection
    # ---------------------------------------------------------
    choch = False

    if trend in ("UPTREND", "DEVELOPING_UP") and lh:
        choch = True

    if trend in ("DOWNTREND", "DEVELOPING_DOWN") and hl:
        choch = True

    return {
        "engine": "Structure",
        "signal": signal,
        "score": score,
        "confidence": confidence,
        "reason": reason,

        "structure": structure,
        "trend": trend,

        "bos": bullish_bos or bearish_bos,
        "choch": choch,

        "hh": hh,
        "hl": hl,
        "lh": lh,
        "ll": ll,

        "higher_high_count": higher_high_count,
        "lower_high_count": lower_high_count,
        "higher_low_count": higher_low_count,
        "lower_low_count": lower_low_count,

        "bullish_displacement": bullish_displacement,
        "bearish_displacement": bearish_displacement,

        "bullish_score": bullish_score,
        "bearish_score": bearish_score,

        "swing_high": swing_high,
        "swing_low": swing_low,
        "current_close": current_close,
        "range_position": range_position
    }
