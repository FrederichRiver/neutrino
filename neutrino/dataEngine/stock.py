#!/usr/bin/python
#coding:utf8
'''
Created on Apr 29, 2017

@author: frederich
'''
from utility.config import readUrl,strDate,netEaseIndex,readAccount
from spider.fetch import openCSV
from libmysql import MySQLServer
from pandas import pandas as pd
from pandas import read_sql_query
    
def fetch_stock(db_index,db_rec,tab,index,today):
    print index
    url_ne_stock=readUrl('url_ne_stock')
    query_index=netEaseIndex(index)
    update=db_index.selectOne(tab, 'update_time', "stock_index='%s'"% index)[-1]
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
                    #print query_date
                except Exception,e:
                    print Exception, ":",e                    
            else:
                try:
                    content='CP=%s,HP=%s,LP=%s,OP=%s,\
                            YCP=%s,AMP=%s,VolT=%s,ValT=%s'\
                             %(CP, HP,LP,OP,YCP,AMP,VolT,ValT)
                    db_rec.updateTable( index, content, "date='%s'" % query_date)
                    #print query_date
                except Exception,e:
                    print Exception,":",e
            db_index.updateTable(tab, "update_time='%s'" % query_date, "stock_index='%s'" % index)
    except Exception,e:
        print Exception,e

def fetch_stock_data(stock):
    querydb = MySQLServer(acc='stock',
                          pw='stock2017',
                          database='stock_data')
    sql = 'select OP,CP,LP,HP,VolT from {stock}'.format(stock=stock)
    df = read_sql_query(sql, querydb._db)
    df.columns = ['Open','Close','Lowest','Highest','Volume']
if __name__ == '__main__':
    print fetch_stock_data('SH600000')
    