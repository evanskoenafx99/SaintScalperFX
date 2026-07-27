from engine.ai import SaintScalperBrain
from execution import ExecutionEngine
from trade_manager import TradeManager


class SaintTradingController:


    def __init__(self):

        self.ai = SaintScalperBrain()

        self.execution = ExecutionEngine()

        self.manager = TradeManager()



    def analyze_market(self, candles):

        analysis = self.ai.analyze(candles)

        return analysis



    def process_trade(self, analysis):

        plan = {

            "signal": analysis.get("signal"),

            "confidence": analysis.get("confidence"),

            "grade": analysis.get("grade"),

            "entry": "AUTO",

            "stop_loss": "AUTO",

            "take_profit": "AUTO"

        }


        decision = self.execution.prepare_order(plan)


        if decision.get("approved"):

            self.manager.add_trade(decision)


        return decision
