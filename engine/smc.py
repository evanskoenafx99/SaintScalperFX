def analyze(data=None):

    return {
        "engine": "SMC",
        "signal": "WAIT",
        "score": 10,
        "confidence": 50,
        "reason": "SMC engine waiting for live MT5 data.",
        "bos": False,
        "choch": False,
        "orderblock": False,
        "liquidity": False
    }
