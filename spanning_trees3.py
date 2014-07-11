from graph import *

class node:
	#optional parameter keeps track of ancestor
	def __init__(self, G = Graph(), ancestor = []):
		self.tree = ancestor[:]
		self.G = G
	
	#make tree node unique by exchanging an edge for a fundamental edge
	def new_node(self, new_edge, stale_edge):
		self.tree[new_edge] = 1
		#do we need to check that this edge is actually in the tree?
		self.tree[stale_edge] = 0
	
	#adjacent vertices to a vertex v in a node's tree
	def adj_verts(self, v_num, edge_info):
		adj_vert_list = []
		
		num_G_edges = self.G.ecount

		for edge in xrange(num_G_edges):
			if self.tree[edge] and v_num in edge_info[edge]:
				adj_vert_list.append(edge_info[edge][0])
				adj_vert_list.append(edge_info[edge][1])
				adj_vert_list.remove(v_num)

		return adj_vert_list


    #find all paths between two vertices in a node's tree
    #return a list of paths (which are in turn lists of vertices in the path)
	def find_path(self, start_vertex, end_vertex, edge_info, path=[]):
		num_G_edges = len(edge_info)
	
        #return if you've gotten to the end point
		if start_vertex == end_vertex:
			return path

        #move starting point to all adjacent vertices and call function again
		for vertex in self.adj_verts(start_vertex, edge_info):
			k = 0
			#check if the vertex is already in the path
			for edge_num in path:
				if vertex in edge_info[edge_num]:
					k += 1
					break
			#if vertex is not already in path, extend the path
			if k == 0:
				new_edge = 0
				for edge_num in range(num_G_edges):
					if vertex in edge_info[edge_num] and start_vertex in edge_info[edge_num]:
						new_edge = edge_num
						break

				extend_path = self.find_path(vertex, end_vertex, edge_info, path + [new_edge])
				if extend_path:
					return extend_path

		return []


#generate trees from a node
#optional parameter keeps track of which fundamental edges to not consider
#note to self: only change trees by fundamental edges > final parameter
#note to self: will need to keep track of how many fundamental edges cdhanged
def gen_trees(tree_node, FE, INx, OUTx, edge_info):
	Trees = []
	Trees.append(tree_node.tree)

	out_len = len(OUTx)
	
	while len(FE) > 0:

		fund_edge = FE[0]

		if not OUTx[fund_edge]:

			f = edge_info[fund_edge]
			v, w = f[0], f[1]
			b_cycle = tree_node.find_path(v, w, edge_info)
			cycle = []
			for edge in b_cycle:
				if not INx[edge]:
					cycle.append(edge)

			new_IN = INx[:]
			new_IN[fund_edge] = 1

			new_OUT = OUTx[:]

			cycle_len = len(cycle)
			
			for e_i in xrange(cycle_len):
				new = node(tree_node.G, tree_node.tree)
				new.new_node(fund_edge, cycle[e_i])
				
				remember = 0
				if new_OUT[cycle[e_i]] == 1:
					remember = 1
				else: new_OUT[cycle[e_i]] = 1

				FE_copy = FE[:]

				more_Trees = gen_trees(new, FE_copy, new_IN, new_OUT, edge_info)
				for t in more_Trees:
					Trees.append(t)

				if remember == 0:
					new_OUT[cycle[e_i]] = 0
				new_IN[cycle[e_i]] = 1

		FE.pop(0)

	#n = 0
	#while n < len(Trees):
	#	if Trees.index(Trees[n]) != n:
	#		Trees.pop(n)
	#	else: n += 1

	return Trees

def Main(G):

	G_ecount = G.ecount

	edge_info = []
	for edge in G.edges:
		vert1 = edge.v1.i
		vert2 = edge.v2.i
		edge_info.append([vert1, vert2])

	#adj_Matrix = [[0]*G.vcount]*G.vcount
	#for edge in G.edges:
	#	v_1 = edge.v1.i
	#	v_2 = edge.v2.i
	#	adj_Matrix[v_1][v_2] = 1
	#	adj_Matrix[v_2][v_1] = 1

	#find the first tree
	T = G.find_tree(edge_info)
	#initialize list of fundamental edges
	F = []

	#fill list of fundamental edges
	edge_num = 0
	while edge_num < G_ecount:
		if not T[edge_num]:
			F.append(edge_num)
		edge_num += 1

	#print "\n Here are the fundamental edges:"
	#for edge_num in F:
		#edge = G.edges[edge_num]
		#print "[" + str(edge.v1.i) + "," + str(edge.v2.i) + "]",
	#print "\n"

	#create node from T
	T_node = node(G, T)

	print "\n Here are all trees:"

	Spanning_Trees = gen_trees(T_node, F, [0]*G_ecount, [0]*G_ecount, edge_info)

	n = 0
	r = 0
	while n < len(Spanning_Trees):
		if Spanning_Trees.index(Spanning_Trees[n]) != n:
			Spanning_Trees.pop(n)
			r += 1
		else: n += 1
		
	for tree in Spanning_Trees:
		print "Tree " + str(Spanning_Trees.index(tree) + 1) + ": ",
		for edge_num in range(G_ecount):
			if tree[edge_num]:
				print "[" + str(edge_info[edge_num][0]) + "," + str(edge_info[edge_num][1]) + "]",
		print "\n"

	print "#repeats: " + str(r)


G = Graph()
G.add_vertex()
G.add_vertex()
G.add_vertex()
G.add_vertex()
G.add_vertex()
G.add_vertex()
G.add_vertex()

G.add_edge(G.vertices[0], G.vertices[1])
G.add_edge(G.vertices[1], G.vertices[2])
G.add_edge(G.vertices[2], G.vertices[3])
G.add_edge(G.vertices[3], G.vertices[4])
G.add_edge(G.vertices[4], G.vertices[5])
G.add_edge(G.vertices[5], G.vertices[6])
G.add_edge(G.vertices[6], G.vertices[0])
G.add_edge(G.vertices[0], G.vertices[2])
G.add_edge(G.vertices[0], G.vertices[3])
G.add_edge(G.vertices[0], G.vertices[4])
G.add_edge(G.vertices[0], G.vertices[5])
G.add_edge(G.vertices[1], G.vertices[3])
G.add_edge(G.vertices[1], G.vertices[4])
G.add_edge(G.vertices[1], G.vertices[5])
G.add_edge(G.vertices[1], G.vertices[6])
G.add_edge(G.vertices[2], G.vertices[4])
G.add_edge(G.vertices[2], G.vertices[5])
G.add_edge(G.vertices[2], G.vertices[6])
G.add_edge(G.vertices[3], G.vertices[5])
G.add_edge(G.vertices[3], G.vertices[6])
G.add_edge(G.vertices[4], G.vertices[6])

Main(G)





