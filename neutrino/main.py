#coding=utf8
'''
Created on Apr 23, 2017

@author: frederich
'''
import wx
import threading
from ui.mainFrameBase import mainFrameBase
from utility.config import readAccount,dateStr
from db.mysql import mysql
from dataEngine.index import generate_list,queryindex,searchindex
from dataEngine.stock import fetch_stock
class mainFrame(mainFrameBase):
    def __init__(self,parent,title):
        """generate a frame from frameBase"""
        mainFrameBase.__init__(self, parent)
        self.SetTitle(title)
        self.Position=(0,0)
        """menu diable"""
        """menu config"""
        self.menuItemConfig.Enable(False)
        self.menuItemSpider.Enable(False)
        self.menuItemTimer.Enable(False)
        self.menuItemDb.Enable(False)
        self.menuItemDividend.Enable(False)
        """menu data"""
        self.menuItemFetchNews.Enable(False)
        self.menuItemFetchFond.Enable(False)
        self.menuItemFinanceData.Enable(False)
        """menu analysis"""
        self.menuItemNuetralNetworks.Enable(False)
        self.menuItemSVM.Enable(False)
        self.menuItemStatic.Enable(False)
        self.menuItemRehabilitation.Enable(False)
        self.menuItemHMM.Enable(False)
        """menu view"""
        self.menuItemDatabase.Enable(False)
        self.menuItemKPlot.Enable(False)
        """menu help"""
        self.menuItemHelp.Enable(False)
        self.menuItemAbout.Enable(False)
        self.menuItemLicense.Enable(False)
        """Event binding"""
        self.Bind(wx.EVT_MENU, self.Event_fetchIndex, id=self.menuItemFetchIndex.GetId())
        self.Bind(wx.EVT_MENU,self.Event_fetchStock,id=self.menuItemFetchStock.GetId())
        self.Bind(wx.EVT_MENU,self.Event_setSTflag,id=self.menuItemST.GetId())
        """Event definition"""
    def Event_fetchIndex(self,event):
        """ when start button should be disabled incase of error operation"""
        self.menuItemFetchIndex.Enable(False)
        """ start a new thread so that ui can be updated in time."""
        task=threading.Thread(target=self.check_list,args=(('indexs',)),name='fetch_indexs')
        task.start()
    def Event_fetchStock(self,event):
        print "fetch stock"
        """ when start button should be disabled incase of error operation"""
        self.menuItemFetchStock.Enable(False)
        """ start a new thread so that ui can be updated in time."""
        task=threading.Thread(target=self.fetch_stocks,args=(),name='fetch_stocks')
        task.start()
    def Event_setSTflag(self,event):
        self.menuItemST.Enable(False)
        task=threading.Thread(target=self.setSTFlag)
        task.start()

    def check_list(self,flag):
        cfg=readAccount()
        db1=mysql('localhost',cfg[0],cfg[1],'indexs')
        db2=mysql('localhost',cfg[0],cfg[1],'stock_data')
        """generate a list which contains all stocks and indexs"""
        indexlist=generate_list(flag)
        """query from database to get a list"""
        dblist=queryindex(db1,dateStr(),flag)
        for i in range(len(dblist)):
            for j in range(len(indexlist)):
                if indexlist[j]==dblist[i]:
                    indexlist[j]='0' 
        for index in indexlist:
            if index!='0':
                searchindex(index,flag, db1, db2, dateStr())
        """set menu enable after task."""
        self.menuItemFetchIndex.Enable(True)
    def fetch_stocks(self):
        cfg=readAccount()
        """ create db connection"""
        db1=mysql('localhost',cfg[0],cfg[1],'indexs')
        db2=mysql('localhost',cfg[0],cfg[1],'stock_data')
        """ fetch stock indexs."""
        stocks=db1.selectValues( 'stocks', 'stock_index')
        for stock in stocks: 
            fetch_stock(db1, db2, 'stocks', stock[0], dateStr())
        """ fetch indexs."""
        indexs=db1.selectValues( 'indexs', 'stock_index')
        for index in indexs: 
            fetch_stock(db1, db2, 'indexs', index[0], dateStr())
    def setSTFlag(self):
        cfg=readAccount()
        db=mysql('localhost',cfg[0],cfg[1],'indexs')
        stocks=db.selectValues('stocks','stock_name')
        for stock in stocks:
            if 'ST' in stock[0]:
                print stock[0]
                db.updateTable('stocks',"flag='S'","stock_name='%s'" % stock[0])
if __name__ == '__main__':
    app=wx.App()
    win=mainFrame(None,'Neutrino')
    win.Show()
    app.MainLoop()