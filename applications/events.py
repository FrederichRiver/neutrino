#!/bin/usr/python3
'''
Created by Friedrich River
Dec 15, 2018
@ Author Friedrich River
'''
import libstock

# event searching stock index

def search_new_stock():
    '''
    Checking for neu stock,
    if exist,
    create a table in stock_data,
    und create a index in finance.
    '''
    '''  Generate a total list of stocks.  '''
    stock_list = libstock.generate_stock_list()
    ''' Checking those stocks I have included in database. '''
    non_listed_stock = libstock.nonlisted(stock_list)
    #print(non_listed_stock[70:150])
    ''' For those non-included, create data table. '''
    libstock.createstock(non_listed_stock)

def func1():
    pass

# event investment statistic

if __name__ == '__main__':
    #search_new_stock()
    libstock.updatedata()
