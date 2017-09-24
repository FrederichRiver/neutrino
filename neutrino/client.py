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
from dataEngine.finance_report import fetch_finance_report
from dataEngine.finance_dividend import fetch_finance_dividend
from analysis.stock import rehabilitation
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
        """menu data"""
        self.menuItemFetchNews.Enable(False)
        self.menuItemFetchFond.Enable(False)
        #self.menuItemFinanceData.Enable(False)
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
        self.Bind(wx.EVT_BUTTON,self.Event_test,self.buttonTest)
        self.Bind(wx.EVT_MENU,self.Event_fetchFinanceData,id=self.menuItemFinanceData.GetId())
        self.Bind(wx.EVT_MENU,self.Event_fetchFinanceDividend,id=self.menuItemDividend.GetId())
        """Event definition"""
    def Event_fetchIndex(self,event):
        """ when start button should be disabled incase of error operation"""
        self.menuItemFetchIndex.Enable(False)
        """ start a new thread so that ui can be updated in time."""
        task=threading.Thread(target=self.Task_check_list,args=(('stocks',)),name='fetch_indexs')
        task.start()
    def Event_fetchStock(self,event):
        print "fetch stock"
        """ when start button should be disabled incase of error operation"""
        self.menuItemFetchStock.Enable(False)
        """ start a new thread so that ui can be updated in time."""
        task=threading.Thread(target=self.Task_fetch_stocks,args=(),name='fetch_stocks')
        task.start()
    def Event_setSTflag(self,event):
        self.menuItemST.Enable(False)
        task=threading.Thread(target=self.Task_set_st_flag)
        task.start()
    def Event_fetchFinanceData(self,event):
        self.menuItemFinanceData.Enable(False)
        task=threading.Thread(target=self.Task_fetch_finance_report)
        task.start()
    def Event_fetchFinanceDividend(self,event):
        self.menuItemDividend.Enable(False)
        task=threading.Thread(target=self.Task_fetch_finance_dividend)
        task.start()
    def Task_check_list(self,flag):
        cfg=readAccount()
        db_index=mysql('localhost',cfg[0],cfg[1],'indexs')
        db_rec=mysql('localhost',cfg[0],cfg[1],'stock_data')
        """generate a list which contains all stocks and indexs"""
        indexlist=generate_list(flag)
        """query from database to get a list"""
        dblist=queryindex(db_index,dateStr(),flag)
        for i in range(len(dblist)):
            for j in range(len(indexlist)):
                if indexlist[j]==dblist[i]:
                    indexlist[j]='0' 
        for index in indexlist:
            if index!='0':
                searchindex(index,flag, db_index, db_rec, dateStr())
        print 'Finished fetching indexs.'
        """set menu enable after task."""
        self.menuItemFetchIndex.Enable(True)
    def Task_fetch_stocks(self):
        cfg=readAccount()
        """ create db connection"""
        db_index=mysql('localhost',cfg[0],cfg[1],'indexs')
        db_rec=mysql('localhost',cfg[0],cfg[1],'stock_data')
        """ fetch stock indexs."""
        stocks=db_index.selectValues( 'stocks', 'stock_index')
        for stock in stocks: 
            fetch_stock(db_index, db_rec, 'stocks', stock[0], dateStr())
        """ fetch indexs."""
        indexs=db_index.selectValues( 'indexs', 'stock_index')
        for index in indexs: 
            fetch_stock(db_index, db_rec, 'indexs', index[0], dateStr())
        self.menuItemFetchStock.Enable(True)
    def Task_set_st_flag(self):
        cfg=readAccount()
        db=mysql('localhost',cfg[0],cfg[1],'indexs')
        stocks=db.selectValues('stocks','stock_name')
        for stock in stocks:
            if 'ST' in stock[0]:
                print stock[0]
                db.updateTable('stocks',"flag='S'","stock_name='%s'" % stock[0])
        self.menuItemST.Enable(True)
    def Task_fetch_finance_report(self):
        cfg=readAccount()
        db_index=mysql('localhost',cfg[0],cfg[1],'indexs')
        db_rec=mysql('localhost',cfg[0],cfg[1],'finance_report')
        """ fetch stock indexs."""
        stocks=db_index.selectValues( 'stocks', 'stock_index')
        for stock in stocks: 
            print stock[0]
            fetch_finance_report(db_index, db_rec,stock[0])
        print 'finish'
        self.menuItemFinanceData.Enable(True)
    def Task_fetch_finance_dividend(self):
        cfg=readAccount()
        db_index=mysql('localhost',cfg[0],cfg[1],'indexs')
        db_rec=mysql('localhost',cfg[0],cfg[1],'finance_dividend')
        stocks=db_index.selectValues( 'stocks', 'stock_index')
        for stock in stocks: 
            print stock[0]
            fetch_finance_dividend(db_rec,stock[0])    
        print 'finish'
        self.menuItemDividend.Enable(True)
    def Event_test(self,event):
        self.buttonTest.Enable(False)
        rehabilitation()
        ## test scripts
        #cfg=readAccount()
        #db_index=mysql('localhost',cfg[0],cfg[1],'indexs')
        #db_data=mysql('localhost',cfg[0],cfg[1],'stock_data')
        #stocklist=db_index.selectValues('stocks','stock_index','update_time>0')
        #print stocklist
        #for i in range(len(stocklist)):
        #    dateresult=db_data.selectValues(stocklist[i][0],'date')
            #print dateresult
        #    for j in range(len(dateresult)):
         #       print dateresult[j][0]
                #dateStr2(dateresult[j][0])
                #db_data.updateTable(stocklist[i][0],'data_str=%s'% dateStr2(int(dateresult[j][0])),'date=%s'%dateresult[j][0])
        ## end scripts
        self.buttonTest.Enable(True)
if __name__ == '__main__':
    app=wx.App()
    win=mainFrame(None,'Neutrino')
    win.Show()
    app.MainLoop()