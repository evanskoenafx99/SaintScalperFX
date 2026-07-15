ENGINE_WEIGHTS = {
    "ict": 20,
    "smc": 20,
    "structure": 15,
    "trend": 10,
    "orderblock": 10,
    "fvg": 10,
    "liquidity": 5,
    "session": 5,
    "risk": 5
}


def calculate(results):

    score = 0
    maximum = sum(ENGINE_WEIGHTS.values())

    for result in results:

        engine = result.get("engine", "").lower()
        signal = result.get("signal", "").upper()

        if signal == "BUY":
            score += ENGINE_WEIGHTS.get(engine, 0)

        elif signal == "SELL":
            score += ENGINE_WEIGHTS.get(engine, 0)

    confidence = round((score / maximum) * 100)

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
        "grade": grade
    }
