from engine.debug_console import DebugConsole
from engine.decision_logger import DecisionLogger
from datetime import datetime
logger = DecisionLogger()
from engine.trend import analyze as trend_analyze
from engine.structure import analyze as structure_analyze
from engine.liquidity import analyze as liquidity_analyze
from engine.fvg import analyze as fvg_analyze
from engine.orderblocks import analyze as orderblock_analyze
from engine.ict import analyze as ict_analyze
from engine.smc import analyze as smc_analyze
from engine.sessions import analyze as session_analyze
from engine.risk import analyze as risk_analyze
from engine.confidence import calculate


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

        buy_score = sum(
            r.get("score", 0)
            for r in results
            if r.get("signal") == "BUY"
        )

        sell_score = sum(
            r.get("score", 0)
            for r in results
            if r.get("signal") == "SELL"
        )

buy_votes = sum(
    1 for r in results
    if r.get("signal") == "BUY"
)

sell_votes = sum(
    1 for r in results
    if r.get("signal") == "SELL"
)

MINIMUM_AGREEMENT = 5

if buy_votes >= MINIMUM_AGREEMENT and buy_score > sell_score:
    signal = "BUY"

elif sell_votes >= MINIMUM_AGREEMENT and sell_score > buy_score:
    signal = "SELL"

else:
    signal = "WAIT"
logger.save({
    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "symbol": symbol if "symbol" in locals() else "UNKNOWN",
    "timeframe": timeframe if "timeframe" in locals() else "UNKNOWN",
    "signal": signal,
    "confidence": confidence["confidence"],
    "grade": confidence["grade"],
    "buy_score": buy_score,
    "sell_score": sell_score,
    "engines": results,
   "reason": "Multi-engine ICT + SMC analysis completed.",
"entry": entry if "entry" in locals() else None,
"stop_loss": stop_loss if "stop_loss" in locals() else None,
"take_profit": take_profit if "take_profit" in locals() else None
})

  DebugConsole.show(
    results=results,
    signal=signal,
    confidence=confidence["confidence"],
    buy_score=buy_score,
    sell_score=sell_score
)
        return {
            "signal": signal,
            "confidence": confidence["confidence"],
            "grade": confidence["grade"],
            "buy_score": buy_score,
            "sell_score": sell_score,
            "engines": results,
            "reason": "Multi-engine ICT + SMC analysis completed."
        }
