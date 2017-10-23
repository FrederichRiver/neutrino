'''
Created on Oct 22, 2017

@author: frederich
'''
"""
Designed by Frederich River.
It is a method for strategy backtesting.
It is base on genetic algorithm.
"""
from dataEngine.stock import fetch_stock_close, dataCleaning
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.formula.api import ols

class backTestBase(object):

    def __init__(self):
        pass

def fetch_interest_rate(cycle= 1.0):
    return 0.0175

def beta_capm(stock, market, start_time, end_time):
    beta = 1.0
    stock_data = fetch_stock_close(stock, start_time, end_time)
    stock_data.columns = [stock]
    market_data = fetch_stock_close(market, start_time, end_time)
    market_data.columns = [market]
    price_data = stock_data.join(market_data)
    price_data = dataCleaning(price_data)
    interest_data = (price_data[1:] / price_data[:-1].values) - 1
    print interest_data
    #print price_data
    result = pd.ols(y=interest_data[stock],x=interest_data[market])
    print 'beta =', result.beta
    plt.plot(interest_data[market], interest_data[stock],'ob')
    
    plt.show()

if __name__ == '__main__':
    beta_capm('SH600016', 'SH600036', '2017-01-01', '2017-10-01')
