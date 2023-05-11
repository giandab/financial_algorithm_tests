import pandas as pd
import matplotlib.pyplot as plt
from yahooquery import Ticker

#Run the main loop. If find a trend start then run trend function until trend is over. Then revert to using mean function.

#Trend will begin when k day and k*4 day moving averages cross. If the previous k day is lower and next is heigher, it is a positive trend => buy orders. Else, sell

#Trend will revert when averages cross again. Close previous buys or buy more depending on whether it was a positive or negative trend.

#Negative trend detected => Sell everything
#Positive trend detected => Buy single 

def mean_reversion(capital, percentage, closing_prices, positions, average,i,df):
        
        #We do not sell short so we only look to close existing long positions
        if (closing_prices[i+1] >= average*(1+percentage)) and positions["long"]>0:

            print("Closed long position, profit: ",closing_prices[i+1] - positions["long_values"][-1] , )

            #selling adds to capital
            capital += closing_prices[i+1]
            positions["long"] -=1
            positions["long_values"].pop()

        if (closing_prices[i+1] <= average*(1-percentage)) and capital >= closing_prices[i+1]:

            print("Buy at ", closing_prices[i+1],)

            #Buying removes from capital
            capital -= closing_prices[i+1]

            #Open a long position
            positions["long"]+=1
            positions["long_values"].append(closing_prices[i+1])

        return capital , positions



def main(ticker,percentage,k):

    ##Set history period
    stock = Ticker(ticker)
    df=stock.history(period="3y") #default is ytd, 1 day 

    capital = 1000
    positions = {"long":0 , "long_values":[]}
    total_value = []

    #Looking at k-day average. Buy when it dips to 80% of that
    closing_prices = df["close"]

    Trend = [False, ""]

    #Looping through price data to test, starting at k to prevent error
    for i in range(k*4,len(closing_prices)-1):

        #Finding k-day average up to this point i
        average = closing_prices[i-k:i].mean()

        #finding k*4 day average up to i
        big_average = closing_prices[i-(k*4):i].mean()

        #Check if they cross.
        if (closing_prices[i-k:i].mean() > big_average) and (closing_prices[i-k-1:i].mean() < big_average):
             
             #If there was an existing negative trend, end it
             if Trend == [True, "negative"]:
                  Trend = [False, ""]
                  print("negative trend was closed, at price", closing_prices[i],)
             
             elif Trend == [False, ""]:
                  
                Trend = [True, "positive"]
                print("positive trend detected, up until price ", closing_prices[i],)

                #Buying  assets
                capital -= closing_prices[i+1]

                #Open a long position
                positions["long"]+=1
                positions["long_values"].append(closing_prices[i+1])
             


        elif (closing_prices[i-k:i].mean() < big_average) and (closing_prices[i-k-1:i].mean() > big_average):
            
            if Trend == [True, "positive"]:
                 
                print("positive trend was closed at price, ", closing_prices[i],)
                Trend=[False,""]

                #selling asset bought
                capital += closing_prices[i+1]
                positions["long"] -=1
                positions["long_values"].pop()

            elif Trend == [False, ""]:
                 
                Trend = [True, "negative"]
                print("Negative trend detected up until price" , closing_prices[i])

                #Sell everything once negative trend is detected
                number_to_close = positions["long"]

                for x in range(number_to_close):

                     #selling adds to capital
                    capital += closing_prices[i+1]
                    positions["long"] -=1
                    positions["long_values"].pop()


        #If there is no trend , run mean reversion model.
        elif Trend == [False,""]:
             capital , positions = mean_reversion(capital, percentage, closing_prices, positions, average,i,df)
        
        #checking total value at end
        #equal to cash amount + value gained from closing all long positions
        total_value.append(capital + positions["long"]*closing_prices[i+1])


    #Plotting
    plt.plot(total_value, label = percentage)
    plt.title("P&L")
    plt.xlabel("Days")
    plt.ylabel("£")
    plt.show(block=False)
        

main("NIO",1/10, 50)




plt.legend()
plt.show()