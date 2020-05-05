#!/usr/bin/python3
import os
from polaris.mysql8 import mysqlHeader

"""
global environment varibles

"""

PYTHON_VERSION = 3.6
LOCAL_TIME_ZONE = 'Beijing'
TIME_FMT = '%Y-%m-%d'


if os.getenv('SERVER') == 'MARS':
    ROOT_PATH = '/root/'
    SOFT_PATH = '/opt/neutrino/'
else:
    ROOT_PATH = '~/Documents/dev/neutrino/applications/'
    SOFT_PATH = '/opt/neutrino/'


encode = 'wAKO0tFJ8ZH38RW4WseZnQ=='

LOG_FILE = SOFT_PATH + 'neutrino.log'
PID_FILE = '/tmp/neutrino.pid'
TASK_FILE = SOFT_PATH + 'config/task.json'
CONF_FILE = SOFT_PATH + 'config/conf.json'
HEAD_FILE = SOFT_PATH + 'config/header.json'
COOKIE_FILE = SOFT_PATH + 'config/cookie.json'
SQL_FILE = SOFT_PATH + 'config/sql.json'
MANUAL = SOFT_PATH + 'config/Neutrino'


GLOBAL_HEADER = mysqlHeader('stock', 'stock2020', 'stock')
VIEWER_HEADER = mysqlHeader('view', 'view2020', 'stock')
