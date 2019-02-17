#!/usr/bin/python3
from libmysql8_dev import MySQLServer
import libencrypt

ms = MySQLBase('stock', libencrypt.mydecrypt('wAKO0tFJ8ZH38RW4WseZnQ=='),
    'stock_index') 
print("select version")
print(ms.version)
print("create table")
print(ms.createTable('test_table','test_index char(8) not null,test_name char(8)'))
print("update table")
print(ms.updateTable('test_table','test_name="shanghai"','test_index="SH600001"'))
print("insert all value")
print(ms.insertAllValues('test_table','test_index="SH600002",test_name="ZGSY"'))
print("insert value")
print(ms.insertValue('test_table','test_index,test_name','"SH600003","GZMT"'))
print("select values")
print(ms.selectValues('test_table','test_name'))
print("select values with conditions")
print(ms.selectValues('test_table', 'test_name', 'test_name is not NULL'))
print("select one value")
print(ms.selectOne('test_table', 'test_name', 'test_name is not NULL'))
print("add column")
print(ms.addColumn('test_table', 'test_col', 'char(4)'))
print("delete table")

print(ms.dropTable('test_table'))
print("show tables")
print(ms.showTables())
print("checking table existance")
print(ms.tableExists('stock_index')[0])
