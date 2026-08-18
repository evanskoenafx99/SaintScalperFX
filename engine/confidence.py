ENGINE_WEIGHTS = {
    "market intelligence": 20,
    "ict": 15,
    "smc": 15,
    "structure": 12,
    "liquidity": 10,
    "fvg": 8,
    "order blocks": 8,
    "orderblock": 8,
    "trend": 5,
    "sessions": 3,
    "session": 3,
    "momentum": 2,
    "risk": 2
}


def calculate(results):

    buy_score = 0
    sell_score = 0

    engines_found = {}

    for result in results:

        engine = result.get("engine", "").lower().strip()
        signal = result.get("signal", "WAIT").upper()

        if engine == "orderblock":
            weight = ENGINE_WEIGHTS["orderblock"]
        else:
            weight = ENGINE_WEIGHTS.get(engine, 0)

        engines_found[engine] = result

        if signal == "BUY":
            buy_score += weight

        elif signal == "SELL":
            sell_score += weight

    # --------------------------------------------------
    # MARKET INTELLIGENCE
    # --------------------------------------------------

    intelligence = engines_found.get(
        "market intelligence",
        {}
    )

    intelligence_signal = intelligence.get(
        "signal",
        "WAIT"
    )

    institutional = intelligence.get(
        "institutional_footprint",
        {}
    )

    manipulation = intelligence.get(
        "manipulation",
        "NONE"
    )

    kill_zone = intelligence.get(
        "kill_zone",
        False
    )

    price_action = intelligence.get(
        "price_action",
        {}
    )

    displacement_buy = price_action.get(
        "strong_bullish",
        False
    )

    displacement_sell = price_action.get(
        "strong_bearish",
        False
    )

    # --------------------------------------------------
    # SAINT ULTRA INSTITUTIONAL BONUSES
    # --------------------------------------------------

    if intelligence_signal == "BUY":

        if institutional.get("bullish"):
            buy_score += 5

        if manipulation == "SELL_SIDE_SWEEP":
            buy_score += 5

        if displacement_buy:
            buy_score += 5

        if kill_zone:
            buy_score += 5

    elif intelligence_signal == "SELL":

        if institutional.get("bearish"):
            sell_score += 5

        if manipulation == "BUY_SIDE_SWEEP":
            sell_score += 5

        if displacement_sell:
            sell_score += 5

        if kill_zone:
            sell_score += 5

    # --------------------------------------------------
    # FINAL DIRECTION
    # --------------------------------------------------

    if buy_score > sell_score:
        direction = "BUY"
        score = buy_score

    elif sell_score > buy_score:
        direction = "SELL"
        score = sell_score

    else:
        direction = "WAIT"
        score = 0

    # Maximum possible practical score:
    # 100 base points + 20 institutional bonuses.
    maximum = 120

    confidence = round(
        (score / maximum) * 100
    )

    confidence = min(confidence, 100)

    # --------------------------------------------------
    # SAINT ULTRA GRADE
    # --------------------------------------------------

    if confidence >= 90:
        grade = "A+"

    elif confidence >= 80:
        grade = "A"

    elif confidence >= 70:
        grade = "B"

    elif confidence >= 60:
        grade = "C"

    else:
        grade = "D"

    # --------------------------------------------------
    # INSTITUTIONAL SETUP STATUS
    # --------------------------------------------------

    core_confirmations = {
        "ict": engines_found.get(
            "ict", {}
        ).get("signal") == direction,

        "smc": engines_found.get(
            "smc", {}
        ).get("signal") == direction,

        "market_intelligence":
            intelligence_signal == direction,

        "structure":
            engines_found.get(
                "structure", {}
            ).get("signal") == direction,

        "fvg":
            engines_found.get(
                "fvg", {}
            ).get("signal") == direction,

        "liquidity":
            engines_found.get(
                "liquidity", {}
            ).get("signal") == direction
    }

    confirmed_count = sum(
        core_confirmations.values()
    )

    setup_confirmed = (
        direction != "WAIT"
        and confirmed_count >= 4
    )

    # A/A+ requires a genuine institutional setup.
    if not setup_confirmed:
        confidence = min(confidence, 79)

        if confidence < 70:
            grade = "C" if confidence >= 60 else "D"
        else:
            grade = "B"

    return {
        "confidence": confidence,
        "grade": grade,
        "direction": direction,
        "score": score,
        "maximum": maximum,

        "buy_score": buy_score,
        "sell_score": sell_score,

        "core_confirmations": confirmed_count,

        "ict_confirmed":
            core_confirmations["ict"],

        "smc_confirmed":
            core_confirmations["smc"],

        "market_intelligence_confirmed":
            core_confirmations["market_intelligence"],

        "structure_confirmed":
            core_confirmations["structure"],

        "fvg_confirmed":
            core_confirmations["fvg"],

        "liquidity_confirmed":
            core_confirmations["liquidity"],

        "institutional_footprint":
            institutional,

        "manipulation":
            manipulation,

        "kill_zone":
            kill_zone,

        "setup_confirmed":
            setup_confirmed
    }
