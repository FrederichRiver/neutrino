debug 6
Log content:
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
Exception in thread SH603033:
Traceback (most recent call last):
  File "/usr/lib/python3.6/threading.py", line 916, in _bootstrap_inner
    self.run()
  File "/usr/lib/python3.6/threading.py", line 864, in run
    self._target(*self._args, **self._kwargs)
  File "/usr/local/lib/python3.6/dist-packages/venus/stock_interest.py", line 42, in insert_interest_table_into_sql
    tab = self.resolve_table(stock_code)
AttributeError: 'EventInterest' object has no attribute 'resolve_table'
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
Reason:
resolve_table函数改名后未及时更新。
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
Solution：
已经解决。