class HybridAI:

    def combine(self, vision_result, market_result):

        vision_conf = int(vision_result["confidence"].replace("%", ""))
        market_conf = market_result["confidence"]

        if vision_result["signal"] == market_result["signal"]:

            confidence = round((vision_conf + market_conf) / 2)

            return {
                "signal": vision_result["signal"],
                "confidence": confidence,
                "agreement": True,
                "grade": self.grade(confidence),
                "reason": "Vision AI and Market AI agree."
            }

        return {
            "signal": "WAIT",
            "confidence": round((vision_conf + market_conf) / 2),
            "agreement": False,
            "grade": "D",
            "reason": "Vision AI and Market AI disagree."
        }

    def grade(self, confidence):

        if confidence >= 95:
            return "A+"

        if confidence >= 90:
            return "A"

        if confidence >= 80:
            return "B"

        if confidence >= 70:
            return "C"

        return "D"
