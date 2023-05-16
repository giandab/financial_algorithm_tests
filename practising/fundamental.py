import pandas as pd
import matplotlib.pyplot as plt
from yahooquery import Ticker, Screener

s = Screener()


###Gets products from a screener and returns the peg ratio for each


print(s.available_screeners)

cars = s.get_screeners("semiconductors",15)
print(cars)

for i in range(14):
    print(cars["semiconductors"]["quotes"][i]["symbol"])
    stock = Ticker(cars["semiconductors"]["quotes"][i]["symbol"])
    print(stock.valuation_measures["PegRatio"][0])

