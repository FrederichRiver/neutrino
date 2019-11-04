#!/usr/bin/env python
# -*- coding: utf-8 -*-
from event import event_download_stock_data
import datetime
from libstock import EventDownloadStockData
from libmysql8 import mysqlHeader, mysqlBase
# event_download_stock_data()

if __name__ == "__main__":
    header = mysqlHeader('root', '6414939', 'test')
    event = EventDownloadStockData()
    event._init_database(header)
    event._download_stock_data('SH600016')
