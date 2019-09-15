#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libstock import StockEventBase
from neutrino import main_function

def test_class_resource():
    from utils import Resource
    res = Resource()
    res._query_info()
    print(res.status())
    print(res.system_report())

def test_libtask():
    from libtask import taskManager, test, test1
    from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
    from libmysql8 import mysqlHeader, mysqlBase
    from apscheduler.executors.pool import ThreadPoolExecutor
    from sqlalchemy.ext.declarative import declarative_base
    
    Base = declarative_base()
    header = mysqlHeader('root', '6414939', 'test')
    mysql = mysqlBase(header)
    jobstores = {'default': SQLAlchemyJobStore(
        engine=mysql.engine,
        metadata=Base.metadata)}
    executor = {'default': ThreadPoolExecutor(20)}
    task = taskManager(taskfile='config/task.json',
                       jobstores=jobstores,
                       executors=executor)
    task.start()
    task.check_task_file()

def test_codeformat():
    from libstock import codeFormat
    code = codeFormat()
    print(code('sh601818'))
    print(code('002230.sz'))
    code.net_ease_code('002230.sz')

if __name__ == "__main__":
    # dataline testing
    """
    input_string = ['2008-07-01', '2007',
                    '0', '0', '1.50',
                    '2008-07-04', '2008-07-07', '--']
    dt = dataline()
    result = dt.resolve(input_string, 'SH600001_interest')
    print(result)
    """
    # event create interest tables
    # event_create_interest_table()
    # event record interest
    # event_record_interest()
    # test_class_resource()
    # test_libtask()
    test_codeformat()
    main_function(None)
