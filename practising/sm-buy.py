import pandas as pd
import matplotlib.pyplot as plt
from yahooquery import Ticker


def sma(ticker,percentage,k):

    ##Set history period
    stock = Ticker(ticker)
    df=stock.history(period="1y") #default is ytd, 1 day 

    capital = 100000
    positions = {"long":0 , "long_values":[]}
    total_value = []

    #Looking at k-day average. Buy when it dips to 80% of that
    closing_prices = df["close"]

    #Looping through price data to test, starting at k to prevent error
    for i in range(k,len(closing_prices)-1):

        #Finding k-day average up to this point i
        average = closing_prices[i-k:i].mean()

        #We do not sell short so we only look to close existing long positions
        if (closing_prices[i+1] >= average*(1+percentage)) and positions["long"]>0:

            print("Closed long position, profit: ",closing_prices[i+1] - positions["long_values"][-1] )

            #selling adds to capital
            capital += closing_prices[i+1]
            positions["long"] -=1
            positions["long_values"].pop()

        if (closing_prices[i+1] <= average*(1-percentage)) and capital >= closing_prices[i+1]:

            print("Buy at ", closing_prices[i+1])

            #Buying removes from capital
            capital -= closing_prices[i+1]

            #Open a long position
            positions["long"]+=1
            positions["long_values"].append(closing_prices[i+1])

        #checking total value at end
        #equal to cash amount + value gained from closing all long positions + value lost from closing all short positions
        total_value.append(capital + positions["long"]*closing_prices[i+1])


    #Plotting
    plt.plot(total_value, label = percentage)
    plt.title("P&L")
    plt.xlabel("Days")
    plt.ylabel("£")
    plt.show(block=False)
        

sma("TSLA",1/10, 50)




plt.legend()
plt.show()