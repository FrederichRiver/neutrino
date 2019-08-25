#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import sys
import time
from message import *
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.combining import AndTrigger, OrTrigger
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from libmysql8 import mysqlHeader, mysqlBase
from sqlalchemy.ext.declarative import declarative_base
from apscheduler.executors.pool import ThreadPoolExecutor


class taskManager(BackgroundScheduler):
    def __init__(self, taskfile=None, gconfig={}, **options):
        """TODO: Docstring for __init__.

        :taskfile: TODO
        :gconfig: TODO
        :**options: TODO
        :returns: TODO

        """
        super(BackgroundScheduler, self).__init__(
            gconfig=gconfig, **options)
        self.func_list = {'test': test, 'test1': test1}
        self.taskfile = taskfile
        if not self.taskfile:
            print('error')


    def task_resolve(self, jsdata):
        """
        Resolve the task file into job and trigger.
        File format is json.
        Return: {job: trigger}
        """
        tasklist = {}
        for task in jsdata:
            # job_resolve
            job = self.func_list[self.job_resolve(task)]
            # trigger_resolve
            trigger = self.trigger_resolve(task)
            if job and trigger:
                tasklist[job] = trigger
        # print(tasklist)
        # format:
        # { job_function<function> : job_trigger<trigger> }
        return tasklist

    def job_resolve(self, jsdata):
        """
        Filter of task file which can filt the incorrect
        config content.
        """
        jobname = jsdata['task'] if 'task' in jsdata.keys() else None
        return jobname

    def trigger_resolve(self, jsdata):
        """
        Resolve the trigger.
        """
        for k in jsdata.keys():
            if k == 'day of week':
                trigger = CronTrigger(day_of_week=jsdata['day of week'])
            elif k == 'hour':
                trigger = CronTrigger(hour=jsdata['hour'])
            else:
                trigger = None
        return trigger

    def check_task_file(self):
        # if task file not exist, send a warning.
        if os.path.exists(self.taskfile):
            sys.stdout.write(DM_CHECK_TASK.format(time.ctime()))
            self.append_task()
        else:
            sys.stdout.write(
                DM_MISS_TASK.format(
                    time.ctime(),
                    self.taskfile)
            )

    def append_task(self):
        # if exist, resolve the task file.
        with open(self.taskfile, 'r') as js:
            load_dict = json.load(js)
            result = self.task_resolve(load_dict)
        job_list = self.get_jobs()
        jobexist = False
        for (k, v) in result.items():
            for job in job_list:
                if k.__name__ == job.id:
                    self.reschedule_job(k.__name__, trigger=v)
                    jobexist = True
            if not jobexist:
                self.add_job(k, trigger=v, id=k.__name__)
            jobexist = False
        self.print_jobs()

class task(object):
    def __init__(self, func, trigger):
        self.func = func
        self.trigger = trigger


def test():
    print('test')


def test1():
    print('test1')


if __name__ == "__main__":
    import os
    Base = declarative_base()
    header = mysqlHeader('root', '6414939', 'test')
    mysql = mysqlBase(header)
    jobstores = {'default': SQLAlchemyJobStore(
        engine=mysql.engine,
        metadata=Base.metadata)}
    executor = {'default': ThreadPoolExecutor(20)}
    task = taskManager(taskfile='config/task.json',
                       jobstores=jobstores,
                       executors=executor)
    task.start()
    task.check_task_file()

    # task.add_job(test, 'interval', seconds=10, id='my_job')
