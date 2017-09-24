#!/usr/bin/python
'''
Created on Aug 27, 2017

@author: frederich
'''
import Pyro4
from libmysql import MySQLServer


if __name__ == '__main__':
    dbAdmin = MySQLServer('localhost', 'root', '6414939', 'test')
    dbStock = MySQLServer('localhost', 'stock', 'stock2017', 'stock_data')
    dbIndex = MySQLServer('localhost', 'stock', 'stock2017', 'indexs')
    Pyro4.Daemon.serveSimple(
        {
            dbAdmin: 'dbAdmin',
            dbStock: 'dbStock',
            dbIndex: 'dbIndex'
        }, ns=True )
