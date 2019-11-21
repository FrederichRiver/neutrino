#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import re
import sys
import time
from message import *
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from event import (event_record_stock, event_init_stock,
                   event_download_stock_data,
                   event_create_interest_table,
                   event_record_interest,
                   event_flag_stock,
                   event_rehabilitation)
from dev import event_cooperation_info, event_finance_info

__version__ = '1.0.3'


class taskManager(BackgroundScheduler):
    def __init__(self, taskfile=None, gconfig={}, **options):
        super(BackgroundScheduler, self).__init__(
            gconfig=gconfig, **options)
        if not taskfile:
            sys.stdout.write(
                f"{time.ctime()}: Task file is not found.")
        else:
            self.func_list = {
                'event_record_stock': event_record_stock,
                'event_init_stock': event_init_stock,
                'event_download_stock_data': event_download_stock_data,
                'event_create_interest_table': event_create_interest_table,
                'event_record_interest': event_record_interest,
                'event_flag_stock': event_flag_stock,
                'event_rehabilitation': event_rehabilitation,
                'event_cooperation_info': event_cooperation_info,
                'event_finance_info': event_finance_info
            }
            self.taskfile = taskfile

    def task_resolve(self, jsdata):
        """
        Resolve the task file into job and trigger.
        File format is json.
        Return: {job: trigger}
        """
        tasklist = {}
        for task in jsdata:
            # job_resolve
            try:
                job = self.func_list[self.job_resolve(task)]
            except KeyError:
                print(
                    f"{time.ctime()}: "
                    f"Job {self.job_resolve(task)} could not be found.")
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
            elif k == 'time':
                m = re.match(r'(\d{1,2}):(\d{2})', jsdata['time'])
                trigger = CronTrigger(hour=int(m.group(1)), minute=int(m.group(2)))
            else:
                trigger = None
        return trigger

    def check_task_file(self):
        # if task file not exist, send a warning.
        if os.path.exists(self.taskfile):
            print(DM_CHECK_TASK.format(time.ctime()))
            self.append_task()
        else:
            print(
                DM_MISS_TASK.format(
                    time.ctime(),
                    self.taskfile)
            )

    def append_task(self):
        # if exist, resolve the task file.
        try:
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
                    print(f'add job {k.__name__}\n')
                jobexist = False
            self.task_report()
        except Exception as e:
            print("Append task error: ", e, '\n')

    def task_report(self):
        print('+-'*15)
        self.print_jobs()
        print('+-'*15)


class task(object):
    def __init__(self, func, trigger):
        self.func = func
        self.trigger = trigger


if __name__ == "__main__":
    x = '5:30'
    m = re.match(r'(\d{1,2}):(\d{2})', x)
    print(m.group(1))
    # task.add_job(test, 'interval', seconds=10, id='my_job')
