#!/usr/bin/python
#coding:utf8
'''
Created on Apr 29, 2017

@author: frederich
'''
import urllib2
from utility.config import readUrl,readDbDef,netEaseIndex,strDate


def fetch_stock(db1,db2,tab,index,today):
    from io import StringIO
    import pandas as pd
    print index
    url_ne_stock=readUrl('url_ne_stock')
    db2.createTable(index,readDbDef('def_stock'))           
    query_index=netEaseIndex(index)
    update=int(db1.selectOne(tab, 'update_time', "stock_index='%s'"% index)[-1])
    netease_stocks_url=url_ne_stock % (query_index,update,today)
    try:
        resp=urllib2.urlopen(netease_stocks_url,timeout=10)
        csv_content=resp.read().decode('gb18030')
        mMatrix=StringIO(csv_content)
        result=pd.read_csv(mMatrix)
        for i in range(0,result.shape[0])[::-1]:   
            query_date=strDate(result.iloc[i,0])
            CP=result.iloc[i,3]
            HP=result.iloc[i,4]
            LP=result.iloc[i,5]
            OP=result.iloc[i,6]
            YOP=result.iloc[i,7]
            AMP=result.iloc[i,9]
            VolT=result.iloc[i,10]
            ValT=result.iloc[i,11]
            if db2.selectValues(index,'*','date=%s'% query_date)==():
                try:
                    columns='date,CP,HP,LP,OP,YOP,AMP,VolT,ValT'
                    content="%s,%s,%s,%s,%s,%s,%s,%s,%s"\
                     % (query_date,CP,HP,LP,OP,YOP,AMP,VolT,ValT)
                    #print content
                    db2.insertValues(index,columns, content)
                except Exception,e:
                    print Exception, ":",e                    
            else:
                try:
                    content='CP=%s,HP=%s,LP=%s,OP=%s,\
                            YOP=%s,AMP=%s,VolT=%s,ValT=%s'\
                             %(CP, HP,LP,OP,YOP,AMP,VolT,ValT)
                    db2.updateTable( index, content, 'date=%s' % query_date)
                except Exception,e:
                    print Exception,":",e
            db1.updateTable(tab, 'update_time=%s' % query_date, "stock_index='%s'" % index)
    except Exception,e:
        print Exception,e
def setSTflag():
    cfg=readAccount()
        db=mysql('localhost',cfg[0],cfg[1],'indexs')
        stocks=db.selectValues('stocks','stock_name')
        for stock in stocks:
            if 'ST' in stock[0]:
                db.updateTable('stocks',"flag='S'","stock_name='%s'" % stock[0])
def setQuitflag():
    cfg=readAccount()
        db=mysql('localhost',cfg[0],cfg[1],'indexs')
        stocks=db.selectValues('stocks','stock_name')
        for stock in stocks:
            if '退市' in stock[0]:
                db.updateTable('stocks',"flag='Q'","stock_name='%s'" % stock[0])