import importlib


class MT5Bridge:

    def __init__(self):

        self.connected = False
        self.account = None
        self.broker = None
        self.bridge = None


    def connect(self, broker_name, credentials=None):

        self.broker = broker_name.lower()

        try:

            module = importlib.import_module(
                f"bridge.{self.broker}"
            )

            self.bridge = module.Broker()

            self.connected = self.bridge.connect(
                credentials
            )

            if self.connected:

                self.account = self.bridge.get_account()

            return self.connected

        except Exception as e:

            print("Bridge Error:", e)

            self.connected = False

            return False


    def disconnect(self):

        if self.bridge:

            self.bridge.disconnect()

        self.connected = False


    def is_connected(self):

        return self.connected


    def get_account(self):

        if self.bridge:

            return self.bridge.get_account()

        return None


    def get_candles(
        self,
        symbol="XAUUSD",
        timeframe="M15",
        bars=200
    ):

        if not self.bridge:

            return []

        return self.bridge.get_candles(
            symbol,
            timeframe,
            bars
        )


    def get_positions(self):

        if not self.bridge:

            return []

        return self.bridge.get_positions()


    def place_order(
        self,
        symbol,
        signal,
        lot,
        sl,
        tp
    ):

        if not self.bridge:

            return False

        return self.bridge.place_order(
            symbol,
            signal,
            lot,
            sl,
            tp
        )


    def modify_trade(
        self,
        ticket,
        stop_loss=None,
        take_profit=None
    ):

        if not self.bridge:

            return False

        return self.bridge.modify_trade(
            ticket,
            stop_loss,
            take_profit
        )


    def close_trade(
        self,
        ticket
    ):

        if not self.bridge:

            return False

        return self.bridge.close_trade(
            ticket
        )


    def execute_with_confirmation(
        self,
        action,
        ticket=None,
        stop_loss=None,
        take_profit=None
    ):

        if action == "HOLD":

            return {
                "success": True,
                "action": action,
                "reason": "No action required"
            }


        if action == "MONITOR":

            return {
                "success": True,
                "action": action,
                "reason": "Monitoring position"
            }


        if action == "PROTECT":

            result = self.modify_trade(
                ticket,
                stop_loss,
                take_profit
            )

        elif action == "CLOSED":

            result = self.close_trade(
                ticket
            )

        else:

            return {
                "success": False,
                "action": action,
                "reason": "Unsupported action"
            }


        if result:

            return {
                "success": True,
                "action": action,
                "reason": "Broker confirmed action"
            }


        return {
            "success": False,
            "action": action,
            "reason": "Broker rejected action"
        }
