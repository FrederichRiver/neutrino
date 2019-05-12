#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.combining import AndTrigger, OrTrigger


def task_resolve(jsdata):
    tasklist = {}
    for task in jsdata:
        # job_resolve
        job = job_resolve(task)
        # trigger_resolve
        trigger = trigger_resolve(task)
        if job and trigger:
            tasklist[job] = trigger
    print(tasklist)
    return job, trigger


def job_resolve(jsdata):
    jn = jsdata['task'] if 'task' in jsdata.keys() else None
    return jn


def trigger_resolve(jsdata):
    for k in jsdata.keys():
        if k == 'day of week':
            trigger = CronTrigger(day_of_week=jsdata['day of week'])
        elif k == 'hour':
            trigger = CronTrigger(hour=jsdata['hour'])
        else:
            trigger = None
    return trigger


with open('./task.json', 'r') as js:
    load_dist = json.load(js)
    print(load_dist, type(load_dist))
    task_resolve(load_dist)
