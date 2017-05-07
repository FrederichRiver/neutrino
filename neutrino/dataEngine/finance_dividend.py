#!/usr/bin/python
'''
Created on May 4, 2017
@author: frederich
'''
from utility.config import readUrl,readDbDef,strDate,readFloat
import pandas as pd
def fetch_finance_dividend(db_rec,stock):
    table_content=readDbDef('def_finance_dividend')
    url_finance_dividend=readUrl('url_finance_dividend') % stock[2:]
    try:
        db_rec.createTable(stock,table_content)
        result=pd.read_html(url_finance_dividend)
        for i in range(len(result[3]))[::-1]:
            year=result[3].iloc[i,1]
            report_date=strDate(result[3].iloc[i,0])
            record_date=strDate(result[3].iloc[i,5])
            send=readFloat(result[3].iloc[i,2])
            increase=readFloat(result[3].iloc[i,3])
            dividend=readFloat(result[3].iloc[i,4])
            #print report_date,send,increase,dividend,record_date
            column_content="report_date, year, record_date, send, increase, dividend"
            insert_content="%s,%s,%s,%s,%s,%s" %(report_date,year,record_date,send,increase,dividend)
            update_content="year=%s, record_date=%s, send=%s, increase=%s, dividend=%s" % (year,record_date,send,increase,dividend)
            condition_content="report_date=%s" % report_date
            #print column_content,insert_content
            try:
                db_rec.insertValues(stock,column_content,insert_content)
            except:
                db_rec.updateTable(stock,update_content,condition_content)
    except Exception,e:
        print Exception,e