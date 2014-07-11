#!/usr/bin/python

import wx
from drawgraph import *
import gonality
from graph import *
import spanning_trees

sage_ok = True

try:
    import sage.all
except ImportError as e:
    sage_ok = False

class InfoBox(wx.Panel):
    def __init__(self, parent, title):
        wx.Panel.__init__(self, parent)
        
        self.label=wx.StaticText(self, label=title)
        self.display=wx.TextCtrl(self)
        self.display.SetEditable(False)
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.label, 0)
        sizer.Add(self.display, 1, wx.EXPAND)
        
        self.SetSizer(sizer)

#the main app window
class Frame(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, title=title, size=(600,600))        
        self.Center()

        self.main_panel = wx.Panel(self)

        #panel with buttons and text boxes
        self.info_panel = wx.Panel(self.main_panel)
        self.info_sizer = wx.FlexGridSizer(rows=0,cols=2)
        self.info_sizer.AddGrowableCol(1, proportion=5)
        self.info_panel.SetSizer(self.info_sizer)

        #buttons panel
        button_panel = wx.Panel(self.main_panel)
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_panel.SetSizer(button_sizer)

        self.tikz = wx.Button(button_panel, -1, "Export TikZ")
        self.clear = wx.Button(button_panel, -1, "Clear graph")
        self.cleardiv = wx.Button(button_panel, -1, "Clear divisor")
        self.compute_gon = wx.Button(button_panel, -1, "Compute gonality")
        self.tryburn = wx.Button(button_panel,-1,"Try burn")
        self.getjac = wx.Button(button_panel,-1,"Get Jacobian")

        self.drawBn = wx.Button(button_panel,-1,"Draw Bn")
        button_sizer.AddMany([(self.tikz, 0), 
                              (self.clear,0), 
                              (self.cleardiv,0),
                              (self.compute_gon, 0),
                              (self.tryburn,0),
                              (self.getjac,0),
                              (self.drawBn,0)])
        
        #text boxes
        self.laplacian = self.add_infobox("Laplacian:")
        self.genus = self.add_infobox("Genus:")
        self.gonality = self.add_infobox("Gonality:")
        self.connec = self.add_infobox("Connectedness:")
        self.div = self.add_infobox("Divisor:")
        self.subset = self.add_infobox("Fireable subset:")

        #the graph drawing panel
        self.view = DrawPanel(self.main_panel, 
                              self.update_info)
        
        self.tikz.Bind(wx.EVT_BUTTON, self.export_tikz)
        self.clear.Bind(wx.EVT_BUTTON, self.clear_event)
        self.compute_gon.Bind(wx.EVT_BUTTON, self.compute_gonality)
        self.cleardiv.Bind(wx.EVT_BUTTON, self.clear_divisor)
        self.tryburn.Bind(wx.EVT_BUTTON, self.try_burn)
        self.getjac.Bind(wx.EVT_BUTTON,self.get_jacob)
        self.drawBn.Bind(wx.EVT_BUTTON,self.draw_Bn)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(button_panel)
        main_sizer.Add(self.info_panel, 0, wx.EXPAND)
        main_sizer.Add(self.view, 1, wx.EXPAND)
        self.main_panel.SetSizer(main_sizer)

    #open up a file dialog and write to a file
    def export_tikz(self, evt):
        dialog = wx.FileDialog(self, style = wx.FD_SAVE)
        dialog.ShowModal()
        path = dialog.GetPath()
        if path != "":
            print path
            tf = open(path, "w")
            tf.write(get_tikz_code(self.view.graph))
            tf.close()

    def compute_gonality(self, event):
        gon = gonality.gonality(self.view.graph)
        self.gonality.SetValue(repr(gon))

    def draw_Bn(self,event):
        self.view.gen_Bn(10)


    #the function to call whenever an edge is updated
    def update_info(self, data):
        self.laplacian.SetValue(repr(data[0]))
        self.genus.SetValue(repr(data[1]))
        self.gonality.SetValue("")
        self.connec.SetValue(repr(data[2]))
        self.div.SetValue(repr(data[3]))
        self.subset.SetValue(repr(data[4]))
    
    def clear_event(self, event):
        self.view.clear()

    def clear_divisor(self, event):
        self.view.divisor.__init__(self.view.graph)
        self.view.update_info()
        self.view.Refresh()

    def add_infobox(self, title):
        infolabel = wx.StaticText(self.info_panel, label=title)
        infobox = wx.TextCtrl(self.info_panel)
        self.info_sizer.Add(infolabel)
        self.info_sizer.Add(infobox, 1, wx.EXPAND)
        return infobox

    def try_burn(self, event):
        if self.view.selection:       
            subset = self.view.divisor.burn(self.view.selection)
            if not subset:
                self.subset.SetValue("Cannot push chips closer")
                self.view.fireset = []
            else:
                self.subset.SetValue(repr(subset) + " - press 'Fire!' to chip-fire all")
                self.view.fireset = subset
        else:
            pass

    def get_jacob(self, event):
        self.view.graph.getJac()

app = wx.App()

frame=Frame('Graphmake')
frame.Show()

app.MainLoop()
