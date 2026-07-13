class ExecutionEngine:

    def can_execute(self, plan):

        confidence = plan.get("confidence", 0)
        grade = plan.get("grade", "D")

        if confidence < 90:
            return False, "Confidence below minimum."

        if grade not in ["A", "A+"]:
            return False, "Trade grade too low."

        return True, "Trade approved."

    def prepare_order(self, plan):

        allowed, reason = self.can_execute(plan)

        if not allowed:
            return {
                "approved": False,
                "reason": reason
            }

        return {
            "approved": True,
            "signal": plan["signal"],
            "entry": plan["entry"],
            "stop_loss": plan["stop_loss"],
            "take_profit": plan["take_profit"],
            "reason": "Trade meets execution rules."
        }
