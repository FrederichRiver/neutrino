#!/usr/bin/python3
'''
Geschafen im Aug 31, 2017

Verfasst von Friederich Fluss

Lib of mysql contains methods to drive mysql db using python.
v1.0.0-stable: Library is released.
v1.0.1-stable: Encrypted password is supported, relative codes are in
libencrypt.
v1.0.2-stable: Add new function TABLEEXIST.
v2.0.3-dev: Complete funcions of mysql.
pre-v2.0.4-stable: Rebuild using metaclass methord.
'''

"""
X2.exit
4.grant db to user
X7.drop database
X9.use database
X10.select now
15.delete from table where
17.multi table update
*18.alter table add index
20.alter table add unique index
25.rename table
26.database backup
"""
import pymysql
from libbase import info, warning, err

__version__ = '2.0.3-dev'

class MySQLBase(object):
    def __init__(self, acc, pw, database, host='localhost', charset='utf8'):
        self.db = pymysql.connect(host=host,
                                user=acc,
                                passwd=pw,
                                db=database,
                                charset='utf8')
        self.cs = self.db.cursor()
        self.version = self._version()

    def _version(self):
        self.cs.execute('select Version()')
        self.db.commit()
        return self.cs.fetchone()[0]

    def createDatabase(self, dbName):
        sql = 'create database {0}'.format(dbName)
        try:
            self.cs.execute(sql)
            self.db.commit()
            return 1
        except Exception as e:
            info('MySQL database creation failure: %s' % e)
            return 0
    
    def dropDatabase(self, dbName):
        sql = 'drop database if exists {0}'.format(dbName)
        try:
            self.cs.execute(sql)
            self.db.commit()
            return 1
        except Exception as e:
            info('MySQL database delete failure: %s' % e)
            return 0

    def createTable(self, tabName, content):
        sql = 'create table if not exists {0} {1}'.format(tabName, content)
        try:
            self.cs.execute(sql)
            self.db.commit()
            return 1
        except Exception as e:
            info('MySQL table creation failure: %s' % e)
            return 0

    def updateTable(self, tabName, content, condition):
        sql = 'update {0} set {1} where {2}'.format(tabName, content, condition)
        try:
            self.cs.execute(sql)
            self.db.commit()
            return 1
        except Exception as e:
            info('MySQL table updating failure: %s' % e)
            return 0

    def insertAllValues(self, tabName, content):
        sql = 'insert into {0} values( {1} )'.format(tabName, content)
        try:
            self.cs.execute(sql)
            self.db.commit()
            return 1
        except Exception as e:
            info('MySQL inserting failure: %s' % e)
            return 0

    def insertValue(self, tabName, field, content):
        sql = 'insert into {0} ({1}) values( {2} )'.format(tabName, field, content)
        try:
            self.cs.execute(sql)
            self.db.commit()
            return 1
        except Exception as e:
            info('MySQL inserting failure: %s' % e)
            return 0

    def selectValues(self, tab, col, *args):
        try:
            if args != ():
                self.cs.execute("""select %s from %s where %s""" % (col, tab, args[0]))
            else:
                self.cs.execute("""select %s from %s""" % (col, tab))
            return self.cs.fetchall()
        except Exception as e:
            info('MySQL selecting failure: %s' % e)
            return None

    def selectOne(self, tabName, field, condition):
        sql = 'select {0} from {1} where {2}'.format(field, tabName, condition)
        try:
            self.cs.execute(sql)
            return self.cs.fetchone()
        except Exception as e:
            info('MySQL selecting failure: %s' % e)
            return None

    def addColumn(self, tab, col, col_type, *args):
        try:
            if args:
                self.cs.execute("""alter table %s add %s %s default %s""" \
                                 % (tab, col, col_type, args[0]))
            else:
                self.cs.execute("""alter table %s add %s %s""" \
                                 % (tab, col, col_type))
            return 1
        except Exception as e:
            info('MySQL adding column failure: %s' % e)
            return 0

    def addIndex(self, tab):
        sql = 'alter {0} '
        try:
            return 1
        except Exception as e:
            return 0

    def dropIndex(self, tab_name, idx_name):
        sql = 'alter {0} drop index {1}'.format(tab_name, idx_namei)
        try:
            self.cs.execute(sql)
            self.db.commit()
            return 1
        except Exception as e:
            info('MySQL drop index failure: %s' % e)
            return 0
    
    def addPrimaryKey(self, tab_name, idx_name):
        sql = 'alter table {0} add primary key {1}'.format(tab_name, idx_namei)
        try:
            self.cs.execute(sql)
            self.db.commit()
            return 1
        except Exception as e:
            info('MySQL add primary key failure: %s' % e)
            return 0

    def changeColumn(self, tabName, old_name, new_name, new_type):
        sql = 'alter table {0} change {1} {2} {3}'.format(tabName, old_name, new_name, new_type)
        try:
            self.cs.execute(sql)
            return 1
        except Exception as e:
            info('MySQL change column failure: %s' % e)
            return 0
    
    def dropColumn(self, tabName, fieldName):
        sql = 'alter table {0} drop {1}'.format(tabName, fieldName)
        try:
            self.cs.execute(sql)
            return 1
        except Exception as e:
            info('MySQL drop column failure: %s' % e)
            return 0

    def removeData(self, table_name, condition):
        sql = 'delete from {0} Where {1}'.format(table_name, condition)
        try:
            self.cs.execute(sql)
            self.db.commit()
            return 1
        except Exception as e:
            info('MySQL delete failure: %s' % e)
            return 0

    def showDatabases(self):
        try:
            self.cs.execute("show databases")
            self.db.commit()
            return self.cs.fetchall()
        except Exception as e:
            info('MySQL database showing failure: %s' % e)
            return 0
    
    def showTables(self):
        try:
            self.cs.execute("show tables")
            self.db.commit()
            return self.cs.fetchall()
        except Exception as e:
            info('MySQL table showing failure: %s' % e)
            return 0

    def tableExists(self, table_name):
        try:
            sql = "select table_name from information_schema.TABLES \
                    where table_name='{0}'"
            self.cs.execute(sql.format(table_name))
            self.db.commit()
            return self.cs.fetchone()
        except Exception as e:
            info('MySQL table checking failure: %s' % e)
            return 0

    def dropTable(self, table_name):
        try:
            sql = "drop table {0}".format(table_name)
            self.cs.execute(sql)
            self.db.commit()
        except Exception as e:
            info('MySQL table dropping failure: %s' % e)
            return 0

if __name__ == '__main__':
    pass
