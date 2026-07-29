from engine.risk import analyze as risk_analyze
from engine.price_risk import calculate as price_calculate


class RiskGuardian:


    def __init__(self):

        self.name = "Saint Risk Guardian V1"



    def check_trade(
        self,
        signal,
        candles,
        bid,
        ask
    ):

        account_risk = risk_analyze()


        if not account_risk["approved"]:

            return {
                "allowed": False,
                "reason": "Risk engine rejected trade"
            }



        prices = price_calculate(
            signal,
            candles,
            bid,
            ask
        )


        if prices["stop_loss"] == 0:

            return {
                "allowed": False,
                "reason": "Invalid stop loss"
            }



        return {

            "allowed": True,

            "reason": "Risk checks passed",

            "risk": account_risk,

            "prices": prices

        }
