#!/usr/bin/python
'''
Created on May 1, 2017

@author: frederich
'''
import urllib2
from spider.fetch import openCSV
from utility.config import readUrl,readDbDef,strDate,readFloat
def fetch_finance_report(db_index,db_rec,stock):
    table_content=readDbDef('def_finance_report')
    url_finance=readUrl('url_finance_data') % stock[2:]
    try:
        result=openCSV(url_finance,'gb18030').T
        result=result.fillna(0)
        for i in range(1,len(result)-1)[::-1]:
            query_date=strDate(result.index[i])
            EPS=readFloat(result.iloc[i,0])  	
            NAPS=readFloat(result.iloc[i,1])
            CFPS=readFloat(result.iloc[i,2])
            MainInc=readFloat(result.iloc[i,3])
            MP=readFloat(result.iloc[i,4])
            PF=readFloat(result.iloc[i,5])
            InvInc=readFloat(result.iloc[i,6])
            NNOI=readFloat(result.iloc[i,7])
            TP=readFloat(result.iloc[i,8])
            NP=readFloat(result.iloc[i,9])
            NPENRGAL=readFloat(result.iloc[i,10])
            NCF=readFloat(result.iloc[i,11])
            CI=readFloat(result.iloc[i,12])
            TC=readFloat(result.iloc[i,13])
            FC=readFloat(result.iloc[i,14])
            TD=readFloat(result.iloc[i,15])
            ND=readFloat(result.iloc[i,16])
            MinInt=readFloat(result.iloc[i,17])
            ROE=readFloat(result.iloc[i,18])
            insert_content="{date},{EPS},{NAPS},{CFPS},{MainInc},\
    		        {MP},{PF},{InvInc},{NNOI},{TP},{NP},{NPENRGAL},\
    		        {NCF},{CI},{TC},{FC},{TD},{ND},{MinInt},{ROE}"\
                    .format(date=query_date,EPS=EPS,NAPS=NAPS,CFPS=CFPS,\
    					MainInc=MainInc,MP=MP,PF=PF,InvInc=InvInc,NNOI=NNOI,\
    					TP=TP,NP=NP,NPENRGAL=NPENRGAL,NCF=NCF,CI=CI,TC=TC,FC=FC,\
    					TD=TD,ND=ND,MinInt=MinInt,ROE=ROE)
            update_content="EPS={EPS},NAPS={NAPS},CFPS={CFPS},\
                    MainInc={MainInc},MP={MP},PF={PF},InvInc={InvInc},\
                    NNOI={NNOI},TP={TP},NP={NP},NPENRGAL={NPENRGAL},\
                    NCF={NCF},CI={CI},TC={TC},FC={FC},TD={TD},\
                    ND={ND},MinInt={MinInt},ROE={ROE}"\
    				.format(EPS=EPS,NAPS=NAPS,CFPS=CFPS,\
    					MainInc=MainInc,MP=MP,PF=PF,InvInc=InvInc,NNOI=NNOI,\
    					TP=TP,NP=NP,NPENRGAL=NPENRGAL,NCF=NCF,CI=CI,TC=TC,FC=FC,\
    					TD=TD,ND=ND,MinInt=MinInt,ROE=ROE)
            condition_content="date={date}".format(date=query_date)
            db_rec.createTable(stock,table_content)
            try:
                db_rec.insertAllValues(stock,insert_content)
            except:
                db_rec.updateTable(stock,update_content,condition_content)
            report_content='report_time=%s' % query_date
            condition="stock_index='%s'"% stock
            db_index.updateTable('stocks', report_content, condition)
    except urllib2.HTTPError:
        print 'HTTP ERROR 404'
    except Exception,e:
        print Exception,e