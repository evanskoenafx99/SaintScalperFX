from datetime import datetime
from engine.debug_console import DebugConsole
from engine.decision_logger import DecisionLogger
from engine.trend import analyze as trend_analyze
from engine.structure import analyze as structure_analyze
from engine.liquidity import analyze as liquidity_analyze
from engine.fvg import analyze as fvg_analyze
from engine.orderblocks import analyze as orderblock_analyze
from engine.ict import analyze as ict_analyze
from engine.smc import analyze as smc_analyze
from engine.sessions import analyze as session_analyze
from engine.risk import analyze as risk_analyze
from engine.momentum import analyze as momentum_analyze
from engine.confidence import calculate
from engine.trade_plan import generate_trade_plan

logger = DecisionLogger()


class SaintScalperBrain:


    def analyze(self, candles):

        results = []

        engines = [
            trend_analyze,
            structure_analyze,
            liquidity_analyze,
            fvg_analyze,
            orderblock_analyze,
            ict_analyze,
            smc_analyze,
            session_analyze,
            momentum_analyze,
            risk_analyze
        ]



        for engine in engines:

            try:

                result = engine(candles)
                results.append(result)


            except Exception as e:

                results.append({
                    "engine": engine.__name__,
                    "signal": "WAIT",
                    "score": 0,
                    "confidence": 0,
                    "reason": str(e)
                })



        confidence = calculate(results)



        buy_score = 0
        sell_score = 0

        buy_votes = 0
        sell_votes = 0



        risk_ok = True



        for r in results:

            name = r.get("engine","").lower()
            signal = r.get("signal","WAIT").upper()
            score = r.get("score",0)


            if "risk" in name:

                continue


            if signal == "BUY":

                buy_score += score
                buy_votes += 1


            elif signal == "SELL":

                sell_score += score
                sell_votes += 1



        if buy_votes >= 4 and buy_score > sell_score:

            signal = "BUY"


        elif sell_votes >= 4 and sell_score > buy_score:

            signal = "SELL"


        else:

            signal = "WAIT"



        if confidence["confidence"] < 60:

            signal = "WAIT"



        logger.save({

            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            "symbol": "UNKNOWN",

            "timeframe": "UNKNOWN",

            "signal": signal,

            "confidence": confidence["confidence"],

            "grade": confidence["grade"],

            "score": confidence["score"],

            "maximum": confidence["maximum"],

            "buy_score": buy_score,

            "sell_score": sell_score,

            "engines": results,

            "reason": "Multi-engine ICT + SMC analysis completed.",

            "entry": None,

            "stop_loss": None,

            "take_profit": None

        })



        DebugConsole.show(

            results=results,

            signal=signal,

            confidence=confidence["confidence"],

            buy_score=buy_score,

            sell_score=sell_score

        )

        momentum = "NEUTRAL"

        for engine in results:
            if engine.get("engine") == "Momentum":
                momentum = engine.get("momentum", "NEUTRAL")
                break

        trade_plan = generate_trade_plan(
            signal=signal,
            pattern="UNKNOWN",
            momentum=momentum,
            levels={},
            engines=results
        )

        return {
            "signal": signal,
            "confidence": confidence["confidence"],
            "grade": confidence["grade"],
            "score": confidence["score"],
            "maximum": confidence["maximum"],
            "buy_score": buy_score,
            "sell_score": sell_score,
            "engines": results,
            "trade_plan": trade_plan,
            "reason": "Multi-engine ICT + SMC analysis completed."
        }
