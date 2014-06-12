#!/usr/bin/python

#contains most of the code for the graph drawing panel
#some display information (whether a vertex is selected, etc.) is contained
#in graph.py

#UI main loop and parent window are started in main.py

import wx
from graph import *
from math import sqrt

def control_point(edge, graph):
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

    #get coordinates for a quadratic bezier curve between the edge.
    #the control point is farther from the edge if there are more edges.
    #it's placed on the side of the edge that has fewer vertices
    sign = 30
    if pos > neg:
        sign *= -1
    c = Point()
    c.x = midpoint.x + sign * edge_perp.x * (edge.index - 1)
    c.y = midpoint.y + sign * edge_perp.y * (edge.index - 1)
    return c
    
#transform a point in window coords to tikz coords
def tikz_transform(point, origin, scale):
    #y-axis is flipped, since +y = down in window coords
    return ((point.x - origin.x)/scale, (origin.y - point.y)/scale)

def get_tikz_code(graph):
    scale  = float(50) #pixels to TikZ coordinates
    origin = Point()
    
    #the following isn't super efficient, but whatever
    origin.x = min(map(lambda v: v.x, graph.vertices) +
                   map(lambda e: control_point(e, graph).x, graph.edges))
    origin.y = max(map(lambda v: v.y, graph.vertices) +
                   map(lambda e: control_point(e, graph).y, graph.edges))

    output = "\\begin{tikzpicture}\n"
    for vertex in graph.vertices:
        output += "\\filldraw (%f, %f) circle (3pt);\n"%tikz_transform(vertex, origin, scale)
    for edge in graph.edges:
        ctrl = control_point(edge, graph)
        tikz_tup = (tikz_transform(edge.v1, origin, scale) +
                    tikz_transform(ctrl, origin, scale) + 
                    tikz_transform(edge.v2, origin, scale))
        output += "\draw (%f, %f) .. controls (%f, %f) .. (%f, %f);\n"%tikz_tup
    output += "\\end{tikzpicture}\n"
    return output

#the graph-drawing panel
class DrawPanel(wx.Panel):
    def __init__(self, parent, info_evt):
        self.graph = Graph()
        wx.Panel.__init__(self, parent)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_click)
        self.Bind(wx.EVT_MOTION, self.mouse_move)
        
        #vertex colors
        self.black = wx.Brush((0,0,0))
        self.red = wx.Brush((255,0,0))
        self.gray = wx.Brush((150, 150, 150))
        self.pink = wx.Brush((255, 100, 100))

        #function to call whenever an edge is added to the graph
        self.info_evt = info_evt

        #which vertex is selected (red), or None if none is
        self.selection = None
    def on_size(self, event):
        event.Skip()
        self.Refresh()
    def on_paint(self, event):
        w,h = self.GetClientSize()
        dc = wx.BufferedPaintDC(self)        
        dc.SetBackground(wx.Brush("white"))
        dc.Clear()
        gc = wx.GraphicsContext.Create(dc)
        gc.SetPen(wx.Pen("black", 1))

        #draw edges
        for edge in self.graph.edges:
            ctrl = control_point(edge, self.graph)
            path = gc.CreatePath()
            path.MoveToPoint(edge.v1.x, edge.v1.y)
            path.AddQuadCurveToPoint(ctrl.x, ctrl.y, edge.v2.x, edge.v2.y)
            gc.DrawPath(path)

        #draw vertices
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
                    self.update_info()
                else:
                    self.selection = vertex
                    vertex.selected = True
                self.Refresh()
                return
        self.graph.add_vertex(x, y)
        last = self.graph.get_last() #the vertex we just added
        if event.ShiftDown() and self.selection:
            self.graph.add_edge(self.selection, last)
            self.update_info()
        self.graph.deselect_all()
        self.selection = last
        self.selection.selected = True
        self.Refresh()
    def update_info(self):
        self.info_evt(
            [self.graph.laplacian(),
             self.graph.jacobian(),
             self.graph.genus(),
             self.graph.guess_pairing()])
    def mouse_move(self, event):
        #draw different colors if we're hovering
        x,y = event.GetX(), event.GetY()
        for vertex in self.graph.vertices:
            if vertex.over(x,y):
                vertex.hover = True
            else:
                vertex.hover = False
        self.Refresh()
    def clear(self):
        self.graph.clear()
        self.selection = None
        self.Refresh()
