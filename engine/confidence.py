ENGINE_WEIGHTS = {
    "ict": 20,
    "smc": 20,
    "structure": 15,
    "trend": 10,
    "order blocks": 10,
    "orderblock": 10,
    "fvg": 10,
    "liquidity": 5,
    "session": 5,
    "momentum": 5
}


def calculate(results):

    buy_score = 0
    sell_score = 0

    maximum = sum(ENGINE_WEIGHTS.values())

    ict_ok = False
    smc_ok = False
    structure_ok = False
    fvg_ok = False
    liquidity_ok = False


    for result in results:

        engine = result.get(
            "engine",
            ""
        ).lower()

        signal = result.get(
            "signal",
            ""
        ).upper()


        weight = ENGINE_WEIGHTS.get(
            engine,
            0
        )


        if signal == "BUY":
            buy_score += weight


        elif signal == "SELL":
            sell_score += weight


        if "ict" in engine and signal != "WAIT":
            ict_ok = True

        if "smc" in engine and signal != "WAIT":
            smc_ok = True

        if "structure" in engine and signal != "WAIT":
            structure_ok = True

        if "fvg" in engine and signal != "WAIT":
            fvg_ok = True

        if "liquidity" in engine and signal != "WAIT":
            liquidity_ok = True



    score = max(
        buy_score,
        sell_score
    )


    confidence = round(
        (score / maximum) * 100
    )


    # ICT + SMC execution gate
    setup_confirmed = (
        ict_ok
        and smc_ok
        and structure_ok
        and fvg_ok
        and liquidity_ok
    )


    if not setup_confirmed:
        confidence = min(confidence, 75)


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


    return {

        "confidence": confidence,

        "grade": grade,

        "score": score,

        "maximum": maximum,

        "buy_score": buy_score,

        "sell_score": sell_score,

        "ict_confirmed": ict_ok,

        "smc_confirmed": smc_ok,

        "structure_confirmed": structure_ok,

        "fvg_confirmed": fvg_ok,

        "liquidity_confirmed": liquidity_ok
    }
