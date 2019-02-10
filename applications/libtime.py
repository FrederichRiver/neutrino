#!/usr/bin/python3

"""
Author : Friederich Fluss
Created: Feb 9, 2019

module time

"""
from datetime import datetime, timezone, timedelta
LOCAL_TIME_ZONE = 'Beijing'
"""
NewYork, London, Frankfort, USWest
"""

class TradeTimeBase(object):
    def __init__(self):
        self.CONFIG='HOLIDAY_CONFIG'
        self.holiday_list = set()
        self.time_zone = timezone(timedelta(hours=8))
        self.time_baseline = datetime.now(self.time_zone)
        self.timezone_FLAG = True 
        self.city = {'Beijing':8,'Bj':8}
    def city_timezone(self, city_name):
        if self.timezone_FLAG:
            return self._get_timezone(city_name)
        else:
            return self._get_timezone2(city_name)
    def _get_timezone(self, city_name):
        return timezone(timedelta(hours = self.city.get(city_name, 0)))
    def _get_timezone2(self, city_name):
        if city_name =='Beijing':
            return timezone(timedelta(hours = 8 ))
        elif city_name == 'Hawaii':
            return timezone(timedelta(hours = -10 ))
        elif city_name == 'Los Angles':
            return timezone(timedelta(hours = -8 ))
        elif city_name == 'Saltlake':
            return timezone(timedelta(hours = -7))
        elif city_name == 'Chicago':
            return timezone(timedelta(hours = -6))
        elif city_name == 'New York':
            return timezone(timedelta(hours = -5))
        elif city_name == 'London' or city_name == 'Paris':
            return timezone(timedelta(hours = 0))
        elif city_name == 'Frankfurt':
            return timezone(timedelta(hours = 1 ))
        else:
            return timezone(timedelta(hours = 0))

    def _load_config(self):
        with open(self.CONFIG,'r') as f:
            temp=f.readline()
            while temp:
                self.holiday_list.add(temp)
                temp = f.readline()
        print(self.holiday_list)
        '''
        load config file to generate a holiday list
        '''
    def _load_time_zone(self):
        '''
        if city_list exist:
            read city time list file
            self.timezoneFlag = True
        else:
            self.timezoneflag = False
        '''
        #read time zone info from a file and gene a set
    def _export_config(self):
        pass
def next_n_day(day_string, n=1):
    x = datetime.strptime(day_string, "%Y-%m-%d") + timedelta(days=n)
    return x.strftime("%Y-%m-%d")

def next_week_day(day_string):
    x = datetime.strptime(day_string, "%Y-%m-%d") + timedelta(days= 1)
    while x.weekday() > 4:
        x = x + timedelta(days = 1)
    return x.strftime("%Y-%m-%d")

if __name__ == '__main__':
    x = TradeTimeBase()
    #x._load_config()
    print(x.time_baseline)
    print(x.time_zone)
    print(x.city_timezone('Chicago'))
    print(x.city_timezone('London'))
    print(x.city_timezone('Beijing'))
    print(x.city_timezone('Bj'))

