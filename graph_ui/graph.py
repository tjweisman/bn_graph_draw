"""this file contains code for actually storing/computing graph information"""

import sage_wrapper
import inspect
sage_util = sage_wrapper.sagely_import("graph_ui.sage_utils")

sympy_ok = True

try:
    from sympy.matrices import *
    from sympy import floor
except ImportError as e:
    sympy_ok = False

from subprocess import call

class Point:
    pass

class Vertex:
    def __init__(self, x=0, y=0):
        self.i = 0
        self.x, self.y = x,y
        
        #keep a running tab on the degree
        self.deg = 0

        #more display information
        self.selected = False
        self.hover = False
    def move(self, x, y):
        self.x, self.y = x, y
    
    #True iff the given x/y coordinates are over the vertex
    def over(self, x, y, click_radius):
        return ((x - self.x)**2 + (y - self.y)**2) < click_radius**2

class Edge:
    def __init__(self, v1, v2):
        self.v1, self.v2 = v1, v2
        self.v1.deg += 1
        self.v2.deg += 1
    def has(self, v):
        return (v.i == self.v1.i or v.i == self.v2.i)

    def compare_edge(self, other_edge):
        if other_edge.v1.i == self.v1.i and other_edge.v2.i == self.v2.i:
            return True
        elif other_edge.v2.i == self.v1.i and other_edge.v1.i == self.v2.i:
            return True
        else: return False


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
        self._connected_ = True
    def add_vertex(self, x=0, y=0):    
        new = Vertex(x,y)
        new.i = len(self.vertices)
        self.vertices.append(new)
        self.Q = None
        self.A = None
        self._connected_ = None
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
    
    def delete_vertex(self, v):
        self.vertices.remove(v)
        for edge in self.edges[:]:
            if edge.has(v):
                self.edges.remove(edge)
        
        for i, v in enumerate(self.vertices):
            v.i = i
        self.A = None
        self.Q = None
    def deselect_all(self):
        for vertex in self.vertices:
            vertex.selected = False
    def get_last(self):
        return self.vertices[-1]

    def connected(self):
        #this code is really crappy, probably because Dan Mitropolsky wrote it.
        #unfortunately, I can't port to Sage because I might not have access. 
        if self._connected_ == True or self._connected_ == False:
            return self._connected_
        
        vseen, edgeQ = [], []
        edgeL = list(self.edges)
        self._connected_ = True
        try:
            newv = self.vertices[0]
            vseen.append(newv)
            nseen = 1
        except:
            return self._connected_

        while nseen < len(self.vertices):
            for e in edgeL:
                if e.has(newv):
                    edgeQ.append(e)
                  #  edgeL.remove(e)
            while True:
                if len(edgeQ) == 0:
                    self._connected_ = False
                    return False
                if edgeQ[0].v1 not in vseen:
                    newv = edgeQ[0].v1
                    vseen.append(newv)
                    nseen += 1
                    edgeQ.pop(0)
                    break
                if edgeQ[0].v2 not in vseen:
                    newv = edgeQ[0].v2
                    vseen.append(newv)
                    nseen += 1
                    edgeQ.pop(0)
                    break
                edgeQ.pop(0)

        return self._connected_

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
        if self.connected():
            return sage_util.graph_jacobian(self.laplacian())
        else:
            return "disconnected"

    def guess_pairing(self):
        if not sympy_ok:
            return "SymPy needed to compute pairing guess"
        n = len(self.vertices)
        if n == 0: 
            return None
        Q = self.sym_laplacian() #this is SymPy!
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

    def genus(self):
        return len(self.edges) - len(self.vertices) + 1

    def outdeg(self, subset, vertex):
        count = 0
        for e in self.edges:
            if e.has(vertex) and ((e.v1.i not in subset) or (e.v2.i not in subset)):
                count += 1
        return count
    
    def find_tree(self):
        #initialize tree as a list of edges
        T = []
        #initialize stack of visited vertices
        visit_stack = []
        #initialize list of visited vertices
        visited_verts = []
        #visit the first vertex: mark as visited, add to stack
        visit_stack.append(self.vertices[0])
        visited_verts.append(self.vertices[0])
        #visit all - as yet - unvisited vertices adjacent to the top of the stack
        #add associated edges to the tree
        #pop top of stack
        #continue until stack is empty
        while(len(visit_stack) > 0):
            v = visit_stack[0]
            #w = Vertex()
            for edge in self.edges:
                if edge.has(v): 
                    if edge.v1 == v:
                        w = edge.v2
                    elif edge.v2 == v:
                        w = edge.v1
                    k = 0
                    while k < len(visited_verts): 
                        if visited_verts[k] == w:
                            break
                        k += 1
                    if k == len(visited_verts):
                        visit_stack.append(w)
                        visited_verts.append(w)
                        T.append(self.edges.index(edge))
            visit_stack.pop(0)
        if len(visited_verts) != len(self.vertices):
           # print "Can't find a spanning tree!"
           # print "Visited vertices:" + str(len(visited_verts))
           # print "Graph vertices:" + str(len(self.vertices))
           # print "Tree length" + str(len(T))
            return []
        else:
            return T

    def getJac(self, startv = 0, ordering = []):
        Spanning_Trees = spanning_trees.getST(self)
        Jac = []
        for tree in Spanning_Trees:
            Jac.append(getdivisor(tree,self,startv,ordering))

        for divisor in Jac:
            print str(divisor)

# a divisor on a graph
class Divisor:
    def __init__(self, graph, forceval = []):
        self.graph = graph
        if not forceval or (len(forceval) != len(graph.vertices)):
            self.values = [0]*len(graph.vertices)
        else:
            self.values = forceval
        self.degree = 0
    def delete_vertex(self, v):
        self.values.pop(v.i)
    def extend(self, value=0):
        self.values.append(value)
    def set(self, vertex, value):
        self.values[vertex.i] = value
    def get(self, vertex):
        return self.values[(vertex.i)]
    def compute_degree(self):
        self.degree = sum(self.values)

    def burn(self, vertex):
        vertex = vertex.i
        for i in xrange (0,len(self.values)):
            if (i != vertex) and (self.values[i] < 0):
                return False
        A = range(0,len(self.values))
        for n in xrange (0,len(self.values)):
            A.remove(vertex)
            found = 0
            for v in A:
                if self.values[v] < self.graph.outdeg(A,self.graph.vertices[v]):
                    vertex = v
                    found = 1
                    break
            if not found:
                return A
        return []

    def fire(self, vertex):
        for e in self.graph.edges:
            if e.has(vertex):
                self.values[vertex.i] -= 1
                if e.v1 != vertex:
                    self.values[e.v1.i] += 1
                else:
                    self.values[e.v2.i] += 1

    def borrow(self, vertex):
        for e in self.graph.edges:
            if e.has(vertex):
                self.values[vertex.i] += 1
                if e.v1 != vertex:
                    self.values[e.v1.i] -= 1
                else:
                    self.values[e.v2.i] -= 1

def getdivisor(tree, G, startv = 0, ordering = []):

        if not ordering:
            ordering = range(len(G.edges))

        if len(ordering) != len(G.edges):
            return 0

        n = len(G.vertices)
        burnt = [startv]
        ecount = [0]*n
        div = Divisor(G)
        burntnum = 1

        while burntnum < n:
            for i in ordering:
                e = G.edges[i]
                if (e.v1.i in burnt) or (e.v2.i in burnt):
                    ordering.remove(i)
                    if e.v1.i not in burnt:
                        v = e.v1.i
                    elif e.v2.i not in burnt:
                        v = e.v2.i
                    else:
                        break

                    if i in tree:
                        burnt.append(v)
                        burntnum += 1
                        div.set(G.vertices[v],ecount[v])
                    else:
                        ecount[v] += 1
                    break
        div.set(G.vertices[startv], 1)
        return div
