#!/usr/bin/python

"""The main application file for the graph drawer.

This file contains the layout and contents of the main window. It
relegates actual control to a Controller object (see controller.py).

It also defines the behavior of global application options in
reconfigure() method.

"""

import wx, controller
from graph_ui.graph_frame import GraphFrame

sage_ok = True
OPTIONS=0

try:
    import sage.all
except ImportError as e:
    sage_ok = False

app = wx.App()
frame = GraphFrame('Graphmake')
control = controller.Controller(frame)

#add infoboxes
frame.add_infobox("lap", "Laplacian")
frame.add_infobox("jac", "Jacobian")
frame.add_infobox("genus", "Genus")
frame.add_infobox("gonality", "Gonality")
frame.add_infobox("pair_guess", "<x,x>")
frame.add_infobox("trees", "Spanning trees")
frame.add_infobox("connect", "Connectedness")
frame.add_infobox("div", "Divisor")
frame.add_infobox("subset", "Fireable subset")
frame.add_infobox("zero", "Is zero")

#add buttons
frame.add_button("Clear graph", control.clear_event)
frame.add_button("Clear divisor", control.clear_divisor,
                display_opt="divisor_iput")
frame.add_button("Compute gonality", 
                control.compute_gonality, 
                display_opt="gonality")

if not sage_ok:
    frame.add_button("Compute Jacobian", 
                    control.compute_jacobian, 
                    display_opt="jac")

frame.add_button("Try burn", control.try_burn,
                display_opt="divisor_iput")
frame.add_button("Draw B_n", control.draw_Bn)
frame.add_button("Start sage", control.start_sage)

#add file menu options
frame.add_file_option("Export TikZ", control.export_tikz)

#add update callback
frame.set_update_callback(control.update_info)

frame.Show()

app.MainLoop()
