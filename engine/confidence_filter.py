from engine.confidence import calculate


def evaluate_confidence(confidence=None, engines=None):

    # New unified mode
    if engines is not None:

        result = calculate(engines)

        return {
            "status": (
                "APPROVED"
                if result["setup_confirmed"]
                else "WAIT"
            ),

            "grade": result["grade"],

            "message": (
                "Saint Ultra setup confirmed."
                if result["setup_confirmed"]
                else "Institutional confirmation incomplete."
            ),

            "confidence": result["confidence"],

            "setup_confirmed":
                result["setup_confirmed"],

            "details": result
        }

    # Compatibility mode for older callers
    if confidence is None:
        confidence = 0

    confidence = float(
        str(confidence).replace("%", "")
    )

    if confidence >= 90:

        return {
            "status": "APPROVED",
            "grade": "A+",
            "message": "Saint Ultra high-confidence setup.",
            "confidence": confidence,
            "setup_confirmed": True
        }

    elif confidence >= 80:

        return {
            "status": "APPROVED",
            "grade": "A",
            "message": "High probability setup.",
            "confidence": confidence,
            "setup_confirmed": False
        }

    elif confidence >= 60:

        return {
            "status": "CAUTION",
            "grade": "B",
            "message": "Moderate setup. Wait for confirmation.",
            "confidence": confidence,
            "setup_confirmed": False
        }

    else:

        return {
            "status": "WAIT",
            "grade": "C",
            "message": "Low confidence. No trade.",
            "confidence": confidence,
            "setup_confirmed": False
        }
