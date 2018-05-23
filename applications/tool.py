#!/usr/bin/python3

from libmysql8 import *

def create_table_stock_index():
    ms = MySQLServer('stock',\
            libencrypt.mydecrypt('wAKO0tFJ8ZH38RW4WseZnQ=='),\
            'finance')
    table_definition="idx smallint unsigned primary key auto_increment,\
            gmt_create DATE,\
            gmt_modified DATE,\
            stock_code char(12) not null,\
            stock_name char(12)"
    print(ms.CREATETABLE('stock_index',table_definition))

def create_database_stock_data():
    ms = MySQLServer('stock',\
            libencrypt.mydecrypt('wAKO0tFJ8ZH38RW4WseZnQ=='),\
            'finance')
    ms._cs.execute('create database stock_data')
    ms._db.commit()

if  __name__ == '__main__':
    ms = MySQLServer('stock',libencrypt.mydecrypt('wAKO0tFJ8ZH38RW4WseZnQ=='),'finance')
    print(ms.VERSION())
    '''
    close,high,low,open,close,amplitude,turnover volumn,turnover value
    '''
    create_table_stock_index()
    #create_database_stock_data()
