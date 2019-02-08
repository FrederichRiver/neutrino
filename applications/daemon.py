#!/usr/bin/python3
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
#import sched
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from threading import Thread

__version__ = '1.1.2'
LOG_FILE = '/tmp/daemon.log'

#daemon process, two times fork.

def daemonize(pid_file, stdin='/dev/null',
                        stdout='/dev/null',
                        stderr='/dev/null'):
    #fork a sub process from father
    if os.path.exists(pid_file):
        raise RuntimeError('Already running')
    try:
        if os.fork() > 0:
            raise SystemExit(0)
    except OSError as e:
        raise RuntimeError('fork #1 failed.')

    os.chdir('/')
    os.umask(0)
    os.setsid()
    #Second fork
    try:
        if os.fork() > 0:
            raise SystemExit(0)
    except OSError as e:
        raise RuntimeError('fork #2 failed.')
    # Flush I/O buffers
    sys.stdout.flush()
    sys.stderr.flush()
    redirect(stdin, stdout, stderr)
    if pid_file:
        with open(pid_file, 'w+') as f:
            f.write(str(os.getpid()))
        atexit.register(os.remove, pid_file)
    def sigterm_handler(signo, frame):
        raise SystemExit(1)
    signal.signal(signal.SIGTERM, sigterm_handler)

def redirect(in_file = LOG_FILE,
        out_file = LOG_FILE,
        err_file = LOG_FILE):
    with open(in_file, 'rb', 0) as read_null:
        os.dup2(read_null.fileno(), sys.stdin.fileno())
    with open(out_file, 'ab', 0) as write_null:
        os.dup2(write_null.fileno(), sys.stdout.fileno())
    with open(err_file, 'ab', 0) as error_null:
        os.dup2(error_null.fileno(), sys.stderr.fileno())

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

def logMonitor():
    while True:
        if os.path.exists(LOG_FILE):
            pass
        else:
            create_file = open(LOG_FILE,'a')
            create_file.close()
            redirect(LOG_FILE, LOG_FILE, LOG_FILE)
            sys.stdout.write('Daemon started with pid {}\n'.format(os.getpid()))
        time.sleep(5)

def main_function():
    sys.stdout.write('Daemon started with pid {}\n'.format(os.getpid()))

    tasksched = BackgroundScheduler()
    tasksched.start()
    tasksched.add_job(test,'interval',seconds=1.0)

    while True:
        sys.stdout.write('{} Daemon Alive!\n'.format(time.ctime()))
        time.sleep(10)

def readTaskPlan():
    if os.path.exists('/tmp/tp'):
        sys.stdout.write('{}\n'.format(time.ctime()))
    else:
        sys.stdout.write('{} Task plan file is not found.\n'.format(time.ctime()))

def test(x,y):
    sys.stdout.write('{}\n'.format(str(x)))

if  __name__=='__main__':
    PIDFILE = '/tmp/daemon.pid'
    if len(sys.argv) != 2:
        print('Usage: {} [start|stop]'.format(sys.argv[0]), file=sys.stderr)
        raise SystemExit(1)
    if sys.argv[1] == 'start':
        try:
            daemonize(PIDFILE, stdout= LOG_FILE, stderr= LOG_FILE)
            sys.stdout.write('Daemon started with pid {}\n'.format(os.getpid()))
        except RuntimeError as e:
            print(e, file=sys.stderr)
            raise SystemExit(1)
        # working code is added here.
        lm = Thread(target=logMonitor,args=(), name='lm', daemon=True)
        lm.start()
        while True:
            readTaskPlan()
            sys.stdout.write('{} Daemon is alive.\n'.format(time.ctime()))
            #run task sequence
            time.sleep(10)
        # ending of working code.

    elif sys.argv[1] =='stop':
        if os.path.exists(PIDFILE):
            sys.stdout.flush()
            with open(LOG_FILE, 'ab', 0) as write_null:
                os.dup2(write_null.fileno(), sys.stdout.fileno())
            sys.stdout.write('Daemon Shutdown {}\n'.format(time.ctime()))
            with open(PIDFILE) as f:
                os.kill(int(f.read()), signal.SIGTERM)
        else:
            print('Not running', file=sys.stderr)
            raise SystemExit(1)
    elif sys.argv[1] =='clear':
        os.system('rm %s' % LOG_FILE)
    else:
        print('Unknown command {!r}'.format(sys.argv[1]), file=sys.stderr)
        raise SystemExit(1)
