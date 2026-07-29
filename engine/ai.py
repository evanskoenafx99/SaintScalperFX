from engine.trend import analyze as trend
from engine.structure import analyze as structure
from engine.liquidity import analyze as liquidity
from engine.fvg import analyze as fvg
from engine.orderblocks import analyze as orderblocks
from engine.ict import analyze as ict
from engine.smc import analyze as smc
from engine.sessions import analyze as sessions
from engine.momentum import analyze as momentum
from engine.risk import analyze as risk


class SaintScalperBrain:

    def analyze(self, candles):

        engines = [
            trend(candles),
            structure(candles),
            liquidity(candles),
            fvg(candles),
            orderblocks(candles),
            ict(candles),
            smc(candles),
            sessions(candles),
            momentum(candles),
            risk(candles)
        ]

        buy_score = 0
        sell_score = 0


        for e in engines:

            signal = e.get("signal","WAIT")
            score = e.get("score",0)

            if signal == "BUY":
                buy_score += score

            if signal == "SELL":
                sell_score += score


        signal = "WAIT"


        # New SaintScalperFX decision logic

        if buy_score >= 25 and buy_score > sell_score:
            signal = "BUY"

        elif sell_score >= 25 and sell_score > buy_score:
            signal = "SELL"


        confidence = min(
            max(buy_score, sell_score),
            100
        )


        return {

            "signal": signal,

            "confidence": confidence,

            "buy_score": buy_score,

            "sell_score": sell_score,

            "engines": engines
        }
