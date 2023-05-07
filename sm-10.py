import pandas as pd
import matplotlib.pyplot as plt


def sma(file,percentage):

    df = pd.read_csv(file)

    capital = 1000
    positions = {"long":0 , "long_values":[] , "short":0, "short_values":[]}
    total_value = []

    #Looking at 10-day average. Buy when it dips to 80% of that
    closing_prices = df["Close"]

    #Looping through price data to test 
    for i in range(10,len(closing_prices)-1):

        #Finding 10-day average up to this point i
        average = closing_prices[i-10:i].mean()

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
        
for i in range(1,8,1):
    sma("file:///C:/Users/giand/Desktop/model_dev/testing/RR.L.csv", i/10)

plt.legend()
plt.show()

