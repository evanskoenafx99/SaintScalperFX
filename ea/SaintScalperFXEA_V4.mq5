//+------------------------------------------------------------------+
//|                 SaintScalperFX EA V5                             |
//|        AI Powered Expert Advisor - Live Bridge Edition           |
//+------------------------------------------------------------------+

#property copyright "SaintScalperFX"
#property version   "5.00"
#property strict

#include <Trade/Trade.mqh>
#include "AIClient.mqh"

CTrade trade;

//====================================================
// INPUTS
//====================================================

input string AI_URL="http://127.0.0.1:5001";

input double LotSize=0.02;

input int StopLoss=100;

input int TakeProfit=300;

input ulong MagicNumber=111111;

//====================================================
// GLOBALS
//====================================================

AIClient ai(AI_URL);

string AISignal="WAIT";

double AIConfidence=0;

datetime LastUpdate=0;

//====================================================
// INITIALIZATION
//====================================================

int OnInit()
{
   trade.SetExpertMagicNumber(MagicNumber);

   ai.Connect();

   Print("====================================");
   Print(" SaintScalperFX EA Version 5");
   Print(" AI Bridge Started");
   Print("====================================");

   EventSetTimer(5);

   return(INIT_SUCCEEDED);
}

//====================================================

void OnDeinit(const int reason)
{
   EventKillTimer();

   Print("SaintScalperFX EA Stopped");
}
//====================================================
// MAIN LOOP
//====================================================

void OnTick()
{
   double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);

   // Send live market data every 60 seconds
   if(TimeCurrent() - LastUpdate >= 60)
   {
      ai.SendMarketData(
         _Symbol,
         EnumToString(_Period),
         bid,
         ask
      );

      ai.SendAccountData();

      LastUpdate = TimeCurrent();
   }

   ExecuteAISignal();
}

//====================================================
// TIMER
//====================================================

void OnTimer()
{
   AIConfidence = ai.GetConfidence();
   AISignal = ai.GetSignal();

   Print("--------------------------------");
   Print("AI Signal      : ", AISignal);
   Print("AI Confidence  : ", AIConfidence);
   Print("--------------------------------");

   ManageTrades();
   ApplyTrailingStop();
}
//====================================================
// EXECUTE AI SIGNAL
//====================================================

void ExecuteAISignal()
{
   if(PositionsTotal() > 0)
      return;

   double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
   double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);

   if(AISignal == "BUY")
   {
      double sl = ask - StopLoss * _Point;
      double tp = ask + TakeProfit * _Point;

      if(trade.Buy(
         LotSize,
         _Symbol,
         ask,
         NormalizeDouble(sl, _Digits),
         NormalizeDouble(tp, _Digits),
         "SaintScalperFX AI BUY"
      ))
      {
         Print("BUY order placed successfully.");
      }
      else
      {
         Print("BUY order failed. Error: ", GetLastError());
      }
   }
   else if(AISignal == "SELL")
   {
      double sl = bid + StopLoss * _Point;
      double tp = bid - TakeProfit * _Point;

      if(trade.Sell(
         LotSize,
         _Symbol,
         bid,
         NormalizeDouble(sl, _Digits),
         NormalizeDouble(tp, _Digits),
         "SaintScalperFX AI SELL"
      ))
      {
         Print("SELL order placed successfully.");
      }
      else
      {
         Print("SELL order failed. Error: ", GetLastError());
      }
   }
   else
   {
      Print("AI decision: WAIT");
   }
}
//====================================================
// TRADE MANAGEMENT
//====================================================

void ManageTrades()
{
   for(int i = PositionsTotal()-1; i >= 0; i--)
   {
      ulong ticket = PositionGetTicket(i);

      if(!PositionSelectByTicket(ticket))
         continue;

      double profit = PositionGetDouble(POSITION_PROFIT);

      if(profit > 10)
      {
         Print("Position #", ticket,
               " Profit: ", profit);
      }
   }
}

//====================================================
// TRAILING STOP
//====================================================

void ApplyTrailingStop()
{
   for(int i = PositionsTotal()-1; i >= 0; i--)
   {
      ulong ticket = PositionGetTicket(i);

      if(!PositionSelectByTicket(ticket))
         continue;

      // Future AI trailing stop
      // logic will be implemented here.
   }
}

//====================================================
// END OF FILE
//====================================================
