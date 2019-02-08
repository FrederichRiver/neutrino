#!/bin/usr/python3
'''

Created on Dec 15, 2018

@ Author: Friedrich River
@ Project: Proxima Centauri

v1.0: First released.
Task plan resolver.
'''
import re

def task_file_reader(filename):
    '''
    Resolving the task file line by line.
    '''
    tasks = []
    if filename is not None:
        with open(filename) as f:
            line = f.readline()
            while line:
                result = line.split(',')
                task_typing(result)
                line = f.readline()
        return tasks
    else:
        return None
def task_typing(result):
    '''
    Return a scheduled event by its parameters
    '''
    if result[1] == 'date':
        pass
    elif result[1] == 'interval':
        pass
    elif result[1] == 'cron':
        print(task_resolve(result))
    else:
        pass

def task_resolve(result):
    cron_result = cron_time()
    for para in result:
        ti = para.split('=')
        if ti[0] == 'hour':
            cron_result.set_hour(ti[1])
    return cron_result.plan()
class cron_time(object):
    def __init__(self):
        self.year = 0
        self.month = 0
        self.day = 0
        self.week = ''
        self.dayofweek = ''
        self.hour = 0
        self.minute = 0
        self.second = 0
    def set_hour(self,h):
        self.hour = h
    def set_day(self,d):
        self.day = d
    def set_week(self,w):
        self.week = w
    def plan(self):
        taskplan = []
        if self.hour:
            taskplan.append('hour=%s' % self.hour)
        return taskplan
if  __name__ == '__main__':
    task_file_reader('/tmp/tp')
