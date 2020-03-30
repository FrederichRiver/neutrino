#!/usr/bin/python3

from polaris.mysql8 import mysqlHeader

"""
global environment varibles

"""

PYTHON_VERSION = 3.6

ROOT_PATH = '~/Documents/dev/neutrino/applications/'
LOCAL_TIME_ZONE = 'Beijing'
encode = 'wAKO0tFJ8ZH38RW4WseZnQ=='

# SOFT_PATH = '/home/friederich/Documents/dev/neutrino/applications/'
SOFT_PATH = '/opt/neutrino/'
LOG_FILE = SOFT_PATH + 'neutrino.log'
PID_FILE = '/tmp/neutrino.pid'
TASK_FILE = SOFT_PATH + 'config/task.json'
CONF_FILE = SOFT_PATH + 'config/conf.json'
SQL_FILE = SOFT_PATH + 'config/sql.json'
MANUAL = SOFT_PATH + 'config/Neutrino'
TIME_FMT = '%Y-%m-%d'

GLOBAL_HEADER = mysqlHeader('stock', 'stock2020', 'stock')
VIEWER_HEADER = mysqlHeader('view', 'view2020', 'stock')
