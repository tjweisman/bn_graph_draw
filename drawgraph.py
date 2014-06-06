#!/usr/bin/python

import wx
from graph import *
from math import sqrt

def draw_edge(gc, edge, graph):
    midpoint = Point()
    edge_v = Point()
    edge_perp = Point()
    midpoint.x = (edge.v1.x + edge.v2.x)/2 
    midpoint.y = (edge.v1.y + edge.v2.y)/2
    edge_v.x, edge_v.y = edge.v1.x - edge.v2.x, edge.v1.y - edge.v2.y
    edge_perp.x, edge_perp.y = -1 * float(edge_v.y), float(edge_v.x)
    
    #count the number of vertices on either side of the edge
    pos = 0
    neg = 0
    for vertex in filter(lambda v: not edge.has(v), graph.vertices):
        vec = Point()
        vec.x, vec.y = vertex.x - midpoint.x, vertex.y - midpoint.y
        mat = [[edge_v.x, edge_perp.x],[edge_v.y, edge_perp.y]]
        det = mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0]
        #product instead of quotient b/c we only care about sign
        param = (vec.y * mat[0][0] - vec.x *  mat[1][0]) * det
        if param > 0:
            pos += 1
        elif param < 0:
            neg += 1

    norm = sqrt(edge_perp.x**2 + edge_perp.y**2)
    if norm != 0:
        edge_perp.x /= norm
        edge_perp.y /= norm

    #draw a quadratic bezier curve between the edge
    #the control point is farther from the edge if there are more edges
    #it's placed on the side of the edge that has less vertices
    sign = 30
    if pos > neg:
        sign *= -1
    cx = midpoint.x + sign * edge_perp.x * (edge.index - 1)
    cy = midpoint.y + sign * edge_perp.y * (edge.index - 1)
    path = gc.CreatePath()
    path.MoveToPoint(edge.v1.x, edge.v1.y)
    path.AddQuadCurveToPoint(cx, cy, edge.v2.x, edge.v2.y)
    gc.DrawPath(path)

class DrawPanel(wx.Panel):
    def __init__(self, parent, info_evt):
        self.graph = Graph()
        wx.Panel.__init__(self, parent)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_click)
        self.Bind(wx.EVT_MOTION, self.mouse_move)
        self.black = wx.Brush((0,0,0))
        self.red = wx.Brush((255,0,0))
        self.gray = wx.Brush((150, 150, 150))
        self.pink = wx.Brush((255, 100, 100))

        self.info_evt = info_evt

        self.selection = None
    def on_size(self, event):
        event.Skip()
        self.Refresh()
    def on_paint(self, event):
        w,h = self.GetClientSize()
        dc = wx.PaintDC(self)        
        dc.SetBackground(wx.Brush("white"))
        dc.Clear()
        gc = wx.GraphicsContext.Create(dc)
        gc.SetPen(wx.Pen("black", 1))

        for edge in self.graph.edges:
            draw_edge(gc, edge, self.graph)

        for vertex in self.graph.vertices:
            if vertex.selected and not vertex.hover:
                gc.SetBrush(self.red)
            elif vertex.selected:
                gc.SetBrush(self.pink)
            elif vertex.hover:
                gc.SetBrush(self.gray)
            else:
                gc.SetBrush(self.black)
            gc.DrawEllipse(vertex.x - Vertex.radius, 
                           vertex.y - Vertex.radius, 
                           2 * Vertex.radius, 
                           2 * Vertex.radius)
    def on_click(self, event):
        x,y = event.GetX(), event.GetY()
        for vertex in self.graph.vertices:
            if vertex.over(x, y):
                if self.selection:
                    #TODO: check that we didn't deselect
                    self.graph.add_edge(self.selection, vertex)
                    self.selection.selected = False
                    self.selection = None
                    self.info_evt(
                        self.graph.laplacian(),
                        self.graph.jacobian(),
                        self.graph.guess_pairing())
                else:
                    self.selection = vertex
                    vertex.selected = True
                self.Refresh()
                return
        self.graph.add_vertex(x, y)
        last = self.graph.get_last()
        if event.ShiftDown() and self.selection:
            self.graph.add_edge(self.selection, last)
            self.info_evt(
                self.graph.laplacian(),
                self.graph.jacobian(),
                self.graph.guess_pairing())
        self.graph.deselect_all()
        self.selection = last
        self.selection.selected = True
        self.Refresh()
    def mouse_move(self, event):
        x,y = event.GetX(), event.GetY()
        for vertex in self.graph.vertices:
            if vertex.over(x,y):
                vertex.hover = True
            else:
                vertex.hover = False
        self.Refresh()
