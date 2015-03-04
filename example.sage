from graph import Graph, Divisor
from gonality import rank_nonnegative

def graph_from_sage(sage_graph):
    """utility function to convert a Sage graph object into this program's
    internal graph object"""
    G = Graph()
    for vertex in sage_graph.vertices():
        G.add_vertex()
    for edge in sage_graph.edges():
        v1 = G.vertices[edge[0]]
        v2 = G.vertices[edge[1]]
        G.add_edge(v1, v2)

    return G


G = graph_from_sage(graphs.CycleGraph(6))

D1 = Divisor(G, [-6, 6, 0, 0, 0, 0])
D2 = Divisor(G, [-1, 1, 0, 0, 0, 0])

print rank_nonnegative(D1)
print rank_nonnegative(D2)
