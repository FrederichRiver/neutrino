debug 3
Log content:
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
2020-02-29 19:00:00 [INFO]: Running job "event_update_shibor (trigger: cron[hour='19', minute='0'], next run at: 2020-02-29 19:00:00 CST)" (scheduled at 2020-02-29 19:00:00+08:00)
2020-02-29 19:00:00 [ERROR]: Job "event_update_shibor (trigger: cron[hour='19', minute='0'], next run at: 2020-03-01 19:00:00 CST)" raised an exception
Traceback (most recent call last):
  File "/usr/local/lib/python3.6/dist-packages/venus/shibor.py", line 31, in get_shibor_data
    df['release_date'], format=TIME_FMT)
NameError: name 'TIME_FMT' is not defined

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/local/lib/python3.6/dist-packages/apscheduler/executors/base.py", line 125, in run_job
    retval = job.func(*job.args, **job.kwargs)
  File "/usr/local/lib/python3.6/dist-packages/venus/stock_event.py", line 174, in event_update_shibor
    event.get_shibor_data(df)
  File "/usr/local/lib/python3.6/dist-packages/venus/shibor.py", line 47, in get_shibor_data
    ERROR(e)
NameError: name 'ERROR' is not defined
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
Reason:
ERROR和TIME_FMT未正确引用。
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
Solution：
已经fix。