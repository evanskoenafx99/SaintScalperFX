//+------------------------------------------------------------------+
//|                                                 Apex Grid EA.mq5 |
//|                          Copyright 2025, ApexMachineEngineer.Ltd |
//|                              https://www.ApexMachineEngineer.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2025, ApexMachineEngineerLtd  ."
#property link      "https://www.ApexMachineEngineer.com"
#property version   "1.00"
#include <Trade/Trade.mqh>

//--------------------------------------------------------------------
CTrade obj_Trade;

input double intialLotsize = 0.02;
double takeProfitPts = 400*_Point;
double stopLossPts = 100*_Point;
double TakeProfit;

double gridSize;
input double gridSize_Spacing = 1;
double LotSize;
input double totalProfit_inCurrency = 1000;
input double MagicNumber = 111;


bool isTradeAllowed = true;
int totalBars = 0;
int handle;
double maData[];
//+------------------------------------------------------------------+
int OnInit(){


   CREATETEXT();


   handle = iMA(_Symbol,_Period,66,0,MODE_SMA,PRICE_CLOSE);
   Print(handle);
   ArraySetAsSeries(maData,true);
   
   static bool isInit = false;
   if(isInit){
      isInit = true;
  
      
      //cheak if licesing has expired

      if(TimeCurrent() > StringToTime("2090.12.31 12:00")){
         Print(__FUNCTION__," > License Is still Active...");
      }else{
         Print(__FUNCTION__," > License Is Not Active AnyMore...");
         ExpertRemove();
         return INIT_FAILED;

      }
      if(AccountInfoInteger(ACCOUNT_TRADE_MODE) == ACCOUNT_TRADE_MODE_DEMO){
         Print(__FUNCTION__," > Demo Account Is Allowed...");
      if(AccountInfoInteger(ACCOUNT_TRADE_MODE) == ACCOUNT_TRADE_MODE_REAL){
         Print(__FUNCTION__," > Real Account Is Allowed...");   
         }
      }
   }

   return(INIT_SUCCEEDED);
}

void OnDeinit(const int reason){   
   
   
}
void OnTick(){
      for(int i = PositionsTotal()-1; i >= 0; i--){    
     ulong posTicket = PositionGetTicket(i);
     if(PositionSelectByTicket(posTicket)){
        double posSl = PositionGetDouble(POSITION_SL);
        double posTp = PositionGetDouble(POSITION_TP);
        
        if(PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY){
           int shift = iLowest(_Symbol,PERIOD_CURRENT,MODE_LOW,10,1);
           double low = iLow(_Symbol,PERIOD_CURRENT,shift);
           low = NormalizeDouble(low,_Digits);
     
           if(low > posSl){
              CTrade trade;
              if(trade.PositionModify(posTicket,low,posTp)){
                 Print(__FUNCTION__," > Pos #",posTicket," was modified...");        
              }
           }
        }else if(PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_SELL){
           int shift = iHighest(_Symbol,PERIOD_CURRENT,MODE_HIGH,10,1);
           double high = iHigh(_Symbol,PERIOD_CURRENT,shift);
           high = NormalizeDouble(high,_Digits);
     
           if(high < posSl || posSl == 0){
              CTrade trade;
              if(trade.PositionModify(posTicket,high,posTp)){
                 Print(__FUNCTION__," > Pos #",posTicket," was modified...");        
   
              }  
           }
        } 
      }
   }
   
   if (PositionsTotal()>1){
      double totalProfit = 0;
      for (int i = PositionsTotal()-1; i>= 0; i--){
         ulong tkt = PositionGetTicket(i);
         if (PositionSelectByTicket(tkt)){
            double profit = PositionGetDouble(POSITION_PROFIT);
            //totalProfit = totalProfit+profit;
            totalProfit += profit;
         }
      }
      if (totalProfit >= totalProfit_inCurrency){
         Print("==== Profit Is Enough Now,Close All the Positions!, ",totalProfit);
         for (int i = PositionsTotal()-1; i>= 0; i--){
            ulong posTkt = PositionGetTicket(i);
            if (PositionSelectByTicket(posTkt)){
               obj_Trade.PositionClose(posTkt);
            }
         }
      }
   } 
   if (isNewBar()) isTradeAllowed = true;
   CopyBuffer(handle,0,1,2,maData);

   double low1 = iLow(_Symbol,_Period,1);
   double low2 =  iLow(_Symbol,_Period,2);
   double High1 =  iHigh(_Symbol,_Period,1);
   double High2 =  iHigh(_Symbol,_Period,2);
   
   double ask = NormalizeDouble(SymbolInfoDouble(_Symbol,SYMBOL_ASK),_Digits);
   double bid = NormalizeDouble(SymbolInfoDouble(_Symbol,SYMBOL_BID),_Digits);

   
   if (PositionsTotal()==0 && low1 > maData[1] && low2 < maData[1] && isTradeAllowed){
   //buy
   Print("BUY");
   gridSize = ask + gridSize_Spacing;
   Print("Next Grid Size = ",gridSize,"Aggressive Apex Scalper v3.0");
   TakeProfit = ask + takeProfitPts;
   obj_Trade.Buy(intialLotsize,_Symbol,ask,0,TakeProfit,"Aggressive Apex Scalper v3.0");
   isTradeAllowed = false;
   }
   else if (PositionsTotal()==0 && High1 > maData[1] && High2 < maData[1] && isTradeAllowed){
   //sell
   Print("SELL");
   gridSize = bid - gridSize_Spacing;
   Print("Next Grid Size = ",gridSize,"Aggressive Apex Scalper v3.0");
   TakeProfit = bid - takeProfitPts;
   obj_Trade.Sell(intialLotsize,_Symbol,bid,0,TakeProfit,"Aggressive Apex Scalper v3.0");
   isTradeAllowed = false;
   }

   if (PositionsTotal() > 0){
      for (int i = PositionsTotal()-1; i>= 0; i--){
         ulong ticket = PositionGetTicket(i);
         if (PositionSelectByTicket(ticket)){
            if (PositionGetInteger(POSITION_TYPE)==POSITION_TYPE_BUY){
               if (ask <= gridSize){
                  obj_Trade.Buy(intialLotsize,_Symbol,ask,0,TakeProfit,"Aggressive Apex Scalper v3.0");
                     gridSize = ask + gridSize_Spacing;
                        Print("Next Grid Size = ",gridSize,"Aggressive Apex Scalper v3.0");
                        
           
               }
            }
            else if (PositionGetInteger(POSITION_TYPE)==POSITION_TYPE_SELL){
               if (bid >= gridSize){
                   obj_Trade.Sell(intialLotsize,_Symbol,bid,0,TakeProfit,"Aggressive Apex Scalper v3.0");     
                      gridSize = bid - gridSize_Spacing;
                         Print("Next Grid Size = ",gridSize,"Aggressive Apex Scalper v3.0");
                         

               }
            }
         }
      }
   }
}

bool isNewBar(){
   int bars = iBars(_Symbol,_Period);
   if (bars > totalBars){
       totalBars = bars;
       return true;
   }
   return false;
}



void CREATETEXT(){
    
    string text = "AGGRESSIVE APEX SCALPER V3.0";

    MqlDateTime str_datetime;
     
    datetime currentTime = TimeCurrent(str_datetime);
    //comment(currentTime,", Sec = ",str_datetime.sec);

    int time_sec = str_datetime.sec;
    color clrT = clrWhite;
    
    if (time_sec >= 0 && time_sec < 10) clrT = clrRed;
    else if (time_sec >= 10 && time_sec < 20) clrT = clrRed;
    else if (time_sec >= 20 && time_sec < 30) clrT = clrBlue;
    else if (time_sec >= 30 && time_sec < 40) clrT = clrGreen;
    else if (time_sec >= 40 && time_sec < 50) clrT = clrOrange;
    else if (time_sec >= 50 && time_sec < 59) clrT = clrPurple;


    if (ObjectFind(0,"NAME") < 0){
        ObjectCreate(0,"NAME",OBJ_LABEL,0,0,0);
    }
    else{
       ObjectSetInteger(0,"NAME",OBJPROP_CORNER,CORNER_LEFT_UPPER);
       ObjectSetInteger(0,"NAME",OBJPROP_XDISTANCE,50);
       ObjectSetInteger(0,"NAME",OBJPROP_YDISTANCE,50);
       ObjectSetString(0,"NAME",OBJPROP_TEXT,text);
       ObjectSetInteger(0,"NAME",OBJPROP_FONTSIZE,50);
       ObjectSetInteger(0,"NAME",OBJPROP_COLOR,clrT);
       ObjectSetInteger(0,"NAME",OBJPROP_BACK,true);

  }
  ChartRedraw(0);
}


bool isNewsEventAhead(){
  MqlCalendarValue values[];
  
  datetime startTime = iTime(_Symbol,PERIOD_D1,0);
  datetime endTime = startTime + PeriodSeconds(PERIOD_D1);
   
  CalendarValueHistory(values,startTime,endTime,NULL,NULL);

  for(int i = 0; i < ArraySize(values); i++){
  MqlCalendarEvent event;
  CalendarEventById(values[i].event_id,event);

  MqlCalendarCountry country;
  CalendarCountryById(event.country_id,country);
   
  if(StringFind(_Symbol,country.currency) < 0) continue;
  if(event.importance == CALENDAR_IMPORTANCE_NONE) continue;
  if(event.importance == CALENDAR_IMPORTANCE_LOW) continue;
  
  
  if(TimeCurrent() >= values[i].time-15*PeriodSeconds(PERIOD_M1) &&
     TimeCurrent() < values[i].time+15*PeriodSeconds(PERIOD_M1)){
     
     
     Print(event.name," is ahead or was just published!!stop trading...");   
     return true;
     
      }
            
   }
   
   return false;

}

//------------------------------------------------------------------------
//owned by Thema Billy Kgole
//born:2004-12-16
//in Alexandra Masakhanine Clinic