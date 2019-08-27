#!/usr/bin/python3
"""
Geschafen im Aug 31, 2017

Verfasst von Friederich Fluss

Lib of mysql contains methods to drive mysql db using python.
v1.0.0-stable: Library is released.
v1.0.1-stable: Encrypted password is supported, relative codes are in
libencrypt.
v1.0.2-stable: Add new function TABLEEXIST.
v2.0.3-dev: Complete funcions of mysql.
v2.0.4-dev: Modify some bug, using encrypt pw.
v2.0.5-dev: Fix bug. drop table -> drop table if exists.
v3.0.6-alpha: change personal engine into commercial engine sqlalchemy.
"""

__version__ = '3.0.6-alpha'

# encode = 'wAKO0tFJ8ZH38RW4WseZnQ=='

from sqlalchemy.engine.url import URL as engine_url
from sqlalchemy import create_engine


class MySQLBase(object):
    def __init__(self, acc, pw, database, host='localhost', port=3306):
        DB_STRING = engine_url('mysql+pymysql',
                               username=acc,
                               password=pw,
                               host=host,
                               port=port,
                               database=database)
        self.engine = create_engine(DB_STRING,echo=True)

    def create_table(self, form):
        form.metadata.create_all(self.engine)
    def batch_create_table(self, form):
        t = form
        print(getattr(t,'__tablename__'))
        setattr(t,'__tablename__', 'test_table')
        print(getattr(t,'__tablename__'))
        form.metadata.create_all(self.engine,tables=[t])

if __name__ == '__main__':
    test = MySQLBase('root', '6414939', 'test')
    print(test.engine)
