import pandas as pd
import matplotlib.pyplot as plt
from yahooquery import Ticker, Screener
import math
import time

s = Screener()


###Gets a list of products in a market then saves their symbols in a list

def symbols_from_market(industry, number_of_symbols):

    stock_screen = s.get_screeners(industry,number_of_symbols)

    stock_list = []


    for i in range(number_of_symbols-1):

        stock = stock_screen[industry]["quotes"][i]["symbol"]

        stock_list.append(stock)

    return stock_list

def update_holdings(date):
    #Gets  ratios of products and saves 1/ratio for each in a list (so that higher is better)

    def ratios_inverted(stock_list,date):

        peg_ratios = []
        pe_ratios = []
        equity_to_debt = []

        for i in stock_list:

            stock = Ticker(i)

            try:
                peg_ratios.append(1/get_measure("PegRatio" , stock,date))
            except Exception as e:
                print(e)
                peg_ratios.append(0)

            try:
                pe_ratios.append(1/get_measure("PeRatio" , stock,date))
            except:
                pe_ratios.append(0)
            

            #Is reported once a year so would not expect to fluctuate
            debt = stock.balance_sheet()["TotalDebt"][0]
            equity = stock.balance_sheet()["StockholdersEquity"][0]

            if math.isnan(equity/debt):
                equity_to_debt.append(0)
            else:
                equity_to_debt.append(equity/debt)


        return peg_ratios,pe_ratios,equity_to_debt


    # Uses a MA to return a decision on whether there is a trend or not

    def current_trend(stock_list,date):

        trends = []

        for i in stock_list:

            stock = Ticker(i)

            hist = stock.history(period="3y")
            
            #Making sure we are only using dates before the "current" date - to anable backtesting
            counter = 0
            while (time.strptime(str(hist.index[counter][1]), "%Y-%m-%d")) < date :
                counter +=1
            
            closing_prices = hist[counter::]["close"]
            #This has created a dataframe where the "current" date is at position 0 and the oldest at position -1 (the end)


            # Identify ten and fifty day averages
            ten_day_ave = closing_prices[:50].mean()

            fifty_day_ave = closing_prices[:10].mean()

            if ten_day_ave > fifty_day_ave:

                trends.append(0.5)

            else:

                trends.append(-0.5)

        return trends


    #have a loop for each measure that will give us the last measure on the closest previous date that isnt "NaN"
    def get_measure(measure, stock, date):
        options = stock.valuation_measures[measure]
        counter  = -1

        #picks from correct date - to enable backtesting
        while math.isnan(options[counter]) or (time.strptime(str(stock.valuation_measures["asOfDate"][counter])[0:10], "%Y-%m-%d")) > date:
            counter-=1

        return options[counter]



    # Getting score for each product

    stocks = symbols_from_market("semiconductors",10)
    pegs,pes,ed = ratios_inverted(stocks,date)
    trends = current_trend(stocks,date)

    scores  = []
    for i in stocks:

        index = stocks.index(i)
        ##Testing##
        print("stock: ", i , " peg: ", pegs[index], " pes: ", pes[index], " equity to debt: ",ed[index], " trend: " ,trends[index] )
        score = pegs[index] + 10*pes[index] + 0.1*ed[index] + trends[index]

        scores.append([i , score])


    #sort scores by highest recommended    

    def sorted(score):
        return score[1]

    scores.sort(reverse = True ,  key = sorted)
    print(scores)

#testing time#
time_1 = "2023/05/19"
newtime = time.strptime(time_1, "%Y/%m/%d")
update_holdings(newtime)




