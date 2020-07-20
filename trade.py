#!/bin/python3

import sys
import numpy as np
import yfinance as yf
import pandas_datareader as pdr
import pandas as pd

ticker = sys.argv[1]

data = yf.download(ticker, period="7d", interval="5m")

data=data.reset_index(drop=True)

data['tr0'] = abs(data["High"] - data["Low"])
data['tr1'] = abs(data["High"] - data["Close"].shift(1))
data['tr2'] = abs(data["Low"]- data["Close"].shift(1))
data["TR"] = round(data[['tr0', 'tr1', 'tr2']].max(axis=1),2)
data["ATR"]=0.00
data["ST"]=0.00

# Calculating ATR
for i, row in data.iterrows():
    if i == 0:
        data.loc[i,'ATR'] = 0.00#data['ATR'].iat[0]
    else:
        data.loc[i,'ATR'] = ((data.loc[i-1,'ATR'] * 13)+data.loc[i,'TR'])/14

data['BUB'] = round(((data["High"] + data["Low"]) / 2) + (2 * data["ATR"]),2)
data['BLB'] = round(((data["High"] + data["Low"]) / 2) - (2 * data["ATR"]),2)


# FINAL UPPERBAND = IF( (Current BASICUPPERBAND < Previous FINAL UPPERBAND) or (Previous Close > Previous FINAL UPPERBAND))
#                     THEN (Current BASIC UPPERBAND) ELSE Previous FINALUPPERBAND)


for i, row in data.iterrows():
    if i==0:
        data.loc[i,"FUB"]=0.00
    else:
        if (data.loc[i,"BUB"]<data.loc[i-1,"FUB"])|(data.loc[i-1,"Close"]>data.loc[i-1,"FUB"]):
            data.loc[i,"FUB"]=data.loc[i,"BUB"]
        else:
            data.loc[i,"FUB"]=data.loc[i-1,"FUB"]

# FINAL LOWERBAND = IF( (Current BASIC LOWERBAND > Previous FINAL LOWERBAND) or (Previous Close < Previous FINAL LOWERBAND))
#                     THEN (Current BASIC LOWERBAND) ELSE Previous FINAL LOWERBAND)

for i, row in data.iterrows():
    if i==0:
        data.loc[i,"FLB"]=0.00
    else:
        if (data.loc[i,"BLB"]>data.loc[i-1,"FLB"])|(data.loc[i-1,"Close"]<data.loc[i-1,"FLB"]):
            data.loc[i,"FLB"]=data.loc[i,"BLB"]
        else:
            data.loc[i,"FLB"]=data.loc[i-1,"FLB"]



# SUPERTREND = IF((Previous SUPERTREND = Previous FINAL UPPERBAND) and (Current Close <= Current FINAL UPPERBAND)) THEN
#                 Current FINAL UPPERBAND
#             ELSE
#                 IF((Previous SUPERTREND = Previous FINAL UPPERBAND) and (Current Close > Current FINAL UPPERBAND)) THEN
#                     Current FINAL LOWERBAND
#                 ELSE
#                     IF((Previous SUPERTREND = Previous FINAL LOWERBAND) and (Current Close >= Current FINAL LOWERBAND)) THEN
#                         Current FINAL LOWERBAND
#                     ELSE
#                         IF((Previous SUPERTREND = Previous FINAL LOWERBAND) and (Current Close < Current FINAL LOWERBAND)) THEN
#                             Current FINAL UPPERBAND


for i, row in data.iterrows():
    if i==0:
        data.loc[i,"ST"]=0.00
    elif (data.loc[i-1,"ST"]==data.loc[i-1,"FUB"]) & (data.loc[i,"Close"]<=data.loc[i,"FUB"]):
        data.loc[i,"ST"]=data.loc[i,"FUB"]
    elif (data.loc[i-1,"ST"]==data.loc[i-1,"FUB"])&(data.loc[i,"Close"]>data.loc[i,"FUB"]):
        data.loc[i,"ST"]=data.loc[i,"FLB"]
    elif (data.loc[i-1,"ST"]==data.loc[i-1,"FLB"])&(data.loc[i,"Close"]>=data.loc[i,"FLB"]):
        data.loc[i,"ST"]=data.loc[i,"FLB"]
    elif (data.loc[i-1,"ST"]==data.loc[i-1,"FLB"])&(data.loc[i,"Close"]<data.loc[i,"FLB"]):
        data.loc[i,"ST"]=data.loc[i,"FUB"]

# Buy Sell Indicator
for i, row in data.iterrows():
    if i==0:
        data["ST_BUY_SELL"]="NA"
    elif (data.loc[i,"ST"]<data.loc[i,"Close"]) :
        data.loc[i,"ST_BUY_SELL"]="BUY"
    else:
        data.loc[i,"ST_BUY_SELL"]="SELL"

print (data)
