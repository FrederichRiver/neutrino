#!/usr/bin/python
'''
Created on Aug 24, 2017
@author: frederich

RPCServer.py regist some api on a server (which might be real or virtual.)
The server provides RMI service to client.
'''
from dataEngine.index import generate_list, query_index, search_index
from dataEngine.stock import fetch_stock
from dataEngine.finance_report import fetch_finance_report
from dataEngine.finance_dividend import fetch_finance_dividend
from utility.config import dateStr, readAccount, int2Date
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SocketServer import ThreadingMixIn
from globalVar import RPC_PORT


class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass


if __name__ == '__main__':
    rpcserver = ThreadXMLRPCServer(('localhost', RPC_PORT), allow_none=True)
    rpcserver.register_introspection_functions()
    rpcserver.register_function(generate_list)
    rpcserver.register_function(query_index)
    rpcserver.register_function(search_index)
    rpcserver.register_function(dateStr)
    rpcserver.register_function(int2Date)
    rpcserver.register_function(fetch_stock)
    rpcserver.register_function(fetch_finance_report)
    rpcserver.register_function(fetch_finance_dividend)
    rpcserver.register_function(readAccount)
    rpcserver.serve_forever()
