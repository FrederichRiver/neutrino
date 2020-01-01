#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Mar 31, 2018
@ Author: Frederich River
'''
import atexit
import os
import signal
import sys
import time
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from env import LOG_FILE, PID_FILE, TASK_FILE, MANUAL
from libmysql8 import mysqlHeader, mysqlBase
from libtask import taskManager
from message import (DM_MSG, DM_START, DM_ALIVE, DM_STOP,
                     DM_NOT_RUN)
from sqlalchemy.ext.declarative import declarative_base
from threading import Thread

__version__ = '1.4.8'


def neutrino(pid_file, log_file):
    # This is a daemon programe, which will start after
    # system booted.
    #
    # It is defined to start by rc.local.
    #
    # fork a sub process from father
    if os.path.exists(pid_file):
        raise RuntimeError('Neutrino is already running')
    try:
        if os.fork() > 0:
            raise SystemExit(0)
    except OSError:
        raise RuntimeError('Fork #1 failed.')

    os.chdir('/')
    os.umask(0)
    os.setsid()
    # Second fork
    try:
        if os.fork() > 0:
            raise SystemExit(0)
    except OSError:
        raise RuntimeError('Fork #2 failed.')
    # Flush I/O buffers
    sys.stdout.flush()
    sys.stderr.flush()

    # with open(log_file, 'rb', 0) as read_null:
    # os.dup2(read_null.fileno(), sys.stdin.fileno())
    with open(log_file, 'a') as write_null:
        # Redirect to 1 which means stdout
        os.dup2(write_null.fileno(), 1)
    with open(log_file, 'a') as error_null:
        # Redirect to 2 which means stderr
        os.dup2(error_null.fileno(), 2)

    if pid_file:
        with open(pid_file, 'w+') as f:
            f.write(str(os.getpid()))
        atexit.register(os.remove, pid_file)

    def sigterm_handler(signo, frame):
        raise SystemExit(1)
    signal.signal(signal.SIGTERM, sigterm_handler)


def _logMonitor(log_file):
    # A parallel programe which monitoring the log file.
    # If log file is not exists, it will create one and
    # relocalize the file.
    while True:
        if os.path.exists(log_file):
            time.sleep(10)
        else:
            create_file = open(log_file, 'a')
            create_file.close()
            with open(log_file, 'a') as write_null:
                os.dup2(write_null.fileno(), 1)
            with open(log_file, 'a') as error_null:
                os.dup2(error_null.fileno(), 2)
            print(
                f"{time.ctime()}: Log file is missing. Recreate it.\n"
                f"{time.ctime()}: Neutrino started with pid {os.getpid()}\n")


def main_function(taskfile=None):
    # judge whether the task file exists.
    print(
            f"{time.ctime()}: "
            f"Neutrino started with pid {os.getpid()}\n")
    Base = declarative_base()
    header = mysqlHeader('root', '6414939', 'test')
    mysql = mysqlBase(header)
    jobstores = {
        'default': SQLAlchemyJobStore(
            engine=mysql.engine, metadata=Base.metadata)
            }
    executor = {'default': ThreadPoolExecutor(20)}
    Neptune = taskManager(taskfile=taskfile,
                          jobstores=jobstores,
                          executors=executor)
    Neptune.start()
    print(f"{time.ctime()}: Neptune start.\n")
    while True:
        print(DM_ALIVE.format(time.ctime()))
        Neptune.check_task_file()
        time.sleep(1800)
    return 1


def print_info(info_file):
    infotext = ''
    with open(info_file) as r:
        infotext = r.read()
    print(infotext)


if __name__ == '__main__':
    # This is main function
    # Arguments format is like 'netrino args'
    # Neutrino receives args like start stop or other.
    if len(sys.argv) != 2:
        print(DM_MSG.format(sys.argv[0]))
        raise SystemExit(1)
    if sys.argv[1] == 'start':
        try:
            neutrino(PID_FILE, LOG_FILE)
            sys.stdout.write(DM_START.format(t=time.ctime(),
                                             pid=os.getpid()))
            sys.stdout.flush()
            # Here we start a thread which monitoring the log
            # file. If log file is missing, it will create one.
            lm = Thread(target=_logMonitor,
                        args=(LOG_FILE,),
                        name='lm',
                        daemon=True)
            lm.start()
            main_function(TASK_FILE)
            # ending of working code.
        except Exception:
            raise SystemExit(1)
    elif sys.argv[1] == 'stop':
        if os.path.exists(PID_FILE):
            sys.stdout.flush()
            with open(LOG_FILE, 'a') as write_null:
                os.dup2(write_null.fileno(), 1)
                write_null.write(DM_STOP.format(time.ctime()))
            with open(PID_FILE) as f:
                os.kill(int(f.read()), signal.SIGTERM)
        else:
            print(DM_NOT_RUN)
            raise SystemExit(1)
    elif sys.argv[1] == 'reboot':
        if os.path.exists(PID_FILE):
            sys.stdout.flush()
            with open(LOG_FILE, 'a') as write_null:
                os.dup2(write_null.fileno(), 1)
                write_null.write(DM_STOP.format(time.ctime()))
            with open(PID_FILE) as f:
                os.kill(int(f.read()), signal.SIGTERM)
        else:
            print(DM_NOT_RUN)
            # raise SystemExit(1)
        try:
            neutrino(PID_FILE, LOG_FILE)
            sys.stdout.write(DM_START.format(t=time.ctime(),
                                             pid=os.getpid()))
            sys.stdout.flush()
            # Here we start a thread which monitoring the log
            # file. If log file is missing, it will create one.
            lm = Thread(target=_logMonitor,
                        args=(LOG_FILE,),
                        name='lm',
                        daemon=True)
            lm.start()
            main_function(TASK_FILE)
            # ending of working code.
        except Exception:
            raise SystemExit(1)
    elif sys.argv[1] == 'clear':
        with open(LOG_FILE, 'w') as f:
            pass
    elif sys.argv[1] == 'help':
        print_info(MANUAL)
    elif sys.argv[1] == 'log':
        print_info(LOG_FILE)
    elif sys.argv[1] == 'version':
        print(__version__)
    else:
        print('Unknown command {!r}'.format(sys.argv[1]))
        raise SystemExit(1)
