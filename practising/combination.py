import pandas as pd
import matplotlib.pyplot as plt
from yahooquery import Ticker, Screener

s = Screener()


###Gets a list of products in a market then saves their symbols in a list

def symbols_from_market(industry, number_of_symbols):

    stock_screen = s.get_screeners(industry,number_of_symbols)

    stock_list = []


    for i in range(number_of_symbols-1):

        stock = stock_screen[industry]["quotes"][i]["symbol"]

        stock_list.append(stock)

    return stock_list

#Gets  ratios of products and saves 1/ratio for each in a list (so that higher is better)

def ratios_inverted(stock_list):

    peg_ratios = []
    pe_ratios = []
    equity_to_debt = []

    for i in stock_list:

        stock = Ticker(i)

        peg_ratios.append(1/stock.valuation_measures["PegRatio"][0])
        pe_ratios.append(1/stock.valuation_measures["PeRatio"][0])
        
        debt = stock.balance_sheet()["TotalDebt"][0]
        equity = stock.balance_sheet()["StockholdersEquity"][0]

        equity_to_debt.append(equity/debt)


    return peg_ratios,pe_ratios,equity_to_debt


# Uses a MA to return a decision on whether there is a trend or not

def current_trend(stock_list):

    trends = []

    for i in stock_list:

        stock = Ticker(i)

        hist = stock.history(period = "3mo")

        closing_prices = hist["close"]


        # Identify ten and fifty day averages
        ten_day_ave = closing_prices[50::].mean()

        fifty_day_ave = closing_prices[10::].mean()

        if ten_day_ave > fifty_day_ave:

            trends.append(0.5)

        else:

            trends.append(-0.5)

    return trends


# Getting score for each product

stocks = symbols_from_market("aerospace_defense",10)
pegs,pes,ed = ratios_inverted(stocks)
trends = current_trend(stocks)

scores  = []
for i in stocks:

    index = stocks.index(i)

    score = pegs[index] + pes[index] + 0.1*ed[index] + trends[index]

    scores.append([i , score])


#sort scores by highest recommended    

def sorted(score):
    return score[1]

scores.sort(reverse = True ,  key = sorted)
print(scores)




