//+------------------------------------------------------------------+
//|                  SaintScalperFX AI Client V2                     |
//|            Communication Layer for SaintBridge                   |
//+------------------------------------------------------------------+
#pragma once

class AIClient
{
private:

   string ServerURL;

public:

   AIClient(string url)
   {
      ServerURL = url;
   }

   //====================================================
   // CONNECT
   //====================================================

   bool Connect()
   {
      Print("========================================");
      Print(" SaintScalperFX AI Client");
      Print(" Connected to: ", ServerURL);
      Print("========================================");

      return true;
   }

   //====================================================
   // SEND MARKET DATA
   //====================================================

   bool SendMarketData(
      string symbol,
      string timeframe,
      double bid,
      double ask
   )
   {
      Print("----------- MARKET -----------");
      Print("Symbol      : ", symbol);
      Print("Timeframe   : ", timeframe);
      Print("Bid         : ", DoubleToString(bid,_Digits));
      Print("Ask         : ", DoubleToString(ask,_Digits));
      Print("------------------------------");

      // HTTP POST to /market
      // (Next version)

      return true;
   }

   //====================================================
   // SEND ACCOUNT DATA
   //====================================================

   bool SendAccountData()
   {
      double balance     = AccountInfoDouble(ACCOUNT_BALANCE);
      double equity      = AccountInfoDouble(ACCOUNT_EQUITY);
      double margin      = AccountInfoDouble(ACCOUNT_MARGIN);
      double freeMargin  = AccountInfoDouble(ACCOUNT_MARGIN_FREE);
      double profit      = AccountInfoDouble(ACCOUNT_PROFIT);
      int openTrades     = PositionsTotal();

      Print("----------- ACCOUNT ----------");
      Print("Balance      : ", balance);
      Print("Equity       : ", equity);
      Print("Profit       : ", profit);
      Print("Margin       : ", margin);
      Print("Free Margin  : ", freeMargin);
      Print("Open Trades  : ", openTrades);
      Print("------------------------------");

      // HTTP POST to /account
      // (Next version)

      return true;
   }

   //====================================================
   // RECEIVE AI SIGNAL
   //====================================================

   string GetSignal()
   {
      // Future JSON response

      return "WAIT";
   }

   //====================================================
   // RECEIVE CONFIDENCE
   //====================================================

   double GetConfidence()
   {
      return 0;
   }
};
