#!/usr/bin/python3
import jupiter.utils
import jupiter.network
import dev_global
import jupiter.database_manager
import numpy as np
import pandas as pd
import datetime


def unit_test_utils():
    print("test read_json")
    print(dev_global.env.CONF_FILE)
    print(utils.read_json('URL', dev_global.env.CONF_FILE))
    print("test read_url")
    print(utils.read_url('Sina', dev_global.env.CONF_FILE))
    print("test record_base")
    print(dev_global.env.LOG_FILE)
    utils.INFO('test')
    utils.ERROR('test')
    utils.WARN('test')
    print("Not tested: class Resource.")
    print("Not tested: str2number.")


def unit_test_network():
    network.delay(4)
    print('Network test finished.')


def unit_test_database_manager():
    bk = database_manager.databaseBackup()
    bk.get_database_list()
    # bk.backup()
    # bk.compress()
    bk.remove_old_backup()


def unit_test_fun_trans():
    s1 = pd.Series([1, -2, 3.5, -0.78, np.nan])
    s2 = pd.Series(['2020-01-22', np.nan, datetime.date(2020, 1, 29)])
    s2 = pd.to_datetime(s2)
    df = pd.concat([s1, s2], axis=1)
    # print(df)
    for index, row in df.iterrows():
        print(row[0], utils.trans(row[0]))
        print(row[1], utils.trans(row[1]))


def unit_test_task_module_reload():
    from dev_global.env import TASK_FILE, GLOBAL_HEADER
    from polaris.mysql8 import mysqlBase
    from apscheduler.executors.pool import ThreadPoolExecutor
    from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
    from sqlalchemy.ext.declarative import declarative_base

    Base = declarative_base()
    mysql = mysqlBase(GLOBAL_HEADER)
    jobstores = {
        'default': SQLAlchemyJobStore(
            engine=mysql.engine, metadata=Base.metadata)
            }
    executor = {'default': ThreadPoolExecutor(20)}
    default_job = {'max_instance': 5}
    tf = '/home/friederich/Documents/dev/applications/neutrino/config/task.json'
    Neptune = taskManager(
        taskfile=tf, jobstores=jobstores,
        executors=executor, job_defaults=default_job)
    Neptune.start()
    Neptune.reload_event()


def test_fun():
    print(time_var)


time_var = datetime.datetime.now()


if __name__ == '__main__':
    # unit_test_network()
    # unit_test_utils()
    # unit_test_database_manager()
    unit_test_fun_trans()
