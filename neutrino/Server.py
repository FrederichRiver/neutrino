'''
Created on Oct 3, 2017

@author: frederich
'''
import wx
from ui.mainFrameBase import mainFrameBase
from dataEngine.index import update_data
from utility.config import InfoLog


class mainFrame(mainFrameBase):
    def __init__(self, parent):
        mainFrameBase.__init__(self, parent)
        self.initUI()
        self.bindEvent()
        InfoLog('Neutrino Server Started.')

    def initUI(self):
        self.Title = 'Neutrino'
        self.SetPosition((0, 0))

    def bindEvent(self):
        self.Bind(wx.EVT_BUTTON, self.Test)

    def Test(self, e):
        pass
        update_data()
    def __del__(self):
        mainFrameBase.__del__(self)
        InfoLog('Neutrino Server Shutdown.')

if __name__ == '__main__':
    app = wx.App()
    window = mainFrame(None)
    window.Show(True)
    app.MainLoop()
    