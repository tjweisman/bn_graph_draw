#!/usr/bin/python

import wx
from sage.all import *
from drawgraph import DrawPanel

class Frame(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, title=title)
        self.Center()

        self.mainPanel = wx.Panel(self)
        infoPanel = wx.Panel(self.mainPanel)
        infoSizer = wx.BoxSizer(wx.VERTICAL)
        infoPanel.SetSizer(infoSizer)

        self.laplacian = wx.TextCtrl(infoPanel)
        self.jacobian = wx.TextCtrl(infoPanel)
        self.pair_guess = wx.TextCtrl(infoPanel)
        infoSizer.Add(self.laplacian, 1, wx.EXPAND)
        infoSizer.Add(self.jacobian, 1, wx.EXPAND)
        infoSizer.Add(self.pair_guess, 1, wx.EXPAND)

        self.laplacian.SetEditable(False)
        self.jacobian.SetEditable(False)
        self.pair_guess.SetEditable(False)

        self.view = DrawPanel(self.mainPanel, 
                              self.update_info)
        
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(infoPanel, 0, wx.EXPAND)
        mainSizer.Add(self.view, 1, wx.EXPAND)
        self.mainPanel.SetSizer(mainSizer)
    def update_info(self, Q, Jac, pair):        
        self.laplacian.SetValue(repr(Q))
        self.jacobian.SetValue(repr(Jac))
        self.pair_guess.SetValue(repr(pair))

app = wx.App()

frame=Frame('Graphmake')
frame.Show()

app.MainLoop()
