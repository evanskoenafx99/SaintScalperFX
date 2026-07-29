from engine.trend import analyze as trend_analyze
from engine.structure import analyze as structure_analyze
from engine.liquidity import analyze as liquidity_analyze
from engine.fvg import analyze as fvg_analyze
from engine.orderblocks import analyze as orderblocks_analyze
from engine.ict import analyze as ict_analyze
from engine.smc import analyze as smc_analyze
from engine.sessions import analyze as sessions_analyze
from engine.momentum import analyze as momentum_analyze
from engine.risk import analyze as risk_analyze


class SaintScalperBrain:

    def __init__(self):
        pass


    def analyze(self, candles):

        engines = [
            trend_analyze,
            structure_analyze,
            liquidity_analyze,
            fvg_analyze,
            orderblocks_analyze,
            ict_analyze,
            smc_analyze,
            sessions_analyze,
            momentum_analyze,
            risk_analyze
        ]


        results = []

        buy_score = 0
        sell_score = 0


        for engine in engines:

            try:
                result = engine(candles)

            except Exception as e:

                result = {
                    "engine": engine.__name__,
                    "signal": "WAIT",
                    "score": 0,
                    "confidence": 0,
                    "reason": str(e)
                }


            results.append(result)


            signal = result.get("signal","WAIT").upper()
            score = result.get("score",0)


            if signal == "BUY":
                buy_score += score

            elif signal == "SELL":
                sell_score += score



        signal = "WAIT"


        # SaintScalperFX decision model

        if buy_score >= 40 and buy_score > sell_score:
            signal = "BUY"


        elif sell_score >= 40 and sell_score > buy_score:
            signal = "SELL"



        confidence = max(
            buy_score,
            sell_score
        )

        if confidence > 100:
            confidence = 100



        return {

            "signal": signal,

            "confidence": confidence,

            "buy_score": buy_score,

            "sell_score": sell_score,

            "engines": results
        }
