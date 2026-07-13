#property copyright "SaintScalperFX"
#property version   "1.00"
#property strict

int OnInit()
{
   Print("SaintScalperFX EA Started");
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
      "Connected to MT5\n",
      "Symbol: ", Symbol(), "\n",
      "Timeframe: ", EnumToString((ENUM_TIMEFRAMES)Period()), "\n",
      "Bid: ", DoubleToString(SymbolInfoDouble(Symbol(), SYMBOL_BID), _Digits), "\n",
      "Ask: ", DoubleToString(SymbolInfoDouble(Symbol(), SYMBOL_ASK), _Digits)
   );
}
