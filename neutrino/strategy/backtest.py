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
from statsmodels.regression.linear_model import OLS

class backTestBase(object):

    def __init__(self):
        pass

def fetch_interest_rate(cycle= 1.0):
    return 0.0175

def beta_regression(stock, market, start_time, end_time):
    stock_data = fetch_stock_close(stock, start_time, end_time)
    stock_data.columns = [stock]
    market_data = fetch_stock_close(market, start_time, end_time)
    market_data.columns = [market]
    price_data = stock_data.join(market_data)
    if price_data.shape[0] :
        price_data = dataCleaning(price_data)
        interest_data = (price_data[1:] / price_data[:-1].values) - 1
    
        result = OLS(interest_data[stock],interest_data[market]).fit()
        #plt.plot(interest_data[market], interest_data[stock], 'ob').
        return stock,result.params[0]
    else:
        return stock, 0.0
if __name__ == '__main__':
    """
    beta = beta_regression('SH600016', 'SH600036', '2017-01-01', '2017-10-01')
    """
    from dataEngine.index import query_stock_list
    stock_list = query_stock_list()[1:]
    betas = {}
    for stock in stock_list:
        code, beta = beta_regression(stock, 'SH600000', '2017-01-01', '2017-10-01')
        if beta>0.7 : print stock, beta
        betas[code] = beta
    print betas