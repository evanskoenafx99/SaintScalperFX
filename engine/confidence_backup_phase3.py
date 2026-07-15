def calculate(results):

    total_score = 0
    max_score = 0


    weights = {

        "ICT": 30,
        "SMC": 30,
        "Structure": 25,
        "Trend": 15,
        "Order Blocks": 15,
        "FVG": 15,
        "Liquidity": 10,
        "Sessions": 5,
        "Risk": 10

    }


    for engine in results:

        name = engine.get("engine")

        weight = weights.get(name, 10)

        score = engine.get("score", 0)


        total_score += min(score, weight)

        max_score += weight



    if max_score == 0:

        confidence = 0

    else:

        confidence = round(
            (total_score / max_score) * 100
        )



    if confidence >= 90:

        grade = "A"


    elif confidence >= 80:

        grade = "B"


    elif confidence >= 70:

        grade = "C"


    else:

        grade = "D"



    return {

        "confidence": confidence,

        "grade": grade

    }
