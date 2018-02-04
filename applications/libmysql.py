'''
Created on Aug 31, 2017

@author: frederich

Lib of mysql contains methods to drive mysql db using python.
'''
import MySQLdb
from utility.config import InfoLog

__version__ = '1.0.0-stable'

class MySQLServer(object):
    def __init__(self, acc, pw, database, host='localhost', charset='utf8'):
        self._name = ''
        try:
            self._db = MySQLdb.connect(host=host,
                                user=acc,
                                passwd=pw,
                                db=database,
                                charset='utf8')
            self._cs = self._db.cursor()
        except Exception as e:
            InfoLog('MySQL connection failure: %s' % e, level='ERROR')

    def selectVersion(self):
        self._cs.execute('select Version()')
        self._db.commit()
        return self._cs.fetchone()[0]

    def createTable(self, tab, content):
        try:
            self._cs.execute("create table if not exists {0} ({1})".format(tab, content))
            self._db.commit()
            return 1
        except Exception as e:
            InfoLog('MySQL table creation failure: %s' % e, level='ERROR')
            return 0

    def updateTable(self, tab, content, condition):
        try:
            self._cs.execute("update {table} set {value} where {condition}".format(table=tab,
                                                                                   value=content,
                                                                                   condition=condition))
            self._db.commit()
            return 1
        except Exception as e:
            InfoLog('MySQL table updating failure: %s' % e, level='ERROR')
            return 0

    def insertAllValues(self, tab, content):
        try:
            self._cs.execute("""insert into %s values( %s )"""% (tab, content))
            self._db.commit()
            return 1
        except Exception as e:
            InfoLog('MySQL inserting failure: %s' % e, level='ERROR')
            return 0

    def insertValues(self, tab, columns, content):
        try:
            self._cs.execute("""insert into %s (%s) values( %s )"""% (tab, columns, content))
            self._db.commit()
            return 1
        except Exception as e:
            InfoLog('MySQL inserting failure: %s' % e, level='ERROR')
            return 0

    def selectValues(self, tab, col, *args):
        try:
            if args != ():
                self._cs.execute("""select %s from %s where %s""" % (col, tab, args[0]))
            else:
                self._cs.execute("""select %s from %s""" % (col, tab))
            return self._cs.fetchall()
        except Exception as e:
            InfoLog('MySQL selecting failure: %s' % e, level='ERROR')
            return None

    def selectOne(self, tab, col, condition):
        try:
            self._cs.execute("""select %s from %s where %s""" % (col, tab, condition))
            return self._cs.fetchone()
        except Exception as e:
            InfoLog('MySQL selecting failure: %s' % e, level='ERROR')
            return None

    def deleteTable(self,tab):
        try:
            self._cs.execute("""drop table %s""" % tab)
            return 1
        except Exception as e:
            InfoLog('MySQL deleting failure: %s' % e, level='ERROR')
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
            InfoLog('MySQL adding column failure: %s' % e, level='ERROR')
            return 0

    def showTables(self):
        try:
            self._cs.execute("show tables")
            self._db.commit()
            return self._cs.fetchall()
        except Exception as e:
            InfoLog('MySQL table showing failure: %s' % e, level='ERROR')
            return 0
