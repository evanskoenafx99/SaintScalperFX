from engine.ai import SaintScalperBrain
from execution import ExecutionEngine
from trade_manager import TradeManager
from core.account_manager import SaintAccountManager


class SaintTradingController:


    def __init__(self):

        self.ai = SaintScalperBrain()

        self.execution = ExecutionEngine()

        self.manager = TradeManager()

        self.accounts = SaintAccountManager()



    def analyze_market(self, candles):

        return self.ai.analyze(candles)



    def process_trade(
        self,
        user_id,
        analysis,
        symbol="XAUUSD"
    ):


        # 1. Check customer permissions first

        account_status = self.accounts.can_trade(
            user_id
        )


        if not account_status["allowed"]:

            return {

                "approved": False,

                "saved": False,

                "reason": "Account permissions blocked.",

                "account_status": account_status

            }



        # 2. Prepare execution plan

        plan = {

            "signal": analysis.get("signal"),

            "confidence": analysis.get("confidence"),

            "grade": analysis.get("grade"),

            "entry": "AUTO",

            "stop_loss": "AUTO",

            "take_profit": "AUTO"

        }



        # 3. Execution rules

        decision = self.execution.prepare_order(
            plan
        )



        # 4. Save approved trades

        if decision.get("approved"):


            self.manager.add_trade({

                "user_id": user_id,

                "symbol": symbol,

                "direction": decision["signal"],

                "entry": decision["entry"]

            })


            decision["saved"] = True


        else:

            decision["saved"] = False



        decision["account_status"] = account_status


        return decision
