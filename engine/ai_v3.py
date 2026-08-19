# ============================================================
# SaintScalperFX AI V3.0
# Core Intelligence Engine
# ============================================================

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

from engine.confidence import calculate

logger = DecisionLogger()


class SaintScalperBrain:

    def __init__(self):

        self.minimum_agreement = 5

        self.engines = [

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

    # =========================================================
    # MAIN AI ANALYSIS
    # =========================================================

    def analyze(self, candles):

        results = []

        for engine in self.engines:

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

            1

            for r in results

            if r.get("signal") == "BUY"

        )

        sell_votes = sum(

            1

            for r in results

            if r.get("signal") == "SELL"

        )
        # =====================================================
        # DECISION ENGINE
        # =====================================================

        if buy_votes >= self.minimum_agreement and buy_score > sell_score:

            signal = "BUY"

        elif sell_votes >= self.minimum_agreement and sell_score > buy_score:

            signal = "SELL"

        else:

            signal = "WAIT"

        # =====================================================
        # TREND DETECTION
        # =====================================================

        if buy_score > sell_score:

            trend = "BULLISH"

        elif sell_score > buy_score:

            trend = "BEARISH"

        else:

            trend = "SIDEWAYS"

        # =====================================================
        # ENTRY PRICE
        # =====================================================

        current_price = candles[-1]["close"]

        entry = round(current_price, 2)

        # =====================================================
        # STOP LOSS
        # =====================================================

        if signal == "BUY":

            stop_loss = round(entry - 5.00, 2)

        elif signal == "SELL":

            stop_loss = round(entry + 5.00, 2)

        else:

            stop_loss = None

        # =====================================================
        # TAKE PROFIT
        # =====================================================

        if signal == "BUY":

            take_profit = round(entry + 10.00, 2)

        elif signal == "SELL":

            take_profit = round(entry - 10.00, 2)

        else:

            take_profit = None

        # =====================================================
        # RISK : REWARD
        # =====================================================

        if signal == "WAIT":

            risk_reward = 0

        else:

            reward = abs(take_profit - entry)

            risk = abs(entry - stop_loss)

            if risk == 0:

                risk_reward = 0

            else:

                risk_reward = round(reward / risk, 2)
        # =====================================================
        # AI SUMMARY
        # =====================================================

        reason = (
            "Multi-engine ICT + SMC analysis completed."
        )

        # =====================================================
        # SAVE DECISION
        # =====================================================

        logger.save({

            "time": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "symbol": "UNKNOWN",

            "timeframe": "UNKNOWN",

            "signal": signal,

            "confidence": confidence["confidence"],

            "grade": confidence["grade"],

            "buy_score": buy_score,

            "sell_score": sell_score,

            "trend": trend,

            "entry": entry,

            "stop_loss": stop_loss,

            "take_profit": take_profit,

            "risk_reward": risk_reward,

            "engines": results,

            "reason": reason

        })

        # =====================================================
        # DEBUG CONSOLE
        # =====================================================

        DebugConsole.show(

            results=results,

            signal=signal,

            confidence=confidence["confidence"],

            buy_score=buy_score,

            sell_score=sell_score

        )

        # =====================================================
        # FINAL AI OUTPUT
        # =====================================================

        response = {

            "signal": signal,

            "confidence": confidence["confidence"],

            "grade": confidence["grade"],

            "trend": trend,

            "entry": entry,

            "stop_loss": stop_loss,

            "take_profit": take_profit,

            "risk_reward": risk_reward,

            "buy_score": buy_score,

            "sell_score": sell_score,

            "engines": results,

            "reason": reason

        }
        # =====================================================
        # RETURN RESPONSE
        # =====================================================

        return response


# ============================================================
# END OF FILE
# SaintScalperFX AI V3.0
# ============================================================
