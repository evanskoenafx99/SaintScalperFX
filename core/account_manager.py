import sqlite3


DATABASE = "users.db"


class SaintAccountManager:


    def __init__(self):

        self.database = DATABASE



    def get_subscription(self, user_id):

        conn = sqlite3.connect(self.database)

        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()


        cursor.execute("""
        SELECT *
        FROM subscriptions
        WHERE user_id=?
        ORDER BY id DESC
        LIMIT 1
        """,
        (user_id,))


        result = cursor.fetchone()

        conn.close()


        if result:

            return dict(result)


        return {

            "plan":"FREE",

            "status":"INACTIVE"

        }



    def get_account(self, user_id):

        conn = sqlite3.connect(self.database)

        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()


        cursor.execute("""
        SELECT *
        FROM trading_accounts
        WHERE user_id=?
        ORDER BY id DESC
        LIMIT 1
        """,
        (user_id,))


        result = cursor.fetchone()

        conn.close()


        if result:

            return dict(result)


        return {

            "status":"DISCONNECTED"

        }



    def get_settings(self, user_id):

        conn = sqlite3.connect(self.database)

        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()


        cursor.execute("""
        SELECT *
        FROM trading_settings
        WHERE user_id=?
        ORDER BY id DESC
        LIMIT 1
        """,
        (user_id,))


        result = cursor.fetchone()

        conn.close()


        if result:

            return dict(result)


        return {

            "mode":"NORMAL",

            "risk":"1%",

            "auto_trade":"OFF"

        }



    def can_trade(self, user_id):


        subscription = self.get_subscription(user_id)

        account = self.get_account(user_id)

        settings = self.get_settings(user_id)



        checks = {


            "subscription": subscription.get("status") == "ACTIVE",


            "account": account.get("status") == "CONNECTED",


            "auto_trade": settings.get("auto_trade") == "ON"


        }



        allowed = all(checks.values())


        return {


            "allowed": allowed,


            "checks": checks,


            "subscription": subscription,


            "account": account,


            "settings": settings


        }
