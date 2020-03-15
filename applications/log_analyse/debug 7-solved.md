debug 6
Log content:
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
2020-03-15 11:01:42 [ERROR]: isinstance() arg 2 must be a type or tuple of types
/usr/local/lib/python3.6/dist-packages/pymysql/cursors.py:170: Warning: (1062, "Duplicate entry 'https://money.163.com/20/0222/13/F60A4HGJ002580S6.html' for key 'url'")
  result = self._query(query)
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
Reason:
isinstance(html, lxml.etree._Element)，输入为'lxml.etree._Element'
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
Solution：
已经解决。