#!/usr/bin/python

from graph_ui.graph_frame import GraphFrame
import wx

app = wx.App()

def adj_mat(evt):
    global f_graph
    frame.set_infobox("adj",str(f_graph.adjacency()))    

frame=GraphFrame('Graphmake')
frame.add_infobox("adj","Adjacency matrix")
frame.add_button("Compute adjacency matrix", adj_mat)
f_graph = frame.view.graph


frame.Show()

app.MainLoop()
