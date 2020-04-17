#!/usr/bin/python3
'''
Created on Aug 31, 2017

@Author: Frederich River
@Project: Mercury

Lib of mysql contains methods to drive mysql db using python.
v1.0.0-stable: Library is released.
v1.0.1-stable: Encrypted password is supported, relative codes are in
libencrypt.
v1.0.2-stable: Add new function TABLEEXIST.
Pre v2.0.2-stable: Rebuild using metaclass methord.
'''
import pymysql
import libencrypt
from libbase import info, warning, err

__version__ = '1.0.1-stable'

class MySQLServer(object):
    def __init__(self, acc, pw, database, host='localhost', charset='utf8'):
        self._name = ''
        self._db = pymysql.connect(host=host,
                                user=acc,
                                passwd=pw,
                                db=database,
                                charset='utf8')
        self._cs = self._db.cursor()

    def VERSION(self):
        self._cs.execute('select Version()')
        self._db.commit()
        return self._cs.fetchone()[0]

    def CREATETABLE(self, tab, content):
        try:
            self._cs.execute("create table if not exists {0} ({1})".format(tab, content))
            self._db.commit()
            return 1
        except Exception as e:
            info('MySQL table creation failure: %s' % e)
            return 0

    def UPDATETABLE(self, tab, content, condition):
        try:
            self._cs.execute("update {table} set {value} where {condition}".format(table=tab,
                                                                                   value=content,
                                                                                   condition=condition))
            self._db.commit()
            return 1
        except Exception as e:
            info('MySQL table updating failure: %s' % e)
            return 0

    def INSERTALLVALUES(self, tab, content):
        try:
            self._cs.execute("""insert into %s values( %s )"""% (tab, content))
            self._db.commit()
            return 1
        except Exception as e:
            info('MySQL inserting failure: %s' % e)
            return 0

    def INSERTVALUE(self, tab, columns, content):
        try:
            self._cs.execute("""insert into %s (%s) values( %s )"""% (tab, columns, content))
            self._db.commit()
            return 1
        except Exception as e:
            info('MySQL inserting failure: %s' % e)
            return 0

    def SELECTVALUES(self, tab, col, *args):
        try:
            if args != ():
                self._cs.execute("""select %s from %s where %s""" % (col, tab, args[0]))
            else:
                self._cs.execute("""select %s from %s""" % (col, tab))
            return self._cs.fetchall()
        except Exception as e:
            info('MySQL selecting failure: %s' % e)
            return None

    def SELECTONE(self, tab, col, condition):
        try:
            self._cs.execute("""select %s from %s where %s""" % (col, tab, condition))
            return self._cs.fetchone()
        except Exception as e:
            info('MySQL selecting failure: %s' % e)
            return None

    def deleteTable(self,tab):
        try:
            self._cs.execute("""drop table %s""" % tab)
            return 1
        except Exception as e:
            info('MySQL deleting failure: %s' % e)
            return 0

    def addColumn(self, tab, col, col_type, *args):
        try:
            if args != ():
                self._cs.execute("""alter table %s add %s %s default %s""" \
                                 % (tab, col, col_type, args[0]))
            else:
                self._cs.execute("""alter table %s add %s %s""" \
                                 % (tab, col, col_type))
            return 1
        except Exception as e:
            info('MySQL adding column failure: %s' % e)
            return 0

    def showTables(self):
        try:
            self._cs.execute("show tables")
            self._db.commit()
            return self._cs.fetchall()
        except Exception as e:
            info('MySQL table showing failure: %s' % e)
            return 0
    def TABLEEXIST(self, table_name):
        try:
            sql = "select table_name from information_schema.TABLES \
                    where table_name='{0}'"
            self._cs.execute(sql.format(table_name))
            self._db.commit()
            return self._cs.fetchone()
        except Exception as e:
            info('MySQL table checking failure: %s' % e)
            return 0


if __name__ == "__main__":
    ms = MySQLServer('stock', libencrypt.mydecrypt('wAKO0tFJ8ZH38RW4WseZnQ=='), 'stock_index')
    print("select version")
    print(ms.VERSION())
    print("create table")
    print(ms.CREATETABLE('test_table','test_index char(8) not null,test_name char(8)'))
    print("update table")
    print(ms.UPDATETABLE('test_table','test_name="shanghai"','test_index="SH600001"'))
    print("insert all value")
    print(ms.INSERTALLVALUES('test_table','test_index="SH600002",test_name="ZGSY"'))
    print("insert value")
    print(ms.INSERTVALUE('test_table','test_index,test_name','"SH600003","GZMT"'))
    print("select values")
    print(ms.SELECTVALUES('test_table','test_name'))
    print("select values with conditions")
    print(ms.SELECTVALUES('test_table', 'test_name', 'test_name is not NULL'))
    print("select one value")
    print(ms.SELECTONE('test_table', 'test_name', 'test_name is not NULL'))
    print("add column")
    print(ms.addColumn('test_table', 'test_col', 'char(4)'))
    print("delete table")
    print(ms.deleteTable('test_table'))
    print("show tables")
    print(ms.showTables())
    print("checking table existance")
    print(ms.TABLEEXIST('stock_index')[0])
