# this file contains code for actually storing/computing graph information

sage_ok = True
sympy_ok = True
try:
    from sage.all import *
except ImportError as e:
    sage_ok = False

try:
    from sympy.matrices import *
    from sympy import floor
except ImportError as e:
    sympy_ok = False

from subprocess import call

class Point:
    pass

class Vertex:
    #number of vertices defined so far.
    #this will break if we define more than one graph!
    count = 0
    
    #vertex display information
    radius = 5
    click_radius = 20

    def __init__(self, x=0, y=0):
        self.i = Vertex.count
        Vertex.count += 1
        self.x, self.y = x,y
        
        #keep a running tab on the degree
        self.deg = 0

        #more display information
        self.selected = False
        self.hover = False
    def move(self, x, y):
        self.x, self.y = x, y
    
    #True iff the given x/y coordinates are over the vertex
    def over(self, x, y):
        return ((x - self.x)**2 + (y - self.y)**2) < Vertex.click_radius**2

class Edge:
    def __init__(self, v1, v2):
        self.v1, self.v2 = v1, v2
        self.v1.deg += 1
        self.v2.deg += 1
    def has(self, v):
        return (v.i == self.v1.i or v.i == self.v2.i)
    
class Graph:
    def __init__(self):
        self.vertices = []
        self.edges = []
        #laplacian is None whenever it's out-of-date
        self.Q = None
        self.A = None
        # SymPy version of laplacian (so we don't call the matrix constructor
        # unnecessarily)
        self.SymQ = None
    def add_vertex(self, x=0, y=0):
        self.vertices.append(Vertex(x,y))
        self.Q = None
        self.A = None
    def add_edge(self, v1, v2):
        self.edges.append(Edge(v1, v2))
        
        #edges need to have an idea of multiplicity so they can get drawn
        #correctly
        self.edges[-1].index = 0
        for edge in self.edges:
            if edge.has(v1) and edge.has(v2):
                self.edges[-1].index += 1
        self.Q = None
        self.A = None
    def deselect_all(self):
        for vertex in self.vertices:
            vertex.selected = False
    def get_last(self):
        return self.vertices[-1]

    def sym_laplacian(self):
        if self.Q:
            return self.SymQ
        self.laplacian()
        return self.SymQ
        
    def adjacency(self):
        n = len(self.vertices)
        if self.A:
            return self.A
        self.A = [x[:] for x in [[0]*n]*n]
        for edge in self.edges:
            i,j = edge.v1.i, edge.v2.i
            self.A[i][j] -= 1
            self.A[j][i] -= 1
        return self.A
    def laplacian(self):
        # if we already have a valid laplacian don't bother recomputing it
        if self.Q:
            return self.Q
        n = len(self.vertices)
        self.Q = [x[:] for x in [[0]*n]*n]
        for edge in self.edges:
            i,j = edge.v1.i, edge.v2.i
            self.Q[i][j] -= 1
            self.Q[j][i] -= 1
            self.Q[i][i] += 1
            self.Q[j][j] += 1
        if sympy_ok:
            self.SymQ = Matrix(self.Q)
        return self.Q
        
    def jacobian(self):
        if not sage_ok:
            return self.jacobian_no_sage()
        Q = matrix(self.laplacian())
        return filter(lambda x: x != 0 and x != 1, Q.elementary_divisors())

    def guess_pairing(self):
        if not sympy_ok:
            return "SymPy needed to compute pairing guess"
        n = len(self.vertices)
        Q = self.SymQ #this is SymPy!
        J = ones(n,n)

        #Moore-Penrose pseudoinverse
        if (Q + J/n).det() == 0:
            return 0
        pinv = (Q + J/n).inv() - J/n
        
        div = zeros(n, 1)
        div[0,0] = -1
        # we might not get a generator, or even have a cyclic group at all
        # in which case this is fairly meaningless
        for i in range(1,n):
            div[i,0] = 1
            pair = (div.T * pinv * div)[0,0]
            if pair != 0:
                return pair
        return 0
        
    def print_laplacian(self):
        Q = self.laplacian()
        print Q
        print repr(Q).replace("[","{").replace("]","}") #mathematica syntax
        print ""

    def clear(self):
        self.vertices = []
        self.edges = []
        self.Q = None
        self.SymQ = None
        Vertex.count = 0

    def genus(self):
        return len(self.edges) - len(self.vertices) + 1
    
    #TODO: pipe this to a running sage process so it doesn't take as long
    #also make this way less dumb
    def jacobian_no_sage(self):
        tmp = open("tmp.sage", "w")
        tmp.write("A = matrix(%s)\n"%repr(self.laplacian()))
        tmp.write("div = A.elementary_divisors()\n")
        tmp.write("div = filter(lambda x: x != 0 and x != 1, div)\n")
        tmp.write("out = open('output', 'w')\n")
        tmp.write("out.write(repr(div))\n")
        tmp.write("out.close()")
        tmp.close()
        call(["sage","tmp.sage"])
        tmp = open("output","r")
        jac = eval(tmp.read())
        tmp.close()
        return jac
        
# a divisor on a graph
class Divisor:
    def __init__(self, graph):
        self.graph = graph
        self.values = ([0]*len(graph.vertices))[:]
        self.degree = 0
    def set(self, vertex, value):
        self.values[vertex.i] = value
    def get(self, vertex):
        return self.values[vertex.i]
    def compute_degree(self):
        self.degree = sum(self.values)
