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

#Gets peg ratios of products and saves 1/peg for each in a list (so that higher is better)

def peg_ratios_list(stock_list):

    peg_ratios = []

    for i in stock_list:

        stock = Ticker(i)

        peg_ratios.append(1/stock.valuation_measures["PegRatio"][0])

    return peg_ratios



#### TESTING ####

stocks = symbols_from_market("semiconductors",15)
pegs = peg_ratios_list(stocks)

print(stocks)
print(pegs)




