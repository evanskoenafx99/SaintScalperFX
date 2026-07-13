class TradePlanner:

    def create(
        self,
        signal,
        entry,
        stop_loss,
        take_profit,
        confidence,
        grade
    ):

        if stop_loss == entry:
            rr = 0
        else:
            rr = round(
                abs(take_profit - entry) /
                abs(entry - stop_loss),
                2
            )

        return {
            "signal": signal,
            "entry": entry,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "risk_reward": f"1:{rr}",
            "confidence": confidence,
            "grade": grade
        }
