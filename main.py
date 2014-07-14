#!/usr/bin/python

import wx
import options
from drawgraph import *
from controller import *
import collections

sage_ok = True
OPTIONS=0

try:
    import sage.all
except ImportError as e:
    sage_ok = False

class InfoBox:
    def __init__(self, parent, title, sizer):
        self.name = title
        self.sizer = sizer
        self.parent = parent
        self.enabled=True

        self.label=wx.StaticText(self.parent, label=(self.name+":"))
        self.display=wx.TextCtrl(self.parent)
        self.display.SetEditable(False)
        
        self.sizer.Add(self.label, 0)
        self.sizer.Add(self.display, 1, wx.EXPAND)
        
    def set_value(self, text):
        self.display.SetValue(text)

    def set_enabled(self, value):
        self.enabled=value
        if value:
            self.label.Show()
            self.display.Show()
        else:
            self.label.Hide()
            self.display.Hide()        

#the main app window
class Frame(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, title=title, size=(600,600))        
        self.Center()

        self.main_panel = wx.Panel(self)

        self.options = collections.OrderedDict({})
        self.infoboxes = collections.OrderedDict({})
        self.buttons = []

        #main menu
        self.menu_bar = wx.MenuBar()
        self.file_menu = wx.Menu()
        self.menu_bar.Append(self.file_menu, 'File')
        self.SetMenuBar(self.menu_bar)

        #panel with buttons and text boxes
        self.info_panel = wx.Panel(self.main_panel)
        self.info_sizer = wx.FlexGridSizer(rows=0,cols=2)
        self.info_sizer.AddGrowableCol(1, proportion=5)
        self.info_panel.SetSizer(self.info_sizer)

        #buttons panel
        self.button_panel = wx.Panel(self.main_panel)
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.button_panel.SetSizer(button_sizer)

        #the graph drawing panel
        self.view = DrawPanel(self.main_panel, 
                              self.update_info,
                              self.options)

        self.controller = Controller(self)
    
        self.add_infobox("lap", "Laplacian")
        self.add_infobox("jac", "Jacobian")
        self.add_infobox("genus", "Genus")
        self.add_infobox("gonality", "Gonality")
        self.add_infobox("pair_guess", "<x,x>")
        self.add_infobox("trees", "Spanning trees")
        self.add_infobox("connect", "Connectedness")
        self.add_infobox("div", "Divisor")
        self.add_infobox("subset", "Fireable subset")

        self.add_file_option("Export TikZ", self.controller.export_tikz)
        self.add_file_option("Options", self.opt_dialog)

        self.add_button("Clear graph", self.controller.clear_event)
        self.add_button("Clear divisor", self.controller.clear_divisor)
        self.add_button("Compute gonality", self.controller.compute_gonality)
        self.add_button("Compute Jacobian", self.controller.compute_jacobian)
        self.add_button("Try burn", self.controller.try_burn)
        self.add_button("Draw B_n", self.controller.draw_Bn)

        button_sizer.AddMany([(button, 0) for button in self.buttons])
        
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.button_panel)
        main_sizer.Add(self.info_panel, 0, wx.EXPAND)
        main_sizer.Add(self.view, 1, wx.EXPAND)
        self.main_panel.SetSizer(main_sizer)

        options.setup_options(self)
        self.reconfigure()

    def add_infobox(self, name, title):
        infobox = InfoBox(self.info_panel, 
                          title, self.info_sizer)
        self.infoboxes[name] = infobox

    def add_file_option(self, name, callback):
        item = self.file_menu.Append(-1, name, name)
        self.Bind(wx.EVT_MENU, callback, item)

    def add_button(self, name, callback):
        button = wx.Button(self.button_panel, -1, name)
        button.Bind(wx.EVT_BUTTON, callback)
        self.buttons.append(button)

    def opt_dialog(self, event):
        dialog = options.OptionsDialog(self, self.options)
        dialog.ShowModal()
        
        self.reconfigure()
        self.info_panel.Layout()
        self.main_panel.Layout()

    def update_info(self):
        self.controller.update_info()

    def reconfigure(self):
        for key in self.infoboxes.keys():
            self.infoboxes[key].set_enabled(self.options[key].value)
        self.controller.update_lap(None)
        
        if self.options["divisor_iput"].value:
            self.view.divisor_panel.Show()
            self.view.v_radius = 10
            self.view.click_radius = 20
        else:
            self.view.v_radius = 5
            self.view.click_radius = 10
            self.view.divisor_panel.Hide()
        

app = wx.App()

frame=Frame('Graphmake')
frame.Show()

app.MainLoop()
