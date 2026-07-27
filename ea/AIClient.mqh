//+------------------------------------------------------------------+
//|                  SaintScalperFX AIClient V4                     |
//|              Production HTTP Communication Layer                |
//+------------------------------------------------------------------+
#property strict
#pragma once

class AIClient
{
private:

   string ServerURL;

   string LastDecision;
   string LastSignal;
   double LastConfidence;
   double LastStopLoss;
   double LastTakeProfit;


   string EscapeJSON(string value)
   {
      StringReplace(value,"\\","\\\\");
      StringReplace(value,"\"","\\\"");
      return value;
   }


public:

AIClient()
{
   ServerURL = "http://127.0.0.1:5001/market";

   LastSignal = "NONE";
   LastConfidence = 0;
   LastStopLoss = 0;
   LastTakeProfit = 0;
}


AIClient(string url)
{
   ServerURL = url;

   LastSignal = "NONE";
   LastConfidence = 0;
   LastStopLoss = 0;
   LastTakeProfit = 0;
}


   void SetURL(string url)
   {
      ServerURL = url;
   }


   bool SendMarketData(
      string symbol,
      ENUM_TIMEFRAMES timeframe,
      double bid,
      double ask,
      MqlRates &candles[],
      int candleCount
   )
   {

      string json="{";

      json += "\"symbol\":\""+EscapeJSON(symbol)+"\",";
      json += "\"timeframe\":\""+IntegerToString(timeframe)+"\",";
      json += "\"bid\":"+DoubleToString(bid,Digits())+",";
      json += "\"ask\":"+DoubleToString(ask,Digits())+",";


      json += "\"candles\":[";


      int limit=MathMin(candleCount,200);


      for(int i=0;i<limit;i++)
      {

         if(i>0)
            json+=",";


         json+="{";

         json+="\"time\":"+IntegerToString(candles[i].time)+",";
         json+="\"open\":"+DoubleToString(candles[i].open,Digits())+",";
         json+="\"high\":"+DoubleToString(candles[i].high,Digits())+",";
         json+="\"low\":"+DoubleToString(candles[i].low,Digits())+",";
         json+="\"close\":"+DoubleToString(candles[i].close,Digits())+",";
         json+="\"volume\":"+IntegerToString(candles[i].tick_volume);

         json+="}";

      }


      json+="]}";


      char post[];
      char result[];

      string headers =
      "Content-Type: application/json\r\n";


      StringToCharArray(json,post);
Print("SAINT DEBUG candles sent: ", candleCount);
Print("SAINT DEBUG JSON size: ", StringLen(json));

      ResetLastError();


      int response =
      WebRequest(
         "POST",
         ServerURL,
         headers,
         10000,
         post,
         result,
         headers
      );


      if(response==-1)
      {
         Print("AIClient V4 HTTP Error: ",
               GetLastError());

         return false;
      }


      string answer =
      CharArrayToString(result);


      ParseResponse(answer);


      return true;

   }



   void ParseResponse(string json)
   {

      LastDecision =
      ExtractString(json,"decision");     

      LastSignal =
      ExtractString(json,"signal");


      LastConfidence =
      ExtractDouble(json,"confidence");


      LastStopLoss =
      ExtractDouble(json,"stop_loss");


      LastTakeProfit =
      ExtractDouble(json,"take_profit");

   }



   string ExtractString(string json,string key)
   {

      string search="\""+key+"\":\"";

      int start=
      StringFind(json,search);


      if(start<0)
         return "";


      start += StringLen(search);


      int end=
      StringFind(json,"\"",start);


      if(end<0)
         return "";


      return StringSubstr(
         json,
         start,
         end-start
      );

   }



   double ExtractDouble(string json,string key)
   {

      string search="\""+key+"\":"; 

      int start=
      StringFind(json,search);


      if(start<0)
         return 0;


      start += StringLen(search);


      int end=
      StringFind(json,",",start);


      if(end<0)
         end=
         StringFind(json,"}",start);


      if(end<0)
         return 0;


      string value =
      StringSubstr(
         json,
         start,
         end-start
      );


      return StringToDouble(value);

   }

   string GetDecision()
  {
      return LastDecision;
  }

   string GetSignal()
   {
      return LastSignal;
   }


   double GetConfidence()
   {
      return LastConfidence;
   }


   double GetStopLoss()
   {
      return LastStopLoss;
   }


   double GetTakeProfit()
   {
      return LastTakeProfit;
   }


};
