def analyze(data=None):

    risk_percent = 1.0
    max_daily_loss = 3.0
    risk_reward = "1:3"


    return {

        "engine": "Risk",

        "signal": "WAIT",

        "score": 0,

        "confidence": 100,

        "reason": "Risk parameters are acceptable.",

        "risk_percent": risk_percent,

        "max_daily_loss": max_daily_loss,

        "risk_reward": risk_reward,

        "approved": True

    }
