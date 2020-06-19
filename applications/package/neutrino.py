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
from dev_global.env import LOG_FILE, PID_FILE, TASK_FILE, MANUAL, GLOBAL_HEADER
from polaris.mysql8 import mysqlHeader, mysqlBase
from jupiter.task_manager import taskManager, taskManager2
from jupiter.utils import ERROR, INFO
from sqlalchemy.ext.declarative import declarative_base
from threading import Thread

__version__ = '1.6.14'


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
    try:
        with open(log_file, 'a') as write_null:
            # Redirect to 1 which means stdout
            os.dup2(write_null.fileno(), 1)
        with open(log_file, 'a') as error_null:
            # Redirect to 2 which means stderr
            os.dup2(error_null.fileno(), 2)
    except Exception:
        ERROR("Error occurs while redirecting.")

    try:
        if pid_file:
            with open(pid_file, 'w+') as f:
                f.write(str(os.getpid()))
            atexit.register(os.remove, pid_file)
    except Exception:
        ERROR("Error occurs while openning PID file.")

    def sigterm_handler(signo, frame):
        raise SystemExit(1)
    signal.signal(signal.SIGTERM, sigterm_handler)


def logfile_monitor(log_file):
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
            INFO("Log file is missing. Recreate it.")
            INFO(f"Neutrino started with pid {os.getpid()}.")


def main_function(taskfile=None, task_line_name=''):
    # judge whether the task file exists.
    mysql = mysqlBase(GLOBAL_HEADER)
    jobstores = {
        'default': SQLAlchemyJobStore(tablename='apscheduler_jobs', engine=mysql.engine)
            }
    executor = {'default': ThreadPoolExecutor(20)}
    default_job = {'max_instance': 5}
    Neptune = taskManager(taskfile=taskfile,
                          jobstores=jobstores,
                          executors=executor,
                          job_defaults=default_job)
    Neptune.start()
    INFO(f"{task_line_name} start.")
    while True:
        # INFO("Checking task file.")
        try:
            Neptune.reload_event()
            Neptune.check_task_file()
        except Exception:
            ERROR("ERROR while checking task file.")
        time.sleep(300)
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
        print("neutrino start|stop|help")
        raise SystemExit(1)
    if sys.argv[1] == 'start':
        neutrino(PID_FILE, LOG_FILE)
        INFO(f"Neutrino id is {os.getpid()}.")
        try:
            # Here we start a thread which monitoring the log
            # file. If log file is missing, it will create one.
            lm = Thread(target=logfile_monitor,
                        args=(LOG_FILE,),
                        name='lm',
                        daemon=True)
            lm.start()
            # ending of working code.
        except Exception as e:
            ERROR("Error occurs while starting log monitor.")
            raise SystemExit(1)
        try:
            main_function(TASK_FILE, 'Neptune')
        except Exception as e:
            ERROR("Error occurs while running task pipe line.")
            print(e)
            raise SystemExit(1)
    elif sys.argv[1] == 'stop':
        if os.path.exists(PID_FILE):
            sys.stdout.flush()
            with open(LOG_FILE, 'a') as write_null:
                os.dup2(write_null.fileno(), 1)
                INFO("Neutrino is stopped.")
            with open(PID_FILE) as f:
                os.kill(int(f.read()), signal.SIGTERM)
        else:
            ERROR("Neutrino is not running.")
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
