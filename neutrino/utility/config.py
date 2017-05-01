'''
Created on Apr 23, 2017

@author: frederich
'''
import time
def readAccount(filename='config'):
    from ConfigParser import ConfigParser
    try:
        cf=ConfigParser()
        cf.read(filename)
        acc=cf.get('db','ACC')
        pw=cf.get('db','PW')
        return acc,pw
    except:
        return None
def dateStr(t=time.localtime()):
    return time.strftime('%Y%m%d',t)
def strDate(objstr):
    try:
        return int( objstr.replace('-',''))
    except:
        return 0
def readUrl(query,filename='config'):
    from ConfigParser import ConfigParser
    try:
        cf=ConfigParser()
        cf.read(filename)
        url=cf.get('url',query)
        return url
    except:
        return None
def readDbDef(query,filename='config'):
    from ConfigParser import ConfigParser
    try:
        cf=ConfigParser()
        cf.read(filename)
        DBdef=cf.get('DBdef',query)
        return DBdef
    except:
        return None
def netEaseIndex(index):
    if index[0:2]=='SH':
        return index.replace('SH','0')
    elif index[0:2]=='SZ':
        return index.replace('SZ','1')  
    else:
        return None