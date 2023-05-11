import pandas as pd
import matplotlib.pyplot as plt
from yahooquery import Ticker


def sma(ticker,percentage,k):

    ##Set history period
    stock = Ticker(ticker)
    df=stock.history(period="2y") #default is ytd, 1 day 

    capital = 1000
    positions = {"long":0 , "long_values":[] , "short":0, "short_values":[]}
    total_value = []

    #Looking at k-day average. Buy when it dips to 80% of that
    closing_prices = df["close"]

    #Looping through price data to test 
    for i in range(k,len(closing_prices)-1):

        #Finding k-day average up to this point i
        average = closing_prices[i-k:i].mean()

        if closing_prices[i+1] >= average*(1+percentage):

            print("Sell at ",closing_prices[i+1] )

            #selling adds to capital
            capital += closing_prices[i+1]

            # if we have no long positions, open a short one
            if positions["long"] == 0:
                positions["short"] += 1
                positions["short_values"].append(closing_prices[i+1])

            #else close a long one
            else:
                positions["long"] -=1
                positions["long_values"].pop()

        elif closing_prices[i+1] <= average*(1-percentage):

            print("Buy at ", closing_prices[i+1])

            #Buying removes from capital
            capital -= closing_prices[i+1]

            #If we have no short positions, create a long one
            if positions["short"] == 0:
                positions["long"]+=1
                positions["long_values"].append(closing_prices[i+1])

            #else close a short one
            else:
                positions["short"]-=1
                positions["short_values"].pop()

        #checking total value at end
        #equal to cash amount + value gained from closing all long positions + value lost from closing all short positions
        total_value.append(capital + positions["long"]*closing_prices[i+1] - positions["short"]*closing_prices[i+1])


    #Plotting
    plt.plot(total_value, label = percentage)
    plt.title("P&L")
    plt.xlabel("Days")
    plt.ylabel("£")
    plt.show(block=False)
        

sma("TSLA",1/100, 50)




plt.legend()
plt.show()

