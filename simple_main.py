#!/usr/bin/python

from graph_ui.graph_frame import GraphFrame
import wx

app = wx.App()
frame=GraphFrame('Graphmake')
frame.add_infobox("adj","Adjacency matrix")
f_graph = frame.view.graph

def adj_mat(evt):
    global f_graph
    frame.set_infobox("adj",str(f_graph.adjacency()))

frame.add_button("Compute adjacency matrix", adj_mat)

frame.Show()
app.MainLoop()
