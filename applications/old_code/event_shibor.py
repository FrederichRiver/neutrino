#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import chardet
import requests
import sys
sys.path.append('..')
from libbase import *
from mysql.libmysql8_dev import MySQLBase
from libstock_dev import StockEventBase
url = 'http://www.shibor.org/shibor/web/html/downLoad.html?nameNew=Historical_Shibor_Data_{0}.xls&downLoadPath=data&nameOld=1{0}.xls&shiborSrc=http://www.shibor.org/shibor/'


class EventRecordShibor(StockEventBase):
    def __init__(self):
        super(EventRecordShibor, self).__init__()
        self.shibor = MySQLBase('root', '6414939', 'bank')

    def run(self):
        year_list = range(2006, 2019)
        for year in year_list:
            url_new = url.format(year)
            req = requests.get(url_new)
            result = pd.read_excel(url_new)
            #print(result.iloc[1,0].strftime('%Y-%m-%d'))
            self.record_shibor(result)

    def record_shibor(self, df):
        for i in range(0, df.shape[0])[::-1]:
            dt = df.iloc[i, 0].strftime('%Y-%m-%d')
            if self.shibor.select_values('shibor',
                '*', "release_date='%s'" % dt) == ():
                try:
                    columns = 'release_date, overnight,\
                    1W,2W,1M,3M,6M,9M,1Y'
                    content = "'{0}','{1}','{2}','{3}','{4}',\
                    '{5}','{6}','{7}','{8}'"
                    content = content.format(
                            dt, df.iloc[i, 1],
                            df.iloc[i, 2], df.iloc[i, 3],
                            df.iloc[i, 4], df.iloc[i, 5],
                            df.iloc[i, 6], df.iloc[i, 7],
                            df.iloc[i, 8])
                    self.shibor.insert_value('shibor',
                            columns, content)
                except Exception as e:
                    err('Inserting err when fetching shibor: %s' % e)
            else:
                try:
                    columns = 'overnight,1W,2W,1M,3M,6M,9M,1Y'
                    content = "'{0}','{1}','{2}','{3}','{4}',\
                            '{5}','{6}','{7}'"
                    content = content.format(df.iloc[i, 1],
                            df.iloc[i, 2], df.iloc[i, 3],
                            df.iloc[i, 4], df.iloc[i, 5],
                            df.iloc[i, 6], df.iloc[i, 7],
                            df.iloc[i, 8])
                except Exception as e:
                    err('Updateing err when fetching shibor: %s'% e)

if __name__ == '__main__':
    shibor = EventRecordShibor()
    shibor.run()
