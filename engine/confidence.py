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


    maximum = sum(
        ENGINE_WEIGHTS.values()
    )


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



    score = max(
        buy_score,
        sell_score
    )


    confidence = round(
        (score / maximum) * 100
    )



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

        "sell_score": sell_score

    }
