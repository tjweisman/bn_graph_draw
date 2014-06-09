#!/usr/bin/python

import wx
from drawgraph import *

class Frame(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, title=title)
        self.Center()

        self.main_panel = wx.Panel(self)
        info_panel = wx.Panel(self.main_panel)
        info_sizer = wx.BoxSizer(wx.VERTICAL)
        info_panel.SetSizer(info_sizer)

        button_panel = wx.Panel(info_panel)
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_panel.SetSizer(button_sizer)

        self.tikz = wx.Button(button_panel, -1, "Export TikZ")
        self.clear = wx.Button(button_panel, -1, "Clear graph")
        button_sizer.Add(self.tikz, 0)
        button_sizer.Add(self.clear, 0)
        
        self.laplacian = wx.TextCtrl(info_panel)
        self.jacobian = wx.TextCtrl(info_panel)
        self.pair_guess = wx.TextCtrl(info_panel)
        info_sizer.Add(button_panel, 0, wx.EXPAND)
        info_sizer.Add(self.laplacian, 1, wx.EXPAND)
        info_sizer.Add(self.jacobian, 1, wx.EXPAND)
        info_sizer.Add(self.pair_guess, 1, wx.EXPAND)


        self.laplacian.SetEditable(False)
        self.jacobian.SetEditable(False)
        self.pair_guess.SetEditable(False)

        self.view = DrawPanel(self.main_panel, 
                              self.update_info)
        
        self.tikz.Bind(wx.EVT_BUTTON, self.export_tikz)
        self.clear.Bind(wx.EVT_BUTTON, self.clear_event)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(info_panel, 0, wx.EXPAND)
        main_sizer.Add(self.view, 1, wx.EXPAND)
        self.main_panel.SetSizer(main_sizer)
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
    
    def clear_event(self, event):
        self.view.clear()

app = wx.App()

frame=Frame('Graphmake')
frame.Show()

app.MainLoop()
