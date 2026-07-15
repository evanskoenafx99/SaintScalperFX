def evaluate_confidence(confidence):

    confidence = float(
        str(confidence).replace("%", "")
    )


    if confidence >= 80:

        return {
            "status": "APPROVED",
            "grade": "A",
            "message": "High probability setup."
        }


    elif confidence >= 60:

        return {
            "status": "CAUTION",
            "grade": "B",
            "message": "Moderate setup. Wait for confirmation."
        }


    else:

        return {
            "status": "WAIT",
            "grade": "C",
            "message": "Low confidence. No trade."
        }
