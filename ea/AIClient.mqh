//+------------------------------------------------------------------+
//|                 SaintScalperFX AI Client V3.0                    |
//|               HTTP Communication Engine                          |
//+------------------------------------------------------------------+
#pragma once

class AIClient
{
private:

   string ServerURL;
   char post[];
   char result[];
   string headers;

public:

   AIClient(string url)
   {
      ServerURL = url;
      headers = "Content-Type: application/json\r\n";
   }

   bool Connect()
   {
      Print("====================================");
      Print(" SaintScalperFX AI Client V3");
      Print(" Server : ",ServerURL);
      Print("====================================");

      return(true);
   }

   bool SendAccountData(
      double balance,
      double equity,
      double margin,
      double freeMargin,
      double profit,
      int openTrades
   )
   {
      string json =
      "{"
      "\"balance\":"+DoubleToString(balance,2)+","
      "\"equity\":"+DoubleToString(equity,2)+","
      "\"margin\":"+DoubleToString(margin,2)+","
      "\"free_margin\":"+DoubleToString(freeMargin,2)+","
      "\"profit\":"+DoubleToString(profit,2)+","
      "\"open_trades\":"+IntegerToString(openTrades)+
      "}";

      StringToCharArray(json,post);
      ResetLastError();

      int timeout = 5000;

      string response_headers = "";

      int res = WebRequest(
         "POST",
         ServerURL + "/account",
         headers,
         timeout,
         post,
         result,
         response_headers
      );

      if(res == -1)
      {
         Print("ACCOUNT SEND FAILED : ", GetLastError());
         return(false);
      }

      Print("Account synced.");

      return(true);
   }

   bool SendMarketData(
      string symbol,
      string timeframe,
      double bid,
      double ask
   )
   {
      string json =
      "{"
      "\"symbol\":\""+symbol+"\","
      "\"timeframe\":\""+timeframe+"\","
      "\"bid\":"+DoubleToString(bid,_Digits)+","
      "\"ask\":"+DoubleToString(ask,_Digits)+
      "}";

      StringToCharArray(json,post);

      ResetLastError();

      int timeout = 5000;

      string response_headers = "";

      int res = WebRequest(
         "POST",
         ServerURL + "/market",
         headers,
         timeout,
         post,
         result,
         response_headers
      );
      if(res == -1)
      {
         Print("MARKET SEND FAILED : ", GetLastError());
         return(false);
      }

      Print("Market synced.");

      return(true);
   }

   string GetSignal()
   {
      return("WAIT");
   }

   double GetConfidence()
   {
      return(0.0);
   }

};
//+------------------------------------------------------------------+
