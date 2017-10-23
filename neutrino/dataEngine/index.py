'''
Created on Apr 24, 2017

@author: frederich
'''
import functools
from utility.config import readUrl, readDbDef, netEaseIndex
from spider.fetch import openCSV
from libmysql import MySQLServer
from globalVar import INDEX_DB, STOCK_DATA_DB
from dataEngine.stock import fetch_stock
from utility.config import strDate, dateStr


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

def update_data():
        querydb = MySQLServer(acc='stock',
                              pw='stock2017',
                              database=INDEX_DB)
        recdb = MySQLServer(acc='root',
                            pw='6414939',
                            database=STOCK_DATA_DB)
        stock_list = query_stock(querydb)
        for stock in stock_list:
            fetch_stock(querydb, recdb, 'stocks', stock, dateStr())

def generate_index():
    stock_list = pre_stock_list()
    querydb=MySQLServer(acc='stock',
                        pw='stock2017',
                        database=INDEX_DB)
    createdb = MySQLServer(acc='root',
                           pw='6414939',
                           database=STOCK_DATA_DB)        
    for stock in stock_list:
        search_index(stock,'stocks',querydb,createdb,strDate)
    
def pre_stock_list():
    '''
    This function generate a stock list, which contains all codes.
    From SH600000 to SZ399999.
    -----
    Returns:
        new_list: a char type list object
    '''   
    gen_list = generate_list('stocks')
    querydb = MySQLServer(acc='stock',
                          pw='stock2017',
                          database=INDEX_DB)
    old_list = query_stock(querydb)
    new_list = []
    for index in gen_list:
        if index not in old_list:
            new_list.append(index)
    print 'gen_list:', len(gen_list)
    print 'old_list:', len(old_list)
    print 'new_list:', len(new_list)
    return new_list
        
def pre_index_list():   
    gen_list = generate_list('indexs')
    querydb = MySQLServer(acc='stock',
                          pw='stock2017',
                          database=INDEX_DB)
    old_list = query_index(querydb)
    new_list = []
    for index in gen_list:
        if index not in old_list:
            new_list.append(index)
def query_stock_list():
    querydb = MySQLServer(acc='stock',
                          pw='stock2017',
                          database=INDEX_DB)
    return query_stock(querydb)
