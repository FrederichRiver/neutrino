'''
Created on Apr 24, 2017

@author: frederich
'''
import functools
from utility.config import readUrl, readDbDef, netEaseIndex
from spider.fetch import openCSV


def generate_list(flag='all'):
        # stocks: stocks only
        # indexs: indexs only
        # sh: stocks in sh only
        # sz: stocks in sz only
        # a: A stock only sh & sz
        # b: B stock only sh & sz
        # h: stocks in hongkong
        # zxb: ZXB only
        # cyb: CYB only
        # funds: funds only
        indexs = []
        if flag == 'all' or flag == 'stocks' or flag == 'a' or flag == 'sh':
            SHA = ['SH600000']*4000
            for i in range(len(SHA)):
                SHA[i] = 'SH' + '60' + str(i).zfill(4)
            indexs.extend(SHA)
        if flag == 'all' or flag == 'stocks' or flag == 'a' or flag == 'sz':    
            SZA = ['SZ000001']*1000
            for i in range(len(SZA)):
                SZA[i] = 'SZ' + str(i).zfill(6)
            indexs.extend(SZA)
        if flag == 'all' or flag == 'stocks' or flag == 'a' or flag == 'sz' or flag == 'cyb':
            CYB = ['SZ300001']*1000
            for i in range(len(CYB)):
                CYB[i] = 'SZ' + '300' + str(i).zfill(3)
            indexs.extend(CYB)
        if flag == 'all' or flag == 'stocks' or flag == 'a' or flag == 'sz'or flag == 'zxb':
            ZXB = ['SZ002000']*1000
            for i in range(len(ZXB)):
                ZXB[i] = 'SZ' + '002' + str(i).zfill(3)
            indexs.extend(ZXB)
        if flag == 'all' or flag == 'stocks' or flag == 'b' or flag == 'sz':
            SZB = ['SZ200001']*1000
            for i in range(len(SZB)):
                SZB[i] = 'SZ' + '200' + str(i).zfill(3)
            indexs.extend(SZB)
        # Indexs
        if flag == 'all' or flag == 'indexs' or flag == 'shi':
            SHI = ['SH000000']*2000
            for i in range(999):
                SHI[i] = 'SH' + str(i).zfill(6)
                SHI[i + 1000] = 'SH' + '950' + str(i).zfill(3)
            indexs.extend(SHI)
        if flag == 'all' or flag == 'indexs' or flag == 'szi':
            SZI = ['SZ399000']*1000
            for i in range(len(SZI)):
                SZI[i] = 'SZ' + '399' + str(i).zfill(3)
            indexs.extend(SZI)
        return indexs


def query_index_list(db, tab):
    """
    db:database of 'indexs'
    today:date of today which is a 8bit integer
    """
    index_list = db.selectValues(tab=tab, col='stock_index')
    result = []
    for index in index_list:
        result.append(index[0])
    return result

query_index = functools.partial(query_index_list, tab= 'indexs')
query_stock = functools.partial(query_index_list, tab= 'stocks')

def search_index(x, tab, db_index, db_rec, today):
    """     x: stock index which is in format of 'SH600001'
            tab: table name which is 'indexs.stocks'
            db1: database of 'indexs'
            db2: database of 'stock_data'
            today: today is a integer in format of 8 integer numbers.
    """
    """    from config read url of 'http://money.163.com'    """
    url_ne_index = readUrl('url_ne_index')
    query_index = netEaseIndex(x)
    netease_stock_indexs_url = url_ne_index % (query_index, today)
    try:
        result = openCSV(netease_stock_indexs_url, 'gb18030')
        if len(result) > 0:
            print x, result.iloc[1, 2]
            stock_name = result.iloc[1, 2].replace(' ', '')
            content = readDbDef('def_index')
            db_rec.createTable(x, content)
            db_index.insertValues(tab,
                                  "stock_index,stock_name",
                                  "'%s','%s'" % (x, stock_name))
    except Exception:
        pass
        # time.sleep(10)
