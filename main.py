#!/usr/bin/python

import wx
from drawgraph import *

class Frame(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, title=title)
        self.Center()

        self.mainPanel = wx.Panel(self)
        infoPanel = wx.Panel(self.mainPanel)
        infoSizer = wx.BoxSizer(wx.VERTICAL)
        infoPanel.SetSizer(infoSizer)

        self.tikz = wx.Button(infoPanel, -1, "export TikZ")
        self.laplacian = wx.TextCtrl(infoPanel)
        self.jacobian = wx.TextCtrl(infoPanel)
        self.pair_guess = wx.TextCtrl(infoPanel)
        infoSizer.Add(self.tikz, 0)
        infoSizer.Add(self.laplacian, 1, wx.EXPAND)
        infoSizer.Add(self.jacobian, 1, wx.EXPAND)
        infoSizer.Add(self.pair_guess, 1, wx.EXPAND)


        self.laplacian.SetEditable(False)
        self.jacobian.SetEditable(False)
        self.pair_guess.SetEditable(False)

        self.view = DrawPanel(self.mainPanel, 
                              self.update_info)
        
        self.tikz.Bind(wx.EVT_BUTTON, self.export_tikz)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(infoPanel, 0, wx.EXPAND)
        mainSizer.Add(self.view, 1, wx.EXPAND)
        self.mainPanel.SetSizer(mainSizer)
    def export_tikz(self, evt):
        dialog = wx.FileDialog(self, style = wx.FD_SAVE)
        dialog.ShowModal()
        path = dialog.GetPath()
        if path != "":
            print path
            tf = open(path, "w")
            tf.write(get_tikz_code(self.view.graph))
            tf.close()

    def update_info(self, Q, Jac, pair):
        self.laplacian.SetValue(repr(Q))
        self.jacobian.SetValue(repr(Jac))
        self.pair_guess.SetValue(repr(pair))

app = wx.App()

frame=Frame('Graphmake')
frame.Show()

app.MainLoop()
