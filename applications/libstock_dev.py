#!/usr/bin/python3

"""
Geschafen im Feb 13, 2019
Verfasst von Friederich Fluss
Version
v1.1.4, Feb 13, 2019, rebuild this lib.
"""
from mysql.libmysql8_dev import MySQLBase
__version__ = '1.1.4-dev'

"""
Define the data format transfer between api is in fotmat below.

"""


def create_stock_list(flag='all'):
    indexs = []
    sha = ['SH600000']*4000
    for i in range(len(sha)):
        sha[i] = 'SH' + '60' + str(i).zfill(4)
    sza = ['SZ000001']*1000
    for i in range(len(sza)):
        sza[i] = 'SZ' + str(i).zfill(6)
    cyb = ['SZ300001']*1000
    for i in range(len(cyb)):
        cyb[i] = 'SZ' + '300' + str(i).zfill(3)
    zxb = ['SZ002000']*1000
    for i in range(len(zxb)):
        zxb[i] = 'SZ' + '002' + str(i).zfill(3)
    szb = ['SZ200001']*1000
    for i in range(len(szb)):
        szb[i] = 'SZ' + '200' + str(i).zfill(3)
    shi = ['SH000000']*2000
    for i in range(999):
        shi[i] = 'SH' + str(i).zfill(6)
        shi[i + 1000] = 'SH' + '950' + str(i).zfill(3)
    szi = ['SZ399000']*1000
    for i in range(len(szi)):
        szi[i] = 'SZ' + '399' + str(i).zfill(3)
    hk = ['HK00001']*10000
    for i in range(len(hk)):
        hk[i] = 'HK'+str(i+1).zfill(5)

    if flag == 'all':
        indexs.extend(sha)
        indexs.extend(sza)
        indexs.extend(cyb)
        indexs.extend(zxb)
        indexs.extend(szb)
        indexs.extend(shi)
        indexs.extend(szi)
    elif flag == 'stocks':
        indexs.extend(sha)
        indexs.extend(sza)
    elif flag == 'a':
        indexs.extend(sha)
        indexs.extend(sza)
    elif flag == 'b':
        indexs.extend(shb)
        indexs.extend(szb)
    elif flag == 'zxb':
        indexs.extend(zxb)
    elif flag == 'cyb':
        indexs.extend(cyb)
    elif flag == 'hk':
        indexs.extend(hk)
    else:
        pass
    return indexs


def del_stock(stock_code, serv):
    ms = MySQLBase(serv[0], serv[1], serv[2])
    ms.drop_table(stock_code)
    ms.remove_data('finance.stock_index',
                   "stock_code='{0}'".format(stock_code))
    return 1


class StockEvent(object):
    def __init__(self):
        self.queue = []

    """
    a pool managed by the class
    if not full continue download and fill the pool
    if full, hang the line and wait until space.
    a data recorder write data to databases.
    First in First out.
    """

    def isFull(self):
        if len(self.queue) > 1000:
            return True
        else:
            return False

    def recorder(self):
        pass

    def download(self):
        pass

    def taskqueue(self):
        while Not self.isEmpty():
            if self.isFull():
                sleep(10)
            else:
                self.queue.add()


    def isEmpty(self):
        return False if len(self.queue) else True


if __name__ == '__main__':
    x = create_stock_list()
    serv = ('root', '6414939', 'stock_data')
    del_stock('SH600002', serv)
