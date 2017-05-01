'''
Created on Apr 24, 2017

@author: frederich
'''
from utility.config import readUrl,readDbDef,netEaseIndex
def generate_list(flag='all'):
        #stocks: stocks only
        #indexs: indexs only
        #sh: stocks in sh only
        #sz: stocks in sz only
        #a: A stock only sh & sz
        #b: B stock only sh & sz
        #h: stocks in hongkong
        #zxb: ZXB only
        #cyb: CYB only
        #funds: funds only
        indexs=[]
        if flag=='all' or flag=='stocks' or flag=='a' or flag=='sh':
            SHA=['SH600000']*4000
            for i in range(len(SHA)):
                SHA[i]='SH'+'60'+str(i).zfill(4)
            indexs.extend(SHA)
        if flag=='all' or flag=='stocks' or flag=='a' or flag=='sz':    
            SZA=['SZ000001']*1000
            for i in range(len(SZA)):
                SZA[i]='SZ'+str(i).zfill(6)
            indexs.extend(SZA)
        if flag=='all' or flag=='stocks' or flag=='a' or flag=='sz' or flag=='cyb':
            CYB=['SZ300001']*1000
            for i in range(len(CYB)):
                CYB[i]='SZ'+'300'+str(i).zfill(3)
            indexs.extend(CYB)
        if flag=='all' or flag=='stocks' or flag=='a' or flag=='sz'or flag=='zxb':
            ZXB=['SZ002000']*1000
            for i in range(len(ZXB)):
                ZXB[i]='SZ'+'002'+str(i).zfill(3)
            indexs.extend(ZXB)
        if flag=='all' or flag=='stocks' or flag=='b' or flag=='sz':
            SZB=['SZ200001']*1000
            for i in range(len(SZB)):
                SZB[i]='SZ'+'200'+str(i).zfill(3)
            indexs.extend(SZB)
        #Indexs
        if flag=='all' or flag=='indexs' or flag=='shi':
            SHI=['SH000000']*2000
            for i in range(999):
                SHI[i]='SH'+str(i).zfill(6)
                SHI[i+1000]='SH'+'950'+str(i).zfill(3)
            indexs.extend(SHI)
        if flag=='all' or flag=='indexs' or flag=='szi':
            SZI=['SZ399000']*1000
            for i in range(len(SZI)):
                SZI[i]='SZ'+'399'+str(i).zfill(3)
            indexs.extend(SZI)
        return indexs
def queryindex(db,today,flag='indexs'):
    """
    db:database of 'indexs'
    today:date of today which is a 8bit integer
    """
    indexs=db.selectValues(flag,'stock_index')
    result=[]
    for index in indexs:
        result.append(index[0])
    return result
def searchindex(x,tab,db1,db2,today):
    """     x: stock index which is in format of 'SH600001'    
            tab: table name which is 'indexs.stocks'
            db1: database of 'indexs'
            db2: database of 'stock_data'
            today: today is a integer in format of 8 integer numbers.      """
    import urllib2
    from io import StringIO
    import pandas as pd
    """    from config read url of 'http://money.163.com'    """
    url_ne_index=readUrl('url_ne_index')
    query_index=netEaseIndex(x)
    netease_stock_indexs_url=url_ne_index % (query_index,today)
    try:
        resp=urllib2.urlopen(netease_stock_indexs_url,timeout=10)
        csv_content=resp.read().decode('gb18030')
        mMatrix=StringIO(csv_content)
        result=pd.read_csv(mMatrix)
        if len(result)>0:
            print x,result.iloc[1,2]
            stock_name=result.iloc[1,2].replace(' ','')
    
            content=readDbDef('def_index')
            db2.createTable(x,content)
            db1.insertValues( tab, "stock_index,stock_name","'%s','%s'" %(x,stock_name))            
                                        
    except Exception,e:
        import time
        print e
        time.sleep(10) 