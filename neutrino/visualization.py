'''
Created on Oct 12, 2017

@author: frederich
'''
import datetime as dt
from dataEngine.stock import fetch_stock_data
from matplotlib.finance import candlestick_ohlc
from matplotlib import dates as mdates
import matplotlib.pyplot as plt

stock_code = 'SH600000'
MA10 = 10
MA50 = 50

def k_plot(stock_code):
    """
    It is a subroutine which can execute a k plot of stock. 
    Returns nothing.
    """
    stock_data = fetch_stock_data(stock_code)
    # candlestick_ohlc use dataframe as [date,open,highest,lowest,close]
    # date should be float date form and we get datetime64
    # convert type of date.
    stock_data = stock_data.reset_index()
    stock_data['date'] = mdates.date2num(stock_data['date'].astype(dt.date))
    stock_data = stock_data.reindex(columns= ['date','Open','Highest','Lowest','Close'])
    # SP is used for moving average curve.
    SP = len(stock_data.values[MA10-1:])
    SP = 50
    # basic figure setting.
    fig = plt.figure(facecolor = '#07000d', figsize=(15, 10))
    ax1 = plt.subplot2grid((6,4), (1,0), rowspan=4, colspan=4,axisbg='#07000d')
    candlestick_ohlc(ax1, 
                     stock_data.values[:], 
                     width=0.3,
                     colorup='#ff1717',
                     colordown='#53c156')
    ax1.grid(True, color='w')
    ax1.tick_params(axis='x',colors='w')
    ax1.tick_params(axis='y',colors='w')
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    # setting axis label.
    ax1.xaxis.label.set_color('w')
    ax1.yaxis.label.set_color('w')
    # setting color of exterior lines.
    ax1.spines['top'].set_color('#5998ff')
    ax1.spines['bottom'].set_color('#5998ff')
    ax1.spines['left'].set_color('#5998ff')
    ax1.spines['right'].set_color('#5998ff')
    plt.xlabel('Date')
    plt.ylabel('Stock price and Volume')
    plt.show()
    
    
k_plot('SH600000')
'''
startdate = dt.date(2016, 6, 29)
enddate = dt.date(2017, 1, 30)
#print enddate
'''