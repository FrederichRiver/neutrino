#!/usr/bin/python3
import time
import sched
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

def genelist(flag='all'):
    stock_index = []
    if flag == 'all' or flag == 'stock' or flag =='a' or flag == 'sh':
        sha = ['SH600000']*4000
        for i in range(len(sha)):
            sha[i] = 'SH'+'60'+str(i).zfill(4)
        stock_index.extend(sha)
    print(stock_index[100])
    return stock_index
def scheduler():
    tasksched = BackgroundScheduler()
    tasksched.start()
    tasksched.add_job(genelist,'interval', seconds = 0.5)
    i = 0
    while i<5:
        time.sleep(3)
        i = i+1
        print(i)

if __name__ == '__main__':
    scheduler()
