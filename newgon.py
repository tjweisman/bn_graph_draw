#!/usr/bin/python

from gonality import *
from graph import *
from spanning_trees import *
import time
import random

def rand_graph(n,p):
    G = Graph()
    for x in xrange(n):
        G.add_vertex()

    while True:
        for x in xrange(n):
            for y in xrange(x+1,n):
                if random.random() <= p:
                    G.add_edge(G.vertices[x], G.vertices[y])

        if G.connected():
            #print "got connected \n"
            break
        else:
            G.edges = []

    return G




def compute_gonality(G):
	divisors_checked = 0
	n = len(G.vertices)
	divisors = []
	for x in xrange(2*n):
		divisors.append([])
	num_divisors = [0]*(2*n)
	sttime = time.time()
	trees = getST(G)
	for tree in trees:
		cur_div = getdivisor(tree, G)
		cur_degree = sum(cur_div.values)
		divisors[cur_degree].append(cur_div)
		num_divisors[cur_degree] += 1
	print "Trees and divisors: " +str(time.time() - sttime)
	degree = 0
	sttime = time.time()
	while True:
		for x in xrange(degree+1):
			for div in divisors[x]:
				divisors_checked += 1
				if rank_positive(div):
					print "Divisors checked: " + str(divisors_checked)
					print str(time.time() - sttime)
					return sum(div.values)
				div.set(G.vertices[0], div.get(G.vertices[0])+1)
		degree += 1

def speed_test(n):
	G = rand_graph(n, .5)
	compute_gonality(G)
	sttime = time.time()
	gonality(G)
	print time.time() - sttime

def num_trees(G):
	G.laplacian()
	M = G.SymQ
	return M[1:, 1:].det()
	
array =[(0,1),(1,2),(2,3),(3,4),(4,0),(0,5),(5,6),(6,7),(7,8),(8,9),(9,10),(10,11),
(7,11),(7,12),(12,13),(13,14),(0,14)]

G = Graph()
for x in xrange(15):
	G.add_vertex()
for tuple in array:
	G.add_edge(G.vertices[tuple[0]], G.vertices[tuple[1]])

print compute_gonality(G)
"""
eff_time = 0
ineff_time = 0

for x in xrange(10):
	print x
	G = rand_graph(9, .5)
	sttime = time.time()
	eff_gon = compute_gonality(G)
	eff_time = eff_time + time.time() - sttime
	sttime = time.time()
	ineff_gon = gonality(G)	
	ineff_time = ineff_time +time.time() - sttime
	if (eff_gon != ineff_gon):
		print "Ahhh"
		print G.laplacian()
		G.SymQ
"""