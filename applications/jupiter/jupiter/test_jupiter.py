#!/usr/bin/python3
import utils
import network
import dev_global
import database_manager
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


if __name__ == '__main__':
    # unit_test_network()
    # unit_test_utils()
    # unit_test_database_manager()
    unit_test_fun_trans()
