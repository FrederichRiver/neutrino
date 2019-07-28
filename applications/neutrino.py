#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Mar 31, 2018
@ Author: Frederich River
@ Project: Proxima Centauri
Daemon process of whole system.
v1.0.0-stable: First released.
v1.1.1-stable: Even log file is deleted, daemon can also run.
v1.1.2: Add task/ delete task function.
v1.1.3: Reading task plan file.
Log is recorded into file /tmp/daemon.log
v1.2.6: Some bugs are fixed.
'''
import os
import sys
import atexit
import signal
import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from threading import Thread
from task_manager import event_task_resolve
from message import DM_MSG, DM_ALIVE, DM_STOP, DM_NOT_RUN
from message import DM_CHECK_TASK, DM_MISS_TASK
from environment import LOG_FILE, PID_FILE, TASK_FILE, MANUAL
from message import DM_START
__version__ = '1.2.6'


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


def add_task(task_name, func, *arg):
    sys.stdout.write('Add task {}\n'.format(task_name))

    tasksched = BackgroundScheduler()
    tasksched.start()
    try:
        tasksched.add_job(func, 'interval', seconds=1.0, args=(arg))
    except Exception:
        sys.stderr.write('{} e'.format(time.ctime()))


def del_task(task_name):
    sys.stdout.write('Delete task {}\n'.format(task_name))


def logMonitor(log_file):
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

            sys.stdout.write(
                'Neutrino started with pid {}\n'.format(os.getpid()))


def main_function():
    sys.stdout.write('Neutrino started with pid {}\n'.format(os.getpid()))

    tasksched = BackgroundScheduler()
    tasksched.start()
    tasks = event_task_resolve()
    for task in tasks:
        tasksched.add_job(task[0], task[1])

    while True:
        sys.stdout.write(DM_ALIVE.format(time.ctime()))
        time.sleep(10)
    return 1


def check_task_plan(task_file):
    # Checking whether task file exists.
    # If not exists, record a warning.
    if os.path.exists(task_file):
        sys.stdout.write(DM_CHECK_TASK.format(time.ctime()))
    else:
        sys.stdout.write(
            DM_MISS_TASK.format(
                time.ctime(),
                task_file)
        )
    return 1


def test(x, y):
    sys.stdout.write('{}\n'.format(str(x)))


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
        except Exception:
            raise SystemExit(1)
        # working code is added here.
        lm = Thread(target=logMonitor, args=(
            LOG_FILE,), name='lm', daemon=True)
        lm.start()
        while True:
            check_task_plan(TASK_FILE)
            sys.stdout.write(DM_ALIVE.format(time.ctime()))
            sys.stdout.flush()
            # run task sequence
            time.sleep(10)
        # ending of working code.

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
    elif sys.argv[1] == 'clear':
        with open(LOG_FILE, 'w') as f:
            pass
    elif sys.argv[1] == 'help':
        helptext = ''
        with open(MANUAL) as r:
            helptext = r.read()
        print(helptext)
    elif sys.argv[1] == 'log':
        logtext = ''
        with open(LOG_FILE) as r:
            logtext = r.read()
        print(logtext)
    elif sys.argv[1] == 'version':
        print(__version__)
    else:
        print('Unknown command {!r}'.format(sys.argv[1]))
        raise SystemExit(1)
