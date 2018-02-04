#!/usr/bin/python3

import os
import sys
import atexit
import signal
import tasksched

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
    with open(stdin, 'rb', 0) as read_null:
        os.dup2(read_null.fileno(), sys.stdin.fileno())
    with open(stdout, 'ab', 0) as write_null:
        os.dup2(write_null.fileno(), sys.stdout.fileno())
    with open(stderr, 'ab', 0) as error_null:
        os.dup2(error_null.fileno(), sys.stderr.fileno())
    if pid_file:
        with open(pid_file, 'w+') as f:
            f.write(str(os.getpid()))
        atexit.register(os.remove, pid_file)
    def sigterm_handler(signo, frame):
        raise SystemExit(1)
    signal.signal(signal.SIGTERM, sigterm_handler)
def main():
    import time
    sys.stdout.write('Daemon started with pid {}\n'.format(os.getpid()))
    while True:
        sys.stdout.write('Daemon Alive! {}\n'.format(time.ctime()))
        time.sleep(10)

if  __name__=='__main__':
    PIDFILE = '/tmp/daemon.pid'
    if len(sys.argv) != 2:
        print('Usage: {} [start|stop]'.format(sys.argv[0]), file=sys.stderr)
        raise SystemExit(1)
    if sys.argv[1] == 'start':
        try:
            daemonize(PIDFILE,
                    stdout='/tmp/daemon.log',
                    stderr='/tmp/daemon.log')
        except RuntimeError as e:
            print(e, file=sys.stderr)
            raise SystemExit(1)
        tasksched.scheduler()
    elif sys.argv[1] =='stop':
        if os.path.exists(PIDFILE):
            with open(PIDFILE) as f:
                os.kill(int(f.read()), signal.SIGTERM)
        else:
            print('Not running', file=sys.stderr)
            raise SystemExit(1)
    else:
        print('Unknown command {!r}'.format(sys.argv[1]), file=sys.stderr)
        raise SystemExit(1)
