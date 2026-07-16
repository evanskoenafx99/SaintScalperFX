//+------------------------------------------------------------------+
//|                 SaintScalperFX AI Client                         |
//|          Communication Library (Version 1.0)                     |
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

   bool Connect()
   {
      Print("Connecting to SaintBridge...");
      Print("Server: ", ServerURL);

      return true;
   }

   bool SendMarketData(
      string symbol,
      string timeframe,
      double bid,
      double ask
   )
   {

      Print("--------------------------------");
      Print("Sending Live Market Data");
      Print("Symbol: ", symbol);
      Print("Timeframe: ", timeframe);
      Print("Bid: ", bid);
      Print("Ask: ", ask);
      Print("--------------------------------");

      // HTTP request will be added here.

      return true;

   }

   string GetSignal()
   {

      // Later this will read JSON
      // returned by SaintBridge.

      return "WAIT";

   }

   double GetConfidence()
   {

      return 0;

   }

};
