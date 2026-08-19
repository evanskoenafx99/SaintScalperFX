def _number(value):
    try:
        value = float(value)
        return value if value > 0 else 0
    except (TypeError, ValueError):
        return 0


def _first_number(*values):
    for value in values:
        number = _number(value)
        if number > 0:
            return number
    return 0


def _get_number(data, *keys):
    if not isinstance(data, dict):
        return 0

    for key in keys:
        if key in data:
            number = _number(data.get(key))
            if number > 0:
                return number

    return 0


def generate_trade_plan(signal, analysis, price=0):
    """
    SAINT ULTRA trade-plan generator.

    This replaces the old pattern/momentum/support/resistance
    trade-plan system.

    The plan is built from the NEW SAINT ULTRA analysis:
        H1 bias
        M15 structure
        liquidity
        institutional zone
        entry confirmation
        market intelligence
        risk
        final state
    """

    analysis = analysis or {}

    signal = str(signal or "WAIT").upper()
    price = _number(price)

    bias = analysis.get("bias", "NEUTRAL")
    state = analysis.get("state", "WAIT")

    structure = analysis.get("structure_context", {})
    liquidity = analysis.get("liquidity", {})
    zone = analysis.get("zone", {})
    confirmation = analysis.get("entry_confirmation", {})
    intelligence = analysis.get("intelligence", {})
    risk = analysis.get("risk", {})
    mtf = analysis.get("multi_timeframe", {})

    if not isinstance(structure, dict):
        structure = {}

    if not isinstance(liquidity, dict):
        liquidity = {}

    if not isinstance(zone, dict):
        zone = {}

    if not isinstance(confirmation, dict):
        confirmation = {}

    if not isinstance(intelligence, dict):
        intelligence = {}

    if not isinstance(risk, dict):
        risk = {}

    if not isinstance(mtf, dict):
        mtf = {}

    plan = {
        "signal": signal,
        "setup_state": "WAIT",
        "entry": 0,
        "stop_loss": 0,
        "take_profit": 0,
        "setup_quality": 0,
        "basis": {
            "bias": bias,
            "state": state,
            "structure": structure,
            "liquidity": liquidity,
            "zone": zone,
            "entry_confirmation": confirmation,
            "intelligence": intelligence,
            "risk": risk,
            "multi_timeframe": mtf,
        },
    }

    # --------------------------------------------------
    # WAIT
    # --------------------------------------------------

    if signal not in ("BUY", "SELL"):
        plan["setup_state"] = state if state else "WAIT"
        plan["setup_quality"] = 0
        return plan

    # --------------------------------------------------
    # ENTRY
    #
    # Prefer a level supplied by the new SAINT ULTRA
    # confirmation/zone analysis.
    # Current market price is only the fallback.
    # --------------------------------------------------

    entry = _first_number(
        _get_number(
            confirmation,
            "entry",
            "entry_price",
            "trigger",
            "trigger_price",
            "level",
        ),
        _get_number(
            zone,
            "entry",
            "entry_price",
            "mid",
            "midpoint",
            "level",
        ),
        price,
    )

    # --------------------------------------------------
    # STOP LOSS
    #
    # Use institutional zone / confirmation levels.
    # No artificial support/resistance calculation.
    # --------------------------------------------------

    stop_loss = _first_number(
        _get_number(
            confirmation,
            "stop_loss",
            "stopLoss",
            "sl",
            "invalidation",
            "invalidation_level",
        ),
        _get_number(
            zone,
            "stop_loss",
            "stopLoss",
            "sl",
            "invalidation",
            "invalidation_level",
        ),
        _get_number(
            structure,
            "stop_loss",
            "stopLoss",
            "sl",
            "invalidation",
            "invalidation_level",
        ),
    )

    # --------------------------------------------------
    # TAKE PROFIT
    #
    # Prefer institutional target levels supplied by
    # the new analysis.
    # --------------------------------------------------

    take_profit = _first_number(
        _get_number(
            confirmation,
            "take_profit",
            "takeProfit",
            "tp",
            "target",
            "target_price",
        ),
        _get_number(
            zone,
            "take_profit",
            "takeProfit",
            "tp",
            "target",
            "target_price",
        ),
        _get_number(
            intelligence,
            "take_profit",
            "takeProfit",
            "tp",
            "target",
            "target_price",
        ),
    )

    plan["entry"] = entry
    plan["stop_loss"] = stop_loss
    plan["take_profit"] = take_profit

    # --------------------------------------------------
    # SETUP STATE
    # --------------------------------------------------

    if state in (
        "SETUP_READY",
        "CONFIRMED",
        "SIGNAL_CONFIRMED",
    ):
        plan["setup_state"] = "CONFIRMED"
    elif state in (
        "SETUP_DEVELOPING",
        "DEVELOPING",
    ):
        plan["setup_state"] = "DEVELOPING"
    else:
        plan["setup_state"] = "SIGNAL"

    # --------------------------------------------------
    # SETUP QUALITY
    #
    # This is a quality display metric, not a second
    # signal engine.
    # --------------------------------------------------

    quality = 0

    if bias in (signal, "BULLISH" if signal == "BUY" else "BEARISH"):
        quality += 20

    structure_signal = str(
        structure.get("signal", "")
    ).upper()

    if structure_signal == signal:
        quality += 20

    if liquidity.get("event"):
        quality += 15

    confirmation_signal = str(
        confirmation.get("signal", "")
    ).upper()

    if confirmation_signal == signal:
        quality += 20

    intelligence_signal = str(
        intelligence.get("signal", "")
    ).upper()

    if intelligence_signal == signal:
        quality += 15

    if risk.get("approved") is True:
        quality += 10

    plan["setup_quality"] = min(quality, 100)

    return plan
