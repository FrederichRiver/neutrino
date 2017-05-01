# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Feb 16 2016)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class mainFrameBase
###########################################################################

class mainFrameBase ( wx.Frame ):
    
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.Point( 0,0 ), size = wx.Size( 300,45 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        self.menubarMain = wx.MenuBar( 0 )
        self.menuData = wx.Menu()
        self.menuItemFetchStock = wx.MenuItem( self.menuData, wx.ID_ANY, u"Fetch Stock", wx.EmptyString, wx.ITEM_NORMAL )
        self.menuData.AppendItem( self.menuItemFetchStock )
        
        self.menuItemFetchIndex = wx.MenuItem( self.menuData, wx.ID_ANY, u"Fetch Index", wx.EmptyString, wx.ITEM_NORMAL )
        self.menuData.AppendItem( self.menuItemFetchIndex )
        
        self.menuItemFetchFond = wx.MenuItem( self.menuData, wx.ID_ANY, u"Fetch Fond", wx.EmptyString, wx.ITEM_NORMAL )
        self.menuData.AppendItem( self.menuItemFetchFond )
        
        self.menuData.AppendSeparator()
        
        self.menuItemFetchNews = wx.MenuItem( self.menuData, wx.ID_ANY, u"Fetch News", wx.EmptyString, wx.ITEM_NORMAL )
        self.menuData.AppendItem( self.menuItemFetchNews )
        
        self.menuItemFinanceData = wx.MenuItem( self.menuData, wx.ID_ANY, u"Fetch Finance Data", wx.EmptyString, wx.ITEM_NORMAL )
        self.menuData.AppendItem( self.menuItemFinanceData )
        
        self.menuItemDividend = wx.MenuItem( self.menuData, wx.ID_ANY, u"Fetch Dividend", wx.EmptyString, wx.ITEM_NORMAL )
        self.menuData.AppendItem( self.menuItemDividend )
        
        self.menubarMain.Append( self.menuData, u"Data" ) 
        
        self.menuAnalysis = wx.Menu()
        self.menuItemRehabilitation = wx.MenuItem( self.menuAnalysis, wx.ID_ANY, u"Rehabilitation", wx.EmptyString, wx.ITEM_NORMAL )
        self.menuAnalysis.AppendItem( self.menuItemRehabilitation )
        
        self.menuNLP = wx.Menu()
        self.menuItemStatic = wx.MenuItem( self.menuNLP, wx.ID_ANY, u"Words Static", wx.EmptyString, wx.ITEM_NORMAL )
        self.menuNLP.AppendItem( self.menuItemStatic )
        
        self.menuAnalysis.AppendSubMenu( self.menuNLP, u"NLP" )
        
        self.menuML = wx.Menu()
        self.menuItemNuetralNetworks = wx.MenuItem( self.menuML, wx.ID_ANY, u"NeutralNetworks", wx.EmptyString, wx.ITEM_NORMAL )
        self.menuML.AppendItem( self.menuItemNuetralNetworks )
        
        self.menuItemHMM = wx.MenuItem( self.menuML, wx.ID_ANY, u"HidenMarkov", wx.EmptyString, wx.ITEM_NORMAL )
        self.menuML.AppendItem( self.menuItemHMM )
        
        self.menuItemSVM = wx.MenuItem( self.menuML, wx.ID_ANY, u"SVM", wx.EmptyString, wx.ITEM_NORMAL )
        self.menuML.AppendItem( self.menuItemSVM )
        
        self.menuAnalysis.AppendSubMenu( self.menuML, u"Machine Learning" )
        
        self.menuDataEdit = wx.Menu()
        self.menuItemST = wx.MenuItem( self.menuDataEdit, wx.ID_ANY, u"ST flag", wx.EmptyString, wx.ITEM_NORMAL )
        self.menuDataEdit.AppendItem( self.menuItemST )
        
        self.menuAnalysis.AppendSubMenu( self.menuDataEdit, u"Data Edit" )
        
        self.menubarMain.Append( self.menuAnalysis, u"Analysis" ) 
        
        self.menuView = wx.Menu()
        self.menuItemDatabase = wx.MenuItem( self.menuView, wx.ID_ANY, u"Database", wx.EmptyString, wx.ITEM_NORMAL )
        self.menuView.AppendItem( self.menuItemDatabase )
        
        self.menuPlot = wx.Menu()
        self.menuItemKPlot = wx.MenuItem( self.menuPlot, wx.ID_ANY, u"K Plot", wx.EmptyString, wx.ITEM_NORMAL )
        self.menuPlot.AppendItem( self.menuItemKPlot )
        
        self.menuView.AppendSubMenu( self.menuPlot, u"Plot" )
        
        self.menubarMain.Append( self.menuView, u"View" ) 
        
        self.menuSetting = wx.Menu()
        self.menuItemConfig = wx.MenuItem( self.menuSetting, wx.ID_ANY, u"Config", wx.EmptyString, wx.ITEM_NORMAL )
        self.menuSetting.AppendItem( self.menuItemConfig )
        
        self.menuItemDb = wx.MenuItem( self.menuSetting, wx.ID_ANY, u"Database", wx.EmptyString, wx.ITEM_NORMAL )
        self.menuSetting.AppendItem( self.menuItemDb )
        
        self.menuItemSpider = wx.MenuItem( self.menuSetting, wx.ID_ANY, u"Spider", wx.EmptyString, wx.ITEM_NORMAL )
        self.menuSetting.AppendItem( self.menuItemSpider )
        
        self.menuItemTimer = wx.MenuItem( self.menuSetting, wx.ID_ANY, u"TaskSchedule", wx.EmptyString, wx.ITEM_NORMAL )
        self.menuSetting.AppendItem( self.menuItemTimer )
        
        self.menubarMain.Append( self.menuSetting, u"Setting" ) 
        
        self.menuHelp = wx.Menu()
        self.menuItemHelp = wx.MenuItem( self.menuHelp, wx.ID_ANY, u"Help", wx.EmptyString, wx.ITEM_NORMAL )
        self.menuHelp.AppendItem( self.menuItemHelp )
        
        self.menuItemAbout = wx.MenuItem( self.menuHelp, wx.ID_ANY, u"About", wx.EmptyString, wx.ITEM_NORMAL )
        self.menuHelp.AppendItem( self.menuItemAbout )
        
        self.menuItemLicense = wx.MenuItem( self.menuHelp, wx.ID_ANY, u"License", wx.EmptyString, wx.ITEM_NORMAL )
        self.menuHelp.AppendItem( self.menuItemLicense )
        
        self.menubarMain.Append( self.menuHelp, u"Help" ) 
        
        self.SetMenuBar( self.menubarMain )
        
        bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.searchCtrl = wx.SearchCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 170,-1 ), 0 )
        self.searchCtrl.ShowSearchButton( True )
        self.searchCtrl.ShowCancelButton( False )
        bSizer5.Add( self.searchCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
        
        self.buttonTest = wx.Button( self, wx.ID_ANY, u"Test", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer5.Add( self.buttonTest, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        
        self.SetSizer( bSizer5 )
        self.Layout()
        
        self.Centre( wx.BOTH )
    
    def __del__( self ):
        pass
    

