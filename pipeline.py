from core.brain import SaintScalperBrain
from planner import TradePlanner
from execution import ExecutionEngine


class SaintScalperPipeline:

    def __init__(self):

        self.brain = SaintScalperBrain()
        self.planner = TradePlanner()
        self.execution = ExecutionEngine()

    def analyze(self, candles):

        decision = self.brain.analyze(candles)

        plan = self.planner.create(
            signal=decision["signal"],
            entry=0.0,
            stop_loss=0.0,
            take_profit=0.0,
            confidence=decision["confidence"],
            grade=decision["grade"]
        )

        execution = self.execution.prepare_order(plan)

        return {
            "decision": decision,
            "plan": plan,
            "execution": execution
        }
