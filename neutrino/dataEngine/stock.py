#!/usr/bin/python
#coding:utf8
'''
Created on Apr 29, 2017

@author: frederich
'''
from utility.config import readUrl,strDate,netEaseIndex
from spider.fetch import openCSV
from libmysql import MySQLServer
from pandas import read_sql_query
import pandas as pd
import matplotlib.pyplot as plt    
import numpy as np
from utility.config import InfoLog

def fetch_stock(db_index,db_rec,tab,index,today):
    """
    1.Get stock data from www.163.com.
    2.Write data into database.
    3.Update a global table to record update history.
    ---
    It is an event and returns nothing.
    """
    InfoLog('update %s' %index)
    print index
    url_ne_stock = readUrl('url_ne_stock')
    query_index = netEaseIndex(index)
    update = db_index.selectOne(tab, 'update_time', "stock_index='%s'"% index)[-1]
    netease_stocks_url=url_ne_stock % (query_index,strDate(update),strDate(today))
    try:
        result=openCSV(netease_stocks_url,'gb18030')
        result.replace('None',0.0)
        for i in range(0,result.shape[0])[::-1]:  
            query_date=result.iloc[i,0]
            CP=result.iloc[i,3]
            HP=result.iloc[i,4]
            LP=result.iloc[i,5]
            OP=result.iloc[i,6]
            YCP=result.iloc[i,7]
            AMP=result.iloc[i,9]
            VolT=result.iloc[i,10]
            ValT=result.iloc[i,11]
            if db_rec.selectValues(index,'*',"date='%s'"% query_date)==():
                try:
                    columns='date,CP,HP,LP,OP,YCP,AMP,VolT,ValT'
                    content="'%s',%s,%s,%s,%s,%s,%s,%s,%s"\
                     % (query_date,CP,HP,LP,OP,YCP,AMP,VolT,ValT)
                    db_rec.insertValues(index,columns, content)
                except Exception,e:
                    InfoLog(e, 'ERROR')                   
            else:
                try:
                    content='CP=%s,HP=%s,LP=%s,OP=%s,\
                            YCP=%s,AMP=%s,VolT=%s,ValT=%s'\
                             %(CP, HP,LP,OP,YCP,AMP,VolT,ValT)
                    db_rec.updateTable( index, content, "date='%s'" % query_date)
                    #print query_date
                except Exception,e:
                    InfoLog(e, 'ERROR')
            db_index.updateTable(tab, "update_time='%s'" % query_date, "stock_index='%s'" % index)
    except Exception,e:
        InfoLog(e, 'ERROR')

def fetch_stock_data(stock):
    """
    Select data from a table stock_data.%Stock_Code.
    Returns a dataFrame object for k plot.
    ---
    DataFrame:
        index: a date time index
        Open: opening price
        Close: closing price
        Lowest: lowest price in a day
        Highest: highest price in a day
        Volume: volume    
    """
    querydb = MySQLServer(acc='stock',
                          pw='stock2017',
                          database='stock_data')
    sql = 'select date,OP,HP,LP,CP from {stock}'.format(stock=stock)
    df = read_sql_query(sql, querydb._db)
    df['date'] = pd.to_datetime(df['date'])
    df.columns = ['date','Open','Highest','Lowest','Close']
    return df
def fetch_stock_close(stock, start_time, end_time):
    """
    Select opening price from a table stock_data.%Stock_Code.
    Returns a dataFrame object.
    ---
    DataFrame:
        index: a date time index
        Open: opening price
    """
    querydb = MySQLServer(acc='stock',
                          pw='stock2017',
                          database='stock_data')
    sql = "select date, CP from {stock} WHERE date BETWEEN '{starttime}' AND '{endtime}'".format(
        stock=stock,
        starttime=start_time,
        endtime=end_time)
    df = read_sql_query(sql, querydb._db)
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index(['date'])
    df.columns = ['Close']
    return df
def fetch_most_correlation(threshold=0.7):
    pass
def create_series(stock):
    s = fetch_stock_close(stock)
    s.columns = [stock]
    return s
def corrMatrix(*args):
    '''
    Not used.
    Calculate the relationship coefficients of series in a dataFrame.
    ---
    Input: Series type object
    Return: corr matrix in terms of dataFrame. 
    '''
    for series in args:
        series = series.join(series)
    return series.corr
def dataCleaning(df):
    for j in range(1,df.shape[1]):
        if np.isnan(df.iloc[0,j]):
            df.iloc[0,j]=0.0
    for i in range(1,df.shape[0]):
        for j in range(1,df.shape[1]):
            if np.isnan(df.iloc[i,j]):
                df.iloc[i,j] = df.iloc[i-1,j]
    return df
def Test1():
    '''
    Test case to calculate correlation coefficient between 2 stocks.
    '''
    stock1='SH600005'
    stock2='SH600010'
    stime = '2016-01-01'
    etime = '2017-01-01'
    s1 = fetch_stock_close(stock1, stime ,etime)
    s2 = fetch_stock_close(stock2, stime ,etime)
    s1.columns = [stock1]
    s2.columns = [stock2]
    print s1.__len__()
    print s2.__len__()
    s3 = s1.join(s2)
    s3 = dataCleaning(s3)
    print s3.corr()
    s3.plot(y=[stock1,stock2])
    plt.show()            
    print 'finish'
def Test2():
    '''
    Test case for calculate coefficients between many stocks.
    '''
    stime = '2016-01-01'
    etime = '2017-01-01'
    from dataEngine.index import query_stock_list
    stock_list = query_stock_list()[1:20]
    stock_data = fetch_stock_close('SH600000', stime, etime)
    stock_data.columns = ['SH600000']
    for stock in stock_list:
        result = fetch_stock_close(stock, stime, etime)
        result.columns = [stock]
        stock_data = stock_data.join(result)
    stock_data = dataCleaning(stock_data)
    print stock_data.corr()

if __name__ == '__main__':
    stime = '2016-01-01'
    etime = '2017-01-01'
    from dataEngine.index import query_stock_list
    stock_list = query_stock_list()[1:20]
    stock_data = fetch_stock_close('SH600000', stime, etime)
    stock_data.columns = ['SH600000']
    for stock in stock_list:
        result = fetch_stock_close(stock, stime, etime)
        result.columns = [stock]
        stock_data = stock_data.join(result)
    stock_data = dataCleaning(stock_data)
    print stock_data.corr()