#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.combining import AndTrigger, OrTrigger


class taskResolver(object):
    def __init__(self, func_list):
        self.func_list = func_list

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
        return tasklist

    def job_resolve(self, jsdata):
        """
        Filter of task file which can filt the incorrect
        config content.
        """
        jn = jsdata['task'] if 'task' in jsdata.keys() else None
        return jn

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

class task(object):
    def __init__(self, func, trigger):
        self.func = func
        self.trigger = trigger

def event_download_stock_data():
    pass


def analysis():
    pass


def test():
    print('test')


def test1():
    print('test1')


if __name__ == "__main__":
    function_list = {'test': test, 'test1': test1, 'analysis': analysis}
    tasksolver = taskResolver(function_list)
    result = None
    with open('config/task.json', 'r') as js:
        load_dist = json.load(js)
        result = tasksolver.task_resolve(load_dist)
        # print(result)
    tm = BackgroundScheduler()
    for j, t in result.items():
        tm.add_job(j, t)
    tm.print_jobs()
    tm.start
