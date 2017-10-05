'''
Created on Oct 3, 2017

@author: frederich
'''
import wx
from ui.mainFrameBase import mainFrameBase
from dataEngine.index import generate_list, query_index, query_stock,\
    search_index
from libmysql import MySQLServer
from utility.config import strDate, dateStr
from dataEngine.stock import fetch_stock
from globalVar import INDEX_DB, STOCK_DATA_DB


class mainFrame(mainFrameBase):
    def __init__(self, parent):
        mainFrameBase.__init__(self, parent)
        self.initUI()
        self.bindEvent()

    def initUI(self):
        self.Title = 'Neutrino'
        self.SetPosition((0, 0))

    def bindEvent(self):
        self.Bind(wx.EVT_BUTTON, self.Test)

    def Test(self, e):
        pass
    
    def update_data(self):
        querydb = MySQLServer(acc='stock',
                              pw='stock2017',
                              database=INDEX_DB)
        recdb = MySQLServer(acc='root',
                            pw='6414939',
                            database=STOCK_DATA_DB)
        stock_list = query_stock(querydb)
        for stock in stock_list:
            fetch_stock(querydb, recdb, 'stocks', stock, dateStr())
    
    def generate_index(self):
        stock_list = self.pre_stock_list()
        querydb=MySQLServer(acc='stock',
                            pw='stock2017',
                            database=INDEX_DB)
        createdb = MySQLServer(acc='root',
                               pw='6414939',
                               database=STOCK_DATA_DB)        
        for stock in stock_list:
            search_index(stock,'stocks',querydb,createdb,strDate)
    
    def pre_stock_list(self):   
        gen_list = generate_list('stocks')
        querydb = MySQLServer(acc='stock',
                              pw='stock2017',
                              database=INDEX_DB)
        old_list = query_stock(querydb)
        new_list = []
        for index in gen_list:
            if index not in old_list:
                new_list.append(index)
        print 'gen_list:', len(gen_list)
        print 'old_list:', len(old_list)
        print 'new_list:', len(new_list)
        return new_list
        
    def pre_index_list(self, e):   
        gen_list = generate_list('indexs')
        querydb = MySQLServer(acc='stock',
                              pw='stock2017',
                              database=INDEX_DB)
        old_list = query_index(querydb)
        new_list = []
        for index in gen_list:
            if index not in old_list:
                new_list.append(index)
    
if __name__ == '__main__':
    app = wx.App()
    window = mainFrame(None)
    window.Show(True)
    app.MainLoop()
    