# some functions to do gonality computations

from Queue import Queue
from sympy.matrices import *
from graph import *

#implementation of Algorithm 5.1 in Bruyn '12
def semi_reduce(D, v0):
    G = D.graph
    n = len(G.vertices)
    x = Divisor(G)
    if n <= 1:
        return D
    for vertex in G.vertices[:v0.i] + G.vertices[v0.i+1:]:
        x.set(vertex, vertex.deg - D.get(vertex))
    #S for SymPy
    xS = Matrix(n - 1, 1, x.values[:v0.i] + x.values[v0.i+1:])
    QS = G.sym_laplacian()
    yS = QS.minorMatrix(v0.i,v0.i).LUsolve(xS).row_insert(v0.i,Matrix([0]))
    vals = [x + y for x,y in zip(D.values, QS * yS.applyfunc(floor))]
    d = Divisor(G)
    d.values = vals
    return d

#implementation of algorithm 5.3, 2A in Bruyn '12
def find_possible_set(Dv, G, v0):
    n = len(G.vertices)
    outdegree = [0]*n
    state = [True]*n
    A_i = ones(n,1)

    num = 0
    #queue of fully burned vertices
    remove_q = Queue()
    remove_q.put(v0)
    state[v0.i] = False
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
def full_reduce(D, v0):
    G = D.graph
    d = semi_reduce(D, v0)
    n = len(G.vertices)
    Q = G.sym_laplacian()
    DM = Matrix(n, 1, d.values)
    A_f = find_possible_set(DM, G, v0)
    #keep chip-firing until we've burned the whole graph
    while A_f:
        DM -= Q * A_f
        A_f = find_possible_set(DM, G, v0)
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

#implementation of algorithm 5.3 in Bruyn '12
def rank_nonnegative(D):
    G = D.graph
    v = G.vertices[0]
    d = full_reduce(D, v)
    return d.values[0] >= 0

def rank_positive(D):
    G = D.graph
    for v in G.vertices:
        d = full_reduce(D,v)
        if d.values[v.i] < 1:
            return False
    return True

def acc_def(acc, next_acc):
    return False

def eval_def(acc):
    return acc

#iterate through all divisors
#effective divisors of degree k correspond to ordered partitions of k by n
#integers. Iterate through those partitions recursively
def iterate_partition(callback, values, index, total, 
                      acc=False, accumulate=acc_def,
                      acc_eval=eval_def):
    if index == len(values) - 1:
        values[-1] = total
        #whenever we complete a new partition, call the callback
        val = callback(values)
        return val
    else:
        for i in range(total + 1):
            values[index] = i
            #update the accumulator with the result of the callback
            next_acc = iterate_partition(callback, 
                                         values, 
                                         index + 1, 
                                         total - i, 
                                         acc, accumulate,
                                         acc_eval)
            acc = accumulate(acc, next_acc)
            #sometimes we can return 
            #(e.g. if we find a divisor of positive rank)
            if acc_eval(acc):
                return acc
        return acc
        

#this function is called on an ordered partition of k
def gonality_callback(values, G):
    D = Divisor(G)
    D.values = values
    if rank_positive(D):
        return D
    return None

#no complex behavior needed; if we find a divisor of positive rank, return it
def gonality_accumulate(acc, next_acc):
    if acc:
        return acc
    elif next_acc:
        return next_acc
    return acc

def gonality(G):
    n = len(G.vertices)
    values = [0]*n
    for i in range(1, n):
        pos_div = iterate_partition(lambda val: gonality_callback(val, G),
                                    values, 0, i, 
                                    accumulate=gonality_accumulate)
        if pos_div:
            return i
    return -1 #if the code reaches this point, something is fucked up
