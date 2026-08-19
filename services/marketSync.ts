import { fetchMarketData } from "./marketFeed";
import { analyzeMarket } from "./saintAPI";
import { updateLiveData, addNotification } from "./liveData";
import { sendLiveNotification } from "./notifications";

let timer: any = null;

let lastSignalKey = "";
let lastAnalysisKey = "";

function getRisk(confidence: number) {
  if (confidence >= 90) return "HIGH";
  if (confidence >= 70) return "MEDIUM";
  return "LOW";
}

function getMarketSession() {
  const hour = new Date().getUTCHours();

  if (hour >= 0 && hour < 8) return "ASIA";
  if (hour >= 8 && hour < 13) return "LONDON";
  if (hour >= 13 && hour < 17) return "LONDON / NEW YORK";
  if (hour >= 17 && hour < 22) return "NEW YORK";

  return "OFF-SESSION";
}

function validNumber(value: any, fallback = 0) {
  const number = Number(value);

  return Number.isFinite(number) ? number : fallback;
}

export function startMarketSync() {
  if (timer) return;

  console.log("Saint Twelve Data → Cloud AI Sync Started");

  const sync = async () => {
    try {
      const market = await fetchMarketData();

      console.log(
        "TWELVE DATA:",
        market?.symbol,
        market?.bid,
        market?.candles?.length
      );

      if (!market || !market.candles?.length) {
        updateLiveData({
          internetStatus: "OFFLINE",
          liveFeedStatus: "OFFLINE",
          aiStatus: "OFFLINE",
        });

        console.log("No market data");
        return;
      }

      updateLiveData({
        internetStatus: "ONLINE",
        liveFeedStatus: "ONLINE",
      });

      const result = await analyzeMarket(market);

      console.log("CLOUD AI RESPONSE:", result);

      console.log(
        "MTF DATA:",
        "M5 =", market.timeframes?.M5?.length ?? 0,
        "M15 =", market.timeframes?.M15?.length ?? 0,
        "H1 =", market.timeframes?.H1?.length ?? 0
      );

      if (!result) {
        updateLiveData({
          aiStatus: "OFFLINE",
        });

        return;
      }

      const signal =
        result.signal === "BUY" || result.signal === "SELL"
          ? result.signal
          : "WAIT";

      const confidence = validNumber(result.confidence, 0);

      const grade = result.grade ?? "D";

      const reason = result.reason ?? "";

      const pattern = result.pattern ?? {};

      const tradePlan = result.trade_plan ?? {};

      const rawEntry =
        result.entry ??
        tradePlan.entry ??
        market.bid ??
        0;

      const rawStopLoss =
        result.stop_loss ??
        result.stopLoss ??
        tradePlan.stop_loss ??
        tradePlan.stopLoss ??
        0;

      const rawTakeProfit =
        result.take_profit ??
        result.takeProfit ??
        tradePlan.take_profit ??
        tradePlan.takeProfit ??
        0;

      const entry = validNumber(rawEntry, market.bid ?? 0);

      const stopLoss = validNumber(rawStopLoss, 0);

      const takeProfit = validNumber(rawTakeProfit, 0);

      // BUY/SELL signals require a complete trade plan.
      // Never display a directional signal when SL or TP is missing.
      const hasCompleteTradePlan =
        entry > 0 &&
        stopLoss > 0 &&
        takeProfit > 0;

      const validatedSignal =
        (signal === "BUY" || signal === "SELL") && hasCompleteTradePlan
          ? signal
          : "WAIT";

      const validatedConfidence =
        validatedSignal === signal ? confidence : 0;

      const risk = getRisk(validatedConfidence);

      const symbol = market.symbol || "XAU/USD";

      const analysisKey =
        `${validatedSignal}:${validatedConfidence}:${grade}:${reason}`;

      updateLiveData({
        internetStatus: "ONLINE",
        liveFeedStatus: "ONLINE",
        aiStatus: "ONLINE",

        aiConfidence: validatedConfidence,
        aiGrade: grade,
        aiReason: reason,
        aiPattern: pattern,

        risk,
        marketSession: getMarketSession(),
        strategy: "INSTITUTIONAL SIGNALS",

        currentSignal: {
          symbol,
          direction: validatedSignal,
          entry,
          stopLoss,
          takeProfit,
        },
      });

      /*
       * Only add an in-app analysis notification when
       * the actual AI result changes.
       */
      if (analysisKey !== lastAnalysisKey) {
        lastAnalysisKey = analysisKey;

        addNotification(
          `AI Analysis • ${symbol} • ${signal} • ${confidence}% confidence`
        );

        if (reason) {
          addNotification(`AI Reason • ${reason}`);
        }
      }

      /*
       * LIVE SIGNAL ALERT
       *
       * Only BUY/SELL signals with confidence >= 70
       * generate a push notification.
       */
      if (
        (signal === "BUY" || signal === "SELL") &&
        confidence >= 70
      ) {
        const signalKey =
          `${validatedSignal}:${symbol}:${validatedConfidence}`;

        if (signalKey !== lastSignalKey) {
          lastSignalKey = signalKey;

          const message =
            `${validatedSignal} ${symbol} (${validatedConfidence}% confidence)`;

          addNotification(message);

          await sendLiveNotification(
            `SaintScalperFX ${signal} Signal`,
            message
          );

          console.log(
            "LIVE NOTIFICATION SENT:",
            message
          );
        }
      } else {
        lastSignalKey = "";
      }

    } catch (error) {
      console.log("Market Sync Error:", error);

      updateLiveData({
        internetStatus: "OFFLINE",
        liveFeedStatus: "OFFLINE",
        aiStatus: "OFFLINE",
      });
    }
  };

  sync();

  timer = setInterval(sync, 10000);
}

export function stopMarketSync() {
  if (timer) {
    clearInterval(timer);
    timer = null;
  }

  console.log("Saint Twelve Data → Cloud AI Sync Stopped");
}
