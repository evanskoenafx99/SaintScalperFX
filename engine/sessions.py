from datetime import datetime

def analyze(data=None):

    hour = datetime.utcnow().hour

    session = "Closed"

    if 0 <= hour < 7:
        session = "Asian"

    elif 7 <= hour < 12:
        session = "London"

    elif 12 <= hour < 21:
        session = "New York"

    score = 15 if session in ["London", "New York"] else 5

    return {
        "engine": "Sessions",
        "signal": "WAIT",
        "score": score,
        "confidence": 80,
        "reason": f"Current session: {session}",
        "session": session
    }
