"""
SaintScalperFX
Account Manager
Version 1.0
"""

from flask import jsonify

# ======================================================
# LIVE ACCOUNT STORAGE
# ======================================================

account_data = {
    "balance": 0.0,
    "equity": 0.0,
    "margin": 0.0,
    "free_margin": 0.0,
    "profit": 0.0,
    "open_trades": 0
}


# ======================================================
# UPDATE ACCOUNT
# ======================================================

def update(data):

    global account_data

    account_data["balance"] = float(data.get("balance", 0))
    account_data["equity"] = float(data.get("equity", 0))
    account_data["margin"] = float(data.get("margin", 0))
    account_data["free_margin"] = float(data.get("free_margin", 0))
    account_data["profit"] = float(data.get("profit", 0))
    account_data["open_trades"] = int(data.get("open_trades", 0))

    return True


# ======================================================
# GET ACCOUNT
# ======================================================

def get():

    return account_data


# ======================================================
# JSON RESPONSE
# ======================================================

def json():

    return jsonify(account_data)
