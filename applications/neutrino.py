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
import message as msg

__version__ = '1.1.5'


def neutrino(pid_file, log_file):
    # fork a sub process from father
    if os.path.exists(pid_file):
        raise RuntimeError('Neutrino is already running')
    try:
        if os.fork() > 0:
            raise SystemExit(0)
    except OSError as e:
        raise RuntimeError('fork #1 failed.')

    os.chdir('/')
    os.umask(0)
    os.setsid()
    # Second fork
    try:
        if os.fork() > 0:
            raise SystemExit(0)
    except OSError as e:
        raise RuntimeError('fork #2 failed.')
    # Flush I/O buffers
    sys.stdout.flush()
    sys.stderr.flush()
    
    #with open(log_file, 'rb', 0) as read_null:
        #os.dup2(read_null.fileno(), sys.stdin.fileno())
    with open(log_file, 'ab', 0) as write_null:
        os.dup2(write_null.fileno(), sys.stdout.fileno())
    with open(log_file, 'ab', 0) as error_null:
        os.dup2(error_null.fileno(), sys.stderr.fileno())

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
    except Exception as e:
        sys.stderr.write('{} e'.format(time.ctime()))


def del_task(task_name):
    sys.stdout.write('Delete task {}\n'.format(task_name))


def logMonitor(log_file):
    while True:
        if os.path.exists(log_file):
            time.sleep(10)
        else:
            create_file = open(log_file, 'a')
            create_file.close()
            with open(log_file, 'ab', 0) as write_null:
                os.dup2(write_null.fileno(), sys.stdout.fileno())
            with open(log_file, 'ab', 0) as error_null:
                os.dup2(error_null.fileno(), sys.stderr.fileno())

            sys.stdout.write(
                'Neutrino started with pid {}\n'.format(os.getpid()))


def main_function():
    sys.stdout.write('Neutrino started with pid {}\n'.format(os.getpid()))

    tasksched = BackgroundScheduler()
    tasksched.start()
    tasksched.add_job(test, 'interval', seconds=1.0)

    while True:
        sys.stdout.write('{} Neutrino is alive!\n'.format(time.ctime()))
        time.sleep(10)


def readTaskPlan(task_file):
    task_file = 'home/frederich/Documents/dev/neutrino/applications/task.json'
    if os.path.exists(task_file):
        sys.stdout.write('{}\n'.format(time.ctime()))
    else:
        sys.stdout.write(
            '{0} Task plan file {1} is not found.\n'.format(
                time.ctime(),
                task_file)
            )



def test(x, y):
    sys.stdout.write('{}\n'.format(str(x)))


if __name__ == '__main__':
    LOG_FILE = '/tmp/neutrino.log'
    PID_FILE = '/tmp/neutrino.pid'
    TASK_FILE = 'task.json'
    if len(sys.argv) != 2:
        print(msg.DAEMON_MSG.format(sys.argv[0]))
        raise SystemExit(1)
    if sys.argv[1] == 'start':
        try:
            neutrino(PID_FILE, LOG_FILE)
            sys.stdout.write(msg.DAEMON_START.format(os.getpid()))
        except RuntimeError as e:
            raise SystemExit(1)
        # working code is added here.
        lm = Thread(target=logMonitor, args=(LOG_FILE,), name='lm', daemon=True)
        lm.start()
        while True:
            readTaskPlan(TASK_FILE)
            sys.stdout.write(msg.DAEMON_ALIVE.format(time.ctime()))
            # run task sequence
            time.sleep(1800)
        # ending of working code.

    elif sys.argv[1] == 'stop':
        if os.path.exists(PID_FILE):
            sys.stdout.flush()
            with open(LOG_FILE, 'ab', 0) as write_null:
                os.dup2(write_null.fileno(), sys.stdout.fileno())
            sys.stdout.write(msg.DAEMON_STOP.format(time.ctime()))
            with open(PID_FILE) as f:
                os.kill(int(f.read()), signal.SIGTERM)
        else:
            print(msg.DAEMON_NOT_RUN)
            raise SystemExit(1)
    elif sys.argv[1] == 'clear':
        os.system('rm %s' % LOG_FILE)
    elif sys.argv[1] == 'help':
        helptext = ''
        with open('config/neutrino', 'r') as r:
            helptext = r.read()
        print(helptext)
    elif sys.argv[1] == 'log':
        logtext = []
        with open(LOG_FILE, 'r') as r:
            line = r.readline()
            while line:
                logtext.append( r.readline())
                line = r.readline()
        print(logtext)
    elif sys.argv[1] == 'version':
        print(__version__)
    else:
        print('Unknown command {!r}'.format(sys.argv[1]))
        raise SystemExit(1)
