import networkx as nx

from networkx import MultiGraph
from networkx.algorithms.tree import is_forest

def is_fvs(g: MultiGraph, w) -> bool:
	gx = g.copy()
	gx.remove_nodes_from(w)
	return is_forest(gx)

# Delete all vertices of degree 0 or 1.
def reduction1(g: MultiGraph, w: set, k: int) -> (MultiGraph, set, int, bool):
	gx = g.copy()
	changed = False
	for v in gx.nodes():
		if gx.degree(v) <= 1:
			gx.remove_node(v)
			changed = True
	return (gx, w, k, changed)

# If there exists a vertex v in H such that G[W ∪ {v}]
# contains a cycle, then include v in the solution, delete v and decrease the
# parameter by 1. That is, the new instance is (G - {v}, W, k - 1).
def reduction2(g: MultiGraph, w: set, k: int) -> (MultiGraph, set, int, bool):
	gx = g.copy()
	for v in gx.nodes():
		wv = w.copy()
		wv.add(v)
		# Check if G[W ∪ {v}] contains a cycle.
		if not is_forest(gx.subgraph(wv)):
			gx.remove_node(v)
			return (gx, w, k - 1, True)
	return (gx, w, k, False)

# If there is a vertex v ∈ V (H) of degree 2 in G such
# that at least one neighbor of v in G is from V (H), then delete this vertex
# and make its neighbors adjacent (even if they were adjacent before; the graph
# could become a multigraph now).
def reduction3(g: MultiGraph, w: set, k: int) -> (MultiGraph, set, int, bool):
	h = g.copy()
	h.remove_nodes_from(w)
	for v in h.nodes():
		if g.degree(v) == 2:
			# Find neighbors that are also in V(H).
			for u in h[v]:
				# Delete this vertex and make its neighbors adjacent.
				gx = g.copy()
				neighbors = g.neighbors(u)
				gx.remove_node(u)
				for n1 in neighbors:
					for n2 in neighbors:
						if n1 != n2:
							gx.add_edge(n1, n2)
				return (gx, w, k, True)
	return (g, w, k, False)

# Exhaustively apply reductions.
def apply_reductions(g: MultiGraph, w: set, k: int) -> (MultiGraph, set, int):
	gx = g
	wx = w
	kx = k
	while True:
		reduction_applied = False
		for f in [reduction1, reduction2, reduction3]:
			(gx, wx, kx, changed) = f(gx, wx, kx)

			if changed:
				print("[Reductions] Applied {}".format(f.__name__))
				reduction_applied = True

		if not reduction_applied:
			return (gx, wx, kx)

def fvs_compression(g: MultiGraph, k: int) -> bool:
	return False
