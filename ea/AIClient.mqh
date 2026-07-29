//+------------------------------------------------------------------+
//|                  SaintScalperFX AIClient V5                     |
//|              Command Channel + Confirmation Layer               |
//+------------------------------------------------------------------+
#property strict
#pragma once

class AIClient
{
private:

   string ServerURL;
   string CommandURL;
   string ConfirmationURL;

   string LastDecision;
   string LastSignal;
   string LastCommand;

   long LastTicket;

   double LastLotSize;
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
      ServerURL="http://127.0.0.1:8000/market";
      CommandURL="http://127.0.0.1:8000/command";
      ConfirmationURL="http://127.0.0.1:8000/confirmation";


      LastDecision="WAIT";
      LastSignal="NONE";
      LastCommand="NONE";

      LastTicket=0;
      LastLotSize=0.0;

      LastConfidence=0;
      LastStopLoss=0;
      LastTakeProfit=0;
   }
AIClient(string url)
{
   ServerURL = url;

   string base = url;
   int pos = StringFind(base, "/market");

   if(pos > 0)
      base = StringSubstr(base, 0, pos);

   CommandURL = base + "/command";
   ConfirmationURL = base + "/confirmation";

   LastDecision = "WAIT";
   LastSignal = "NONE";
   LastCommand = "NONE";
   LastTicket = 0;
   LastLotSize = 0.0;
   LastConfidence = 0;
   LastStopLoss = 0;
   LastTakeProfit = 0;
}


   void SetURL(string url)
   {
      ServerURL=url;
   }

   void SetCommandURL(string url)
   {
      CommandURL=url;
   }

   void SetConfirmationURL(string url)
   {
      ConfirmationURL=url;
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

      json+="\"symbol\":\""+EscapeJSON(symbol)+"\",";
      json+="\"timeframe\":\""+IntegerToString(timeframe)+"\",";
      json+="\"bid\":"+DoubleToString(bid,Digits())+",";
      json+="\"ask\":"+DoubleToString(ask,Digits())+",";

      json+="\"candles\":[";

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

      string headers=
      "Content-Type: application/json\r\n";

      StringToCharArray(json,post);

      ResetLastError();

      int response=
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
         Print("AIClient HTTP Error: ",GetLastError());
         return false;
      }

      string answer=CharArrayToString(result);

      ParseResponse(answer);

      return true;
   }

   void ParseResponse(string json)
   {
      LastDecision=ExtractString(json,"decision");
      LastSignal=ExtractString(json,"signal");
      LastCommand=ExtractString(json,"command");

      LastTicket=(long)ExtractDouble(json,"ticket");
      LastLotSize=ExtractDouble(json,"lot_size");

      LastConfidence=ExtractDouble(json,"confidence");
      LastStopLoss=ExtractDouble(json,"stop_loss");
      LastTakeProfit=ExtractDouble(json,"take_profit");
   }

bool FetchCommand()
   {
      char post[];
      char result[];

      string headers=
      "Content-Type: application/json\r\n";

      ResetLastError();

      int response=
      WebRequest(
         "GET",
         CommandURL,
         headers,
         10000,
         post,
         result,
         headers
      );

      if(response==-1)
      {
         Print("Command Request Error: ",GetLastError());
         return false;
      }

      ParseResponse(CharArrayToString(result));

      return true;
   }
   bool SendConfirmation(
      string command,
      long ticket,
      bool success
   )
   {
      string json="{";

      json+="\"command\":\""+EscapeJSON(command)+"\",";
      json+="\"ticket\":"+IntegerToString((int)ticket)+",";
      json+="\"success\":";
      json+=(success ? "true" : "false");
      json+="}";

      char post[];
      char result[];

      string headers="Content-Type: application/json\r\n";

      StringToCharArray(json,post);

      ResetLastError();

      int response=
      WebRequest(
         "POST",
         ConfirmationURL,
         headers,
         10000,
         post,
         result,
         headers
      );

      if(response==-1)
      {
         Print("Confirmation Error: ",GetLastError());
         return false;
      }

      return true;
   }

   string ExtractString(string json,string key)
   {
      string search="\""+key+"\":\"";

      int start=StringFind(json,search);

      if(start<0)
         return "";

      start+=StringLen(search);

      int end=StringFind(json,"\"",start);

      if(end<0)
         return "";

      return StringSubstr(json,start,end-start);
   }

   double ExtractDouble(string json,string key)
   {
      string search="\""+key+"\":";

      int start=StringFind(json,search);

      if(start<0)
         return 0;

      start+=StringLen(search);

      int end=StringFind(json,",",start);

      if(end<0)
         end=StringFind(json,"}",start);

      if(end<0)
         return 0;

      return StringToDouble(
         StringSubstr(json,start,end-start)
      );
   }

   string GetDecision()
   {
      return LastDecision;
   }

   string GetSignal()
   {
      return LastSignal;
   }

   string GetCommand()
   {
      return LastCommand;
   }

   long GetTicket()
   {
      return LastTicket;
   }

   double GetLotSize()
   {
      return LastLotSize;
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
