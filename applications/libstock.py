#!/usr/bin/python3

"""
Geschafen im Feb 13, 2019
Verfasst von Friederich Fluss
Version
v1.1.4, Feb 13, 2019, rebuild this lib.
v1.2.5, Feb 17, 2019, build class stockeventbase, not perfect.
"""
from datetime import *
__version__ = '1.2.4-dev'


def create_stock_list(flag='all'):
    indices = []
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
        indices.extend(sha)
        indices.extend(sza)
        indices.extend(cyb)
        indices.extend(zxb)
        indices.extend(szb)
        indices.extend(shi)
        indices.extend(szi)
    elif flag == 'stocks':
        indices.extend(sha)
        indices.extend(sza)
    elif flag == 'a':
        indices.extend(sha)
        indices.extend(sza)
    elif flag == 'b':
        indices.extend(shb)
        indices.extend(szb)
    elif flag == 'zxb':
        indices.extend(zxb)
    elif flag == 'cyb':
        indices.extend(cyb)
    elif flag == 'hk':
        indices.extend(hk)
    else:
        pass
    return indices


class StockEventBase(object):
    def __init__(self):
        self.queue = []
        self.code = {}
        self.today = datetime.now().strftime('%Y-%m-%d')

    def __repr__(self):
        return self.today


if __name__ == '__main__':
    event = StockEventBase()
    print(event)
