debug 2
Log content:
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
2020-02-28 22:00:25 [ERROR]: Job "event_download_stock_data (trigger: cron[hour='22', minute='0'], next run at: 2020-02-29 22:00:00 CST)" raised an exception
Traceback (most recent call last):
  File "/usr/local/lib/python3.6/dist-packages/apscheduler/executors/base.py", line 125, in run_job
    retval = job.func(*job.args, **job.kwargs)
  File "/usr/local/lib/python3.6/dist-packages/venus/stock_event.py", line 27, in event_download_stock_data
    event.download_stock_data(stock_code)
  File "/usr/local/lib/python3.6/dist-packages/venus/stock_manager.py", line 142, in download_stock_data
    stock_code, self.today, start_date=update)
  File "/usr/local/lib/python3.6/dist-packages/venus/stock_manager.py", line 29, in get_trade_data
    result = pd.read_csv(url, encoding='gb18030')
  File "/usr/local/lib/python3.6/dist-packages/pandas/io/parsers.py", line 685, in parser_f
    return _read(filepath_or_buffer, kwds)
  File "/usr/local/lib/python3.6/dist-packages/pandas/io/parsers.py", line 440, in _read
    filepath_or_buffer, encoding, compression
  File "/usr/local/lib/python3.6/dist-packages/pandas/io/common.py", line 196, in get_filepath_or_buffer
    req = urlopen(filepath_or_buffer)
  File "/usr/lib/python3.6/urllib/request.py", line 223, in urlopen
    return opener.open(url, data, timeout)
  File "/usr/lib/python3.6/urllib/request.py", line 532, in open
    response = meth(req, response)
  File "/usr/lib/python3.6/urllib/request.py", line 642, in http_response
    'http', request, response, code, msg, hdrs)
  File "/usr/lib/python3.6/urllib/request.py", line 570, in error
    return self._call_chain(*args)
  File "/usr/lib/python3.6/urllib/request.py", line 504, in _call_chain
    result = func(*args)
  File "/usr/lib/python3.6/urllib/request.py", line 650, in http_error_default
    raise HTTPError(req.full_url, code, msg, hdrs, fp)
urllib.error.HTTPError: HTTP Error 500: Internal Server Error
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
Reason:
HTTP 500 – 内部服务器错误
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
Solution：
