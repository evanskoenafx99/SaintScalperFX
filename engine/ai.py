from engine.trend import analyze as trend
from engine.structure import analyze as structure
from engine.liquidity import analyze as liquidity
from engine.fvg import analyze as fvg
from engine.orderblocks import analyze as orderblocks
from engine.ict import analyze as ict
from engine.smc import analyze as smc
from engine.sessions import analyze as sessions
from engine.momentum import analyze as momentum
from engine.risk import analyze as risk
from engine.market_intelligence import analyze as market_intelligence


class SaintScalperBrain:

    """
    SAINT ULTRA Decision Engine

    Architecture:

        HTF CONTEXT
             ↓
        STRUCTURE
             ↓
        LIQUIDITY
             ↓
        FVG / ORDER BLOCK
             ↓
        ENTRY CONFIRMATION
             ↓
        RISK GATE
             ↓
        BUY / SELL

    Important:
        The current feed supplies M15 candles only.

        Therefore this version does NOT pretend that M15 data
        is H4/H1/M5 data.

        Multi-timeframe confirmation will be added when the
        market feed is upgraded.
    """

    def analyze(self, candles, timeframes=None):

        # ==================================================
        # SAINT ULTRA MULTI-TIMEFRAME ENGINE
        #
        # H1  = higher-timeframe directional bias
        # M15 = ICT / SMC setup timeframe
        # M5  = entry confirmation timeframe
        #
        # Legacy callers can still use analyze(candles).
        # ==================================================

        timeframes = timeframes or {}

        h1_candles = timeframes.get("H1", [])
        m15_candles = timeframes.get("M15", candles or [])
        m5_candles = timeframes.get("M5", [])

        if not m15_candles:
            m15_candles = candles or []

        candles = m15_candles

        if not candles:

            return {
                "signal": "WAIT",
                "confidence": 0,
                "bias": "NEUTRAL",
                "state": "WAIT",
                "reason": "No candle data.",
                "buy_score": 0,
                "sell_score": 0,
                "confirmations": 0,
                "buy_confirmations": 0,
                "sell_confirmations": 0,
                "engines": []
            }

        # ==================================================
        # RUN COMPONENT ENGINES
        # ==================================================

        trend_result = trend(candles)
        structure_result = structure(candles)
        liquidity_result = liquidity(candles)
        fvg_result = fvg(candles)
        orderblock_result = orderblocks(candles)
        ict_result = ict(candles)
        smc_result = smc(candles)
        session_result = sessions(candles)
        momentum_result = momentum(candles)
        risk_result = risk(candles)
        intelligence_result = market_intelligence(candles)

        engines = [
            trend_result,
            structure_result,
            liquidity_result,
            fvg_result,
            orderblock_result,
            ict_result,
            smc_result,
            session_result,
            momentum_result,
            risk_result,
            intelligence_result
        ]

        # ==================================================
        # MARKET INTELLIGENCE
        # ==================================================

        intelligence_signal = intelligence_result.get(
            "signal",
            "WAIT"
        )

        institutional = intelligence_result.get(
            "institutional_footprint",
            {}
        )

        manipulation = intelligence_result.get(
            "manipulation",
            "NONE"
        )

        kill_zone = intelligence_result.get(
            "kill_zone",
            False
        )

        # ==================================================
        # STRUCTURE
        #
        # Structure is the primary directional component.
        #
        # Trend is NOT allowed to override structure.
        # ==================================================

        structure_signal = structure_result.get(
            "signal",
            "WAIT"
        )

        structure_type = structure_result.get(
            "structure",
            "Unknown"
        )

        structure_trend = structure_result.get(
            "trend",
            "RANGING"
        )

        bos = structure_result.get(
            "bos",
            False
        )

        choch = structure_result.get(
            "choch",
            False
        )

        # ==================================================
        # DETERMINE MARKET BIAS
        # ==================================================

        bias = "NEUTRAL"

        if structure_signal == "BUY":

            bias = "BULLISH"

        elif structure_signal == "SELL":

            bias = "BEARISH"

        elif intelligence_signal == "BUY":

            bias = "BULLISH"

        elif intelligence_signal == "SELL":

            bias = "BEARISH"

        # ==================================================
        # LIQUIDITY EVENT
        # ==================================================

        liquidity_signal = liquidity_result.get(
            "signal",
            "WAIT"
        )

        liquidity_type = liquidity_result.get(
            "liquidity",
            "NONE"
        )

        liquidity_event = liquidity_signal in [
            "BUY",
            "SELL"
        ]

        # ==================================================
        # ZONE DETECTION
        #
        # FVG OR ORDER BLOCK.
        #
        # They do NOT need to exist simultaneously.
        # ==================================================

        fvg_signal = fvg_result.get(
            "signal",
            "WAIT"
        )

        fvg_exists = fvg_result.get(
            "fvg",
            False
        )

        fvg_type = fvg_result.get(
            "type",
            "None"
        )

        orderblock_signal = orderblock_result.get(
            "signal",
            "WAIT"
        )

        orderblock_exists = orderblock_result.get(
            "order_block",
            False
        )

        orderblock_type = orderblock_result.get(
            "type",
            "None"
        )

        bullish_zone = (
            fvg_exists and fvg_signal == "BUY"
        ) or (
            orderblock_exists and orderblock_signal == "BUY"
        )

        bearish_zone = (
            fvg_exists and fvg_signal == "SELL"
        ) or (
            orderblock_exists and orderblock_signal == "SELL"
        )

        zone_exists = bullish_zone or bearish_zone

        # ==================================================
        # ICT / SMC ARE COMPOSITE CONTEXT
        #
        # They do not independently vote.
        # ==================================================

        ict_signal = ict_result.get(
            "signal",
            "WAIT"
        )

        smc_signal = smc_result.get(
            "signal",
            "WAIT"
        )

        # ==================================================
        # DETERMINE ZONE DIRECTION
        # ==================================================

        zone_direction = "NONE"

        if bullish_zone and not bearish_zone:

            zone_direction = "BUY"

        elif bearish_zone and not bullish_zone:

            zone_direction = "SELL"

        elif bullish_zone and bearish_zone:

            zone_direction = "CONFLICT"

        # ==================================================
        # LIQUIDITY + STRUCTURE RELATIONSHIP
        # ==================================================

        liquidity_alignment = False

        if bias == "BULLISH":

            if liquidity_type == "SELL_SIDE_SWEEP":
                liquidity_alignment = True

        elif bias == "BEARISH":

            if liquidity_type == "BUY_SIDE_SWEEP":
                liquidity_alignment = True

        # ==================================================
        # SETUP STATE
        # ==================================================

        state = "WAIT"

        reasons = []

        # --------------------------------------------------
        # CONFLICTING STRUCTURE
        # --------------------------------------------------

        if structure_signal == "BUY" and intelligence_signal == "SELL":

            state = "SETUP_DEVELOPING"

            reasons.append(
                "Bullish structure conflicts with bearish market intelligence."
            )

        elif structure_signal == "SELL" and intelligence_signal == "BUY":

            state = "SETUP_DEVELOPING"

            reasons.append(
                "Bearish structure conflicts with bullish market intelligence."
            )

        # --------------------------------------------------
        # NO STRUCTURE
        # --------------------------------------------------

        elif structure_signal == "WAIT":

            state = "WAIT"

            reasons.append(
                "No confirmed market structure direction."
            )

        # --------------------------------------------------
        # STRUCTURE EXISTS
        # --------------------------------------------------

        else:

            # ==============================================
            # LIQUIDITY NOT YET TAKEN
            # ==============================================

            if not liquidity_event:

                state = "SETUP_DEVELOPING"

                reasons.append(
                    "Directional structure exists, but no liquidity event is confirmed."
                )

            # ==============================================
            # LIQUIDITY EXISTS BUT WRONG DIRECTION
            # ==============================================

            elif not liquidity_alignment:

                state = "SETUP_DEVELOPING"

                reasons.append(
                    "Liquidity event does not align with the market bias."
                )

            # ==============================================
            # LIQUIDITY ALIGNED
            # ==============================================

            else:

                reasons.append(
                    "Liquidity event aligns with market bias."
                )

                # ==========================================
                # NO FVG / OB
                # ==========================================

                if not zone_exists:

                    state = "SETUP_DEVELOPING"

                    reasons.append(
                        "Liquidity was taken, but no FVG or Order Block zone is present."
                    )

                # ==========================================
                # CONFLICTING ZONES
                # ==========================================

                elif zone_direction == "CONFLICT":

                    state = "SETUP_DEVELOPING"

                    reasons.append(
                        "Bullish and bearish zones conflict."
                    )

                # ==========================================
                # ZONE EXISTS BUT WRONG DIRECTION
                # ==========================================

                elif zone_direction != structure_signal:

                    state = "SETUP_DEVELOPING"

                    reasons.append(
                        "FVG/Order Block direction does not match structure."
                    )

                # ==========================================
                # VALID SETUP ZONE
                # ==========================================

                else:

                    state = "SETUP_READY"

                    reasons.append(
                        "Structure, liquidity and setup zone are aligned."
                    )

        # ==================================================
        # MULTI-TIMEFRAME CONFIRMATION
        #
        # H1 = directional context
        # M15 = setup
        # M5 = entry trigger
        # ==================================================

        h1_result = None
        h1_signal = "WAIT"
        h1_bias = "NEUTRAL"

        if h1_candles:
            h1_result = structure(h1_candles)

            h1_signal = h1_result.get(
                "signal",
                "WAIT"
            )

            if h1_signal == "BUY":
                h1_bias = "BULLISH"

            elif h1_signal == "SELL":
                h1_bias = "BEARISH"

        # If M15 has no confirmed direction, H1 provides
        # higher-timeframe directional context.
        if structure_signal == "WAIT":

            if h1_signal == "BUY":
                bias = "BULLISH"

            elif h1_signal == "SELL":
                bias = "BEARISH"

        # --------------------------------------------------
        # H1 / M15 ALIGNMENT
        # --------------------------------------------------

        h1_alignment = False
        h1_conflict = False

        if h1_signal in ["BUY", "SELL"]:

            # H1 and M15 agree.
            if h1_signal == structure_signal:
                h1_alignment = True

            # M15 has no confirmed direction yet.
            # H1 is context, NOT a conflict.
            elif structure_signal == "WAIT":
                h1_alignment = False
                h1_conflict = False

            # Only opposite confirmed directions are a conflict.
            elif h1_signal != structure_signal:
                h1_alignment = False
                h1_conflict = True

        # --------------------------------------------------
        # M5 ENTRY CONFIRMATION
        #
        # We intentionally use structure as the primary
        # trigger. A tiny M5 candle pattern is not enough
        # to override the higher timeframe.
        # --------------------------------------------------

        m5_confirmation = False
        m5_signal = "WAIT"

        if m5_candles and structure_signal in ["BUY", "SELL"]:

            m5_result = structure(m5_candles)

            m5_signal = m5_result.get(
                "signal",
                "WAIT"
            )

            if m5_signal == structure_signal:
                m5_confirmation = True

        # --------------------------------------------------
        # APPLY H1 CONTEXT
        # --------------------------------------------------

        if h1_conflict:

            state = "SETUP_DEVELOPING"

            reasons.append(
                "H1 bias conflicts with M15 structure."
            )

        elif h1_alignment:

            reasons.append(
                "H1 bias confirms M15 structure."
            )

        elif h1_candles:

            reasons.append(
                "H1 directional bias is not yet confirmed."
            )

        # --------------------------------------------------
        # ENTRY STATE
        # --------------------------------------------------

        if state == "SETUP_READY":

            if m5_confirmation:

                reasons.append(
                    "M5 entry confirmation aligned with M15 structure."
                )

            elif m5_candles:

                reasons.append(
                    "M5 entry confirmation does not match M15 structure."
                )

            else:

                reasons.append(
                    "M5 entry confirmation unavailable."
                )

        # ==================================================
        # REQUIRED MULTI-TIMEFRAME GATE
        #
        # H1  = mandatory macro direction
        # M15 = mandatory setup
        # M5  = mandatory entry confirmation
        #
        # M15 alone is NEVER allowed to produce BUY/SELL.
        # ==================================================

        required_mtf_ready = (
            bool(h1_candles)
            and bool(m15_candles)
            and bool(m5_candles)
            and h1_signal in ["BUY", "SELL"]
            and h1_alignment
            and m5_confirmation
        )

        if not h1_candles:
            reasons.append(
                "WAIT: H1 data required for macro direction."
            )

        elif h1_signal not in ["BUY", "SELL"]:
            reasons.append(
                "WAIT: H1 directional bias is not confirmed."
            )

        elif h1_conflict:
            reasons.append(
                "WAIT: H1 conflicts with M15 structure."
            )

        if not m5_candles:
            reasons.append(
                "WAIT: M5 data required for entry confirmation."
            )

        elif not m5_confirmation:
            reasons.append(
                "WAIT: M5 entry confirmation does not match M15 structure."
            )

        # ==================================================
        # RISK GATE
        #
        # Risk NEVER contributes directional points.
        # ==================================================

        risk_approved = risk_result.get(
            "approved",
            False
        )

        if not risk_approved:

            state = "WAIT"

            reasons.append(
                "Risk gate rejected the setup."
            )

        # ==================================================
        # FINAL SIGNAL
        #
        # RESPONSIVE SIGNAL ENGINE
        #
        # A strong M15 setup does not require M5 confirmation
        # or a fresh liquidity sweep before becoming actionable.
        #
        # H1 conflict and the risk gate remain hard protections.
        #
        # M5, liquidity and setup zones strengthen confidence
        # rather than forcing an otherwise strong setup to wait.
        # ==================================================

        signal = "WAIT"

        directional_evidence = 0

        # Primary structure
        if structure_signal in ["BUY", "SELL"]:
            directional_evidence += 1

        # Independent confirmations
        if ict_signal == structure_signal:
            directional_evidence += 1

        if smc_signal == structure_signal:
            directional_evidence += 1

        if intelligence_signal == structure_signal:
            directional_evidence += 1

        if zone_direction == structure_signal:
            directional_evidence += 1

        if liquidity_alignment:
            directional_evidence += 1

        # Strong current structure can become actionable
        # without waiting for M5.
        fast_signal_ready = (
            structure_signal in ["BUY", "SELL"]
            and directional_evidence >= 3
            and required_mtf_ready
            and risk_approved
            and not h1_conflict
        )

        # Fully confirmed setup remains valid.
        full_setup_ready = (
            state == "SETUP_READY"
            and required_mtf_ready
            and risk_approved
            and not h1_conflict
        )

        if fast_signal_ready or full_setup_ready:

            if structure_signal == "BUY":
                signal = "BUY"

            elif structure_signal == "SELL":
                signal = "SELL"

        # ==================================================
        # CONFIDENCE
        #
        # This is now based on completed conditions rather
        # than blindly summing engine scores.
        # ==================================================

        confidence = 0

        if structure_signal in ["BUY", "SELL"]:

            confidence += 25

        if liquidity_alignment:

            confidence += 20

        if zone_direction == structure_signal:

            confidence += 20

        if ict_signal == structure_signal:

            confidence += 10

        if smc_signal == structure_signal:

            confidence += 10

        if intelligence_signal == structure_signal:

            confidence += 5

        if institutional.get("bullish") and structure_signal == "BUY":

            confidence += 5

        if institutional.get("bearish") and structure_signal == "SELL":

            confidence += 5

        if m5_confirmation:

            confidence += 15

        if h1_alignment:

            confidence += 10

        if h1_conflict:

            confidence = 0

        if not risk_approved:

            confidence = 0

        # No directional structure = no directional confidence.
        if structure_signal not in ["BUY", "SELL"]:

            confidence = 0

        confidence = min(
            confidence,
            100
        )

        # ==================================================
        # SIGNAL SAFETY
        # ==================================================

        if signal == "WAIT":

            if state == "SETUP_DEVELOPING":

                display_signal = "SETUP DEVELOPING"

            elif state == "SETUP_READY":

                display_signal = "WAIT"

            else:

                display_signal = "WAIT"

        else:

            display_signal = signal

        # ==================================================
        # LEGACY SCORE FIELDS
        #
        # Kept for API compatibility.
        #
        # These are NOT used to make the decision.
        # ==================================================

        buy_score = 0
        sell_score = 0

        if structure_signal == "BUY":
            buy_score = confidence

        elif structure_signal == "SELL":
            sell_score = confidence

        # ==================================================
        # CONFIRMATIONS
        # ==================================================

        buy_confirmations = 0
        sell_confirmations = 0

        if structure_signal == "BUY":
            buy_confirmations += 1

        if structure_signal == "SELL":
            sell_confirmations += 1

        if liquidity_alignment:

            if structure_signal == "BUY":
                buy_confirmations += 1

            elif structure_signal == "SELL":
                sell_confirmations += 1

        if zone_direction == structure_signal:

            if structure_signal == "BUY":
                buy_confirmations += 1

            elif structure_signal == "SELL":
                sell_confirmations += 1

        confirmations = max(
            buy_confirmations,
            sell_confirmations
        )

        # ==================================================
        # RETURN
        # ==================================================

        return {

            "signal": display_signal,

            "confidence": confidence,

            "bias": bias,

            "state": state,

            "reason": " ".join(reasons),

            "buy_score": buy_score,

            "sell_score": sell_score,

            "confirmations": confirmations,

            "buy_confirmations": buy_confirmations,

            "sell_confirmations": sell_confirmations,

            "institutional_footprint": {
                "bullish": institutional.get(
                    "bullish",
                    False
                ),
                "bearish": institutional.get(
                    "bearish",
                    False
                )
            },

            "manipulation": manipulation,

            "kill_zone": kill_zone,

            "liquidity_event": liquidity_event,

            "liquidity_type": liquidity_type,

            "zone": {
                "exists": zone_exists,
                "direction": zone_direction,
                "fvg": fvg_exists,
                "fvg_type": fvg_type,
                "order_block": orderblock_exists,
                "order_block_type": orderblock_type
            },

            "structure_context": {
                "signal": structure_signal,
                "structure": structure_type,
                "trend": structure_trend,
                "bos": bos,
                "choch": choch
            },

            "entry_confirmation": {
                "required": True,
                "m5_available": bool(m5_candles),
                "confirmed": m5_confirmation,
                "signal": m5_signal
            },

            "multi_timeframe": {
                "h1_available": bool(h1_candles),
                "h1_signal": h1_signal,
                "h1_bias": h1_bias,
                "h1_alignment": h1_alignment,
                "h1_conflict": h1_conflict,
                "m15_signal": structure_signal,
                "m5_available": bool(m5_candles),
                "m5_signal": m5_signal,
                "m5_confirmation": m5_confirmation
            },

            "risk": {
                "approved": risk_approved,
                "risk_percent": risk_result.get(
                    "risk_percent"
                ),
                "max_daily_loss": risk_result.get(
                    "max_daily_loss"
                ),
                "risk_reward": risk_result.get(
                    "risk_reward"
                )
            },

            "intelligence": intelligence_result,

            "engines": engines
        }
