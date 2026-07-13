def calculate(results):

    total_score = 0
    max_score = 0

    for engine in results:
        total_score += engine.get("score", 0)
        max_score += 20

    if max_score == 0:
        confidence = 0
    else:
        confidence = round((total_score / max_score) * 100)

    if confidence >= 95:
        grade = "A+"

    elif confidence >= 90:
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
