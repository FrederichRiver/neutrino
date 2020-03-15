debug 1
Log content:
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
2020-02-22 23:50:00 [INFO]: Running job "event_download_stock_data (trigger: cron[hour='23', minute='50'], next run at: 2020-02-22 23:50:00 CST)" (scheduled at 2020-02-22 23:50:00+08:00)
SH600016
/usr/local/lib/python3.6/dist-packages/pymysql/cursors.py:170: Warning: (1264, "Out of range value for column 'volume' at row 1")
  result = self._query(query)
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
Reason:
SH600016 显示字长不够，手动修改问题日的交易量，跳过该条数据即可解决。程序中未发现原因。
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
Solution：
手动insert该行数据，跳过程序检验。尚未发现解决办法。