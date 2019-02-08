#!/usr/bin/python3
"""
version: v0.0.1-dev
"""
import random
from libmysql8 import *

def rand(n):
    return random.randint(0,n)

class Person(object):
    def __init__(self, Name, current, START_DATE='1999-12-19'):
        self.current = 100000
        self.quant = 0
        self.freq = 3
    def _buy(self, quanti, preis):
        if preis:
            if (self.current - quanti*preis ) >=0:
                self.current = self.current - quanti*preis
                self.quant = self.quant + quanti
                return 1
            else:
                return 0
        else:
            return 0

    def _sell(self, quanti, preis):
        if self.quant >= quanti:
            self.current = self.current + quanti*preis
            self.quant = self.quant - quanti
            return 1
        else:
            return 0
    def _bankrupt(self):
        pass
    def _benefit(self, preis):
        bf = self.current + self.quant*preis - 100000
        return bf
    def report(self, preis):
        if preis > 0:
            print('Current:', self.current)
            print('Quanty:', self.quant)
            print('Benefit:', self._benefit(preis))
    def buy_or_not(code):
        
        pass

#class c1(object):
def buy_or_not():
    pass

def list():
    ms = MySQLServer('stock', 'stock2018','stock_data')
    result = ms.SELECTVALUES('SH600000','trade_date,close_price')
    d={}
    print(result[0][0],result[0][1])
    for data in result:
        d[data[0]]=data[1]
    return d

from datetime import datetime, timedelta

def next_n_day(day_string, n=1):
    x = datetime.strptime(day_string, "%Y-%m-%d") + timedelta(n)
    return x.strftime("%Y-%m-%d")

def next_week_day(day_string):
    x = datetime.strptime(day_string, "%Y-%m-%d") + timedelta(1)
    while x.weekday() > 4:
        x = x + timedelta(1)
    return x.strftime("%Y-%m-%d")

def stradge():
    pass

if __name__ == '__main__':
    d = list()
    fred = Person('Fred',100000)
    fred._buy(1000, 1.21)
    fred.report(1.22)
    fred._sell(500, 1.25)
    fred.report(1.28)
    start_day = '2018-01-07'
    the_day = start_day
    cot = 1
    while cot < 20:
        print(the_day, d.get(the_day, -1))
        the_day = next_week_day(the_day)
        cot = cot +1
    print("Trading")
    while cot < 25:
        the_day = next_n_day(the_day, rand(fred.freq))
        fred._buy(100, d.get(the_day, 0))
        fred.report(d.get(the_day,0))
        cot = cot + 1
