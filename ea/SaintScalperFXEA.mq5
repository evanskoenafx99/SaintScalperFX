#property copyright "SaintScalperFX"
#property version   "1.10"
#property strict

input string API_URL = "http://127.0.0.1:8000/live_signal";

datetime lastSend = 0;

int OnInit()
{
   Print("SaintScalperFX Live EA Started");
   return(INIT_SUCCEEDED);
}


void OnDeinit(const int reason)
{
   Print("SaintScalperFX EA Stopped");
}


void OnTick()
{
   Comment(
      "SaintScalperFX\n",
      "LIVE MT5 CONNECTION\n",
      "Symbol: ", Symbol(), "\n",
      "Timeframe: ", EnumToString((ENUM_TIMEFRAMES)Period()), "\n",
      "Bid: ", DoubleToString(SymbolInfoDouble(Symbol(), SYMBOL_BID), _Digits), "\n",
      "Ask: ", DoubleToString(SymbolInfoDouble(Symbol(), SYMBOL_ASK), _Digits)
   );


   if(TimeCurrent() - lastSend >= 60)
   {
      SendMarketData();
      lastSend = TimeCurrent();
   }
}


void SendMarketData()
{
   MqlRates rates[];

   ArraySetAsSeries(rates,true);


   int copied = CopyRates(
      Symbol(),
      Period(),
      0,
      50,
      rates
   );


   if(copied <= 0)
   {
      Print("No candle data");
      return;
   }


   string json = "{\"candles\":[";


   for(int i=copied-1;i>=0;i--)
   {
      json += "{";
      json += "\"open\":"+DoubleToString(rates[i].open,_Digits)+",";
      json += "\"high\":"+DoubleToString(rates[i].high,_Digits)+",";
      json += "\"low\":"+DoubleToString(rates[i].low,_Digits)+",";
      json += "\"close\":"+DoubleToString(rates[i].close,_Digits);
      json += "}";

      if(i>0)
         json += ",";
   }


   json += "]}";


   char data[];
   char result[];

   StringToCharArray(
      json,
      data
   );


   string headers =
      "Content-Type: application/json\r\n";


   int response = WebRequest(
      "POST",
      API_URL,
      headers,
      5000,
      data,
      result,
      headers
   );


   if(response == -1)
   {
      Print("API connection failed");
      return;
   }


   string answer = CharArrayToString(result);

   Print("AI RESPONSE: ", answer);
}
