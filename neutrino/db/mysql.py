#!/usr/bin/python2
'''
Created on Apr 23, 2017

@author: frederich
'''
import MySQLdb
class mysql(object):
    def __init__(self,host,acc,pw,database):
        self._name=''
        try:
            x=MySQLdb.connect(host=host,user=acc,passwd=pw,db=database,charset='utf8')
            self._db=x
            self._cs=x.cursor()
        except MySQLdb.Error,e:
            print 'MySQL Error: %s' % str(e)
    def getName(self):
        return self._name
    def createTable(self,tab,content):
        try:
            self._cs.execute("""create table if not exists %s (%s)""" % (tab,content))
            self._db.commit()
            return 1
        except MySQLdb.Error, e:
            raise e
            return 0
    def updateTable(self,tab,content,condition):
        try:
            self._cs.execute("""update %s set %s where %s""" % (tab,content,condition))
            self._db.commit()
            return 1
        except MySQLdb.Error, e:
            raise e
            return 0
    def insertAllValues(self,tab,content):
        try:
            self._cs.execute("""insert into %s values( %s )"""% (tab,content))
            self._db.commit()
            return 1
        except MySQLdb.Error, e:
            raise e
            return 0
    def insertValues(self,tab,columns,content):
        try:
            self._cs.execute("""insert into %s (%s) values( %s )"""% (tab,columns,content))
            self._db.commit()
            return 1
        except MySQLdb.Error, e:
            raise e
            return 0
    def selectValues(self,tab,col,*args):
        try:
            if args!=():
                self._cs.execute("""select %s from %s where %s""" % (col,tab,args[0]))
            else:
                self._cs.execute("""select %s from %s""" % (col,tab))            
            return self._cs.fetchall()
        except MySQLdb.Error, e:
            raise e
            return None
    def selectOne(self,tab,col,condition):
        try:
            self._cs.execute("""select %s from %s where %s""" % (col,tab,condition))
            return self._cs.fetchone()
        except MySQLdb.Error, e:
            raise e
            return None
    def close(self):
        self._db.close()
        return 0