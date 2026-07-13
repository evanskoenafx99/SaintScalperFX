from engine.trend import analyze as trend
from engine.structure import analyze as structure
from engine.liquidity import analyze as liquidity
from engine.fvg import analyze as fvg
from engine.orderblocks import analyze as orderblocks
from engine.sessions import analyze as sessions
from engine.risk import analyze as risk
from engine.confidence import calculate


class SaintScalperBrain:

    def analyze(self, candles):

        results = []

        results.append(trend(candles))
        results.append(structure(candles))
        results.append(liquidity(candles))
        results.append(fvg(candles))
        results.append(orderblocks(candles))
        results.append(sessions())
        results.append(risk())

        buy = 0
        sell = 0
        wait = 0

        for result in results:

            if result["signal"] == "BUY":
                buy += result["score"]

            elif result["signal"] == "SELL":
                sell += result["score"]

            else:
                wait += result["score"]

        if buy > sell and buy > wait:
            signal = "BUY"

        elif sell > buy and sell > wait:
            signal = "SELL"

        else:
            signal = "WAIT"

        confidence = calculate(results)

        return {
            "signal": signal,
            "confidence": confidence["confidence"],
            "grade": confidence["grade"],
            "results": results
        }
