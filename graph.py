from sage.all import *
from sympy.matrices import *

class Point:
    pass

class Vertex:
    count = 0
    radius = 5
    click_radius = 20
    def __init__(self, x=0, y=0):
        self.i = Vertex.count
        Vertex.count += 1
        self.x, self.y = x,y
        self.selected = False
        self.hover = False
    def move(self, x, y):
        self.x, self.y = x, y
    
    def over(self, x, y):
        return ((x - self.x)**2 + (y - self.y)**2) < Vertex.click_radius**2

class Edge:
    def __init__(self, v1, v2):
        self.v1, self.v2 = v1, v2
    def has(self, v):
        return (v.i == self.v1.i or v.i == self.v2.i)
    
class Graph:
    def __init__(self):
        self.vertices = []
        self.edges = []
    def add_vertex(self, x=0, y=0):
        self.vertices.append(Vertex(x,y))
    def add_edge(self, v1, v2):
        self.edges.append(Edge(v1, v2))
        self.edges[-1].index = 0
        for edge in self.edges:
            if edge.has(v1) and edge.has(v2):
                self.edges[-1].index += 1
    def deselect_all(self):
        for vertex in self.vertices:
            vertex.selected = False
    def get_last(self):
        return self.vertices[-1]

    def laplacian(self):
        n = len(self.vertices)
        Q = [x[:] for x in [[0]*n]*n]
        for edge in self.edges:
            i,j = edge.v1.i, edge.v2.i
            Q[i][j] -= 1
            Q[j][i] -= 1
            Q[i][i] += 1
            Q[j][j] += 1
        return Q
        
    def jacobian(self):
        Q = matrix(self.laplacian())
        return filter(lambda x: x != 0 and x != 1, Q.elementary_divisors())

    def guess_pairing(self):
        n = len(self.vertices)
        Q = Matrix(self.laplacian()) #this is SymPy!
        J = ones(n,n)
        pinv = (Q + J/n).inv() - J/n
        
        div = zeros(n, 1)
        div[0,0] = -1
        #we might not get a generator... is there a way to check?
        for i in range(1,n):
            div[i,0] = 1
            pair = (div.T * pinv * div)[0,0]
            if pair != 0:
                return pair
        return 0
        

    def print_laplacian(self):
        Q = self.laplacian()
        print Q
        print repr(Q).replace("[","{").replace("]","}")
        print ""
        
