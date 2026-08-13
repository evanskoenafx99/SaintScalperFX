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
        confirmations = 0


        for e in engines:

            signal = e.get("signal", "WAIT")
            score = e.get("score", 0)


            if signal == "BUY":
                buy_score += score
                confirmations += 1


            elif signal == "SELL":
                sell_score += score
                confirmations += 1



        confidence = max(
            buy_score,
            sell_score
        )


        if confirmations >= 2:
            confidence += 15

        if confirmations >= 3:
            confidence += 10

        if confirmations >= 4:
            confidence += 10


        confidence = min(confidence,100)


        signal = "WAIT"


        if buy_score > sell_score:

            if confidence >= 50:
                signal = "BUY"

            elif confidence >= 20:
                signal = "WATCH BUY"



        elif sell_score > buy_score:

            if confidence >= 50:
                signal = "SELL"

            elif confidence >= 20:
                signal = "WATCH SELL"



        return {

            "signal": signal,

            "confidence": confidence,

            "buy_score": buy_score,

            "sell_score": sell_score,

            "confirmations": confirmations,

            "engines": engines

        }
