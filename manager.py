class AIManager:

    def __init__(self):

        self.mode = "HYBRID"

    def set_mode(self, mode):

        self.mode = mode.upper()

    def get_mode(self):

        return self.mode

    def available_modes(self):

        return [
            "VISION",
            "MARKET",
            "HYBRID"
        ]

