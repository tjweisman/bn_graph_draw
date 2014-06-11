# some functions to do gonality computations

from Queue import Queue
from sympy.matrices import *
from graph import *

#implementation of Algorithm 5.1 in Bruyn '12
def semi_reduce(D, G):
    n = len(G.vertices)
    x = Divisor(G)
    if n <= 1:
        return D
    for vertex in G.vertices[1:]:
        x.set(vertex, vertex.deg - D.get(vertex))
    #S for SymPy
    xS = Matrix(n - 1, 1, D.values[1:])
    QS = G.sym_laplacian()
    yS = zeros(1).col_join(QS.minorMatrix(0,0).LUsolve(xS))
    vals = [x + y for x,y in zip(D.values, QS * yS.applyfunc(floor))]
    d = Divisor(G)
    d.values = vals
    return d

#implementation of algorithm 5.3, 2A in Bruyn '12
def find_possible_set(Dv, G):
    n = len(G.vertices)
    outdegree = [0]*n
    state = [True]*n
    A_i = ones(n,1)

    num = 0
    #queue of fully burned vertices
    remove_q = Queue()
    remove_q.put(G.vertices[0])
    state[0] = False
    A = G.adjacency()
    while not remove_q.empty():
        v = remove_q.get()
        A_i[v.i] = 0
        num += 1
        #how many "buckets"/"firefighters" left on this vertex
        outdegree = [x - y for x,y in zip(outdegree, A[v.i])]
        for v_n in get_neighbors(v, G):
            if state[v_n.i] and Dv[v_n.i] - outdegree[v_n.i] < 0:
                state[v_n.i] = False
                remove_q.put(v_n)
    if num >= n:
        return None
    return A_i

#implementation of algorithm 5.3, 2B in Bruyn '12
def full_reduce(D, G):
    d = semi_reduce(D, G)
    n = len(G.vertices)
    Q = G.sym_laplacian()
    DM = Matrix(n, 1, d.values)
    A_f = find_possible_set(DM, G)
    #keep chip-firing until we've burned the whole graph
    while A_f:
        DM -= Q * A_f
        A_f = find_possible_set(DM, G)
    d.values = DM.T.tolist()[0]
    return d

def get_neighbors(v, G):
    A = G.adjacency()
    n = len(A)
    neighbors = [None]*n
    num = 0
    for i in range(n):
        if A[v.i][i] != 0:
            neighbors[num] = G.vertices[i]
            num += 1
    return neighbors[:num]
