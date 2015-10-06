import random
import pickle

from fvs import *
from random import randint

# Split an integer into a sum.
# Not very "fair", but nice and simple.
def split(k: int) -> list:
	n = randint(1, k)
	if n < k:
		return [n] + split(k - n)
	else:
		return [k]

# Generate a random FVS instance with a minimum FVS size of k.
def generate(k: int) -> MultiGraph:
	# Random number of line segments (contribute nothing).
	num_lines = randint(0, k)

	# Random number of cycles (contribute 1 FVS point each).
	num_cycles = randint(0, k - 1)

	# FVS sizes for the complete graphs.
	complete_graph_fvs_sizes = split(k - num_cycles)

	# Create all the graphs.
	line_graphs = [nx.path_graph(randint(1, k)) for _ in range(num_lines)]
	cycle_graphs = [nx.cycle_graph(randint(3, k + 3)) for _ in range(num_cycles)]
	complete_graphs = [nx.complete_graph(kx + 2) for kx in complete_graph_fvs_sizes]

	# Shuffle a list of connected components.
	graphs = line_graphs + cycle_graphs + complete_graphs
	random.shuffle(graphs)

	# Connect the components without adding cycles.
	g = MultiGraph(graphs[0])
	offset = len(graphs[0])
	for c in graphs[1:]:
		# Last node from the previous connected component.
		prev_last = g.nodes()[-1]

		# Add the connected component. The offset ensures the vertices have new labels.
		g.add_edges_from([(x + offset, y + offset) for (x, y) in c.edges()])

		# First node of the newly added connected component.
		curr_first = offset

		# Add the connecting edge.
		g.add_edge(prev_last, curr_first)

		offset += len(c)

	return g

K_MIN = 2
K_MAX = 8
GRAPHS_PER_K = 20
OUTPUT_FILE = "graphs.pickle"

# Generate a bunch of graphs and write them to disk.
def generate_lots():
	instances = [(generate(k), k) for k in range(K_MIN, K_MAX) for _ in range(GRAPHS_PER_K)]
	with open(OUTPUT_FILE, "wb") as f:
		pickle.dump(instances, f)
