import itertools
import networkx as nx
import networkx.algorithms.components.connected as nxc
import networkx.algorithms.cycles as cyc

from networkx import MultiGraph
from networkx.algorithms.tree import is_forest

def graph_minus(g: MultiGraph, w: set) -> MultiGraph:
	gx = g.copy()
	gx.remove_nodes_from(w)
	return gx

def is_fvs(g: MultiGraph, w) -> bool:
	h = graph_minus(g, w)
	return ((len(h) == 0) or is_forest(h))

# Note: All reduction functions return (G, W, k) followed by any element added to the solution
# as part of the reduction and a boolean that indicates whether the input instance was changed.

# Delete all vertices of degree 0 or 1 (as they can't be part of any cycles).
def reduction1(g: MultiGraph, w: set, k: int) -> (MultiGraph, set, int, int, bool):
	gx = g.copy()
	changed = False
	for v in gx.nodes():
		if gx.degree(v) <= 1:
			gx.remove_node(v)
			changed = True
	return (gx, w, k, None, changed)

# If there exists a vertex v in H such that G[W ∪ {v}]
# contains a cycle, then include v in the solution, delete v and decrease the
# parameter by 1. That is, the new instance is (G - {v}, W, k - 1).
# If v introduces a cycle, it must be part of X as none of the vertices in W
# will be available to neutralise this cycle.
def reduction2(g: MultiGraph, w: set, k: int) -> (MultiGraph, set, int, int, bool):
	h = graph_minus(g, w)
	for v in h.nodes():
		wv = w.copy()
		wv.add(v)
		# Check if G[W ∪ {v}] contains a cycle.
		if not is_forest(g.subgraph(wv)):
			gx = g.copy()
			gx.remove_node(v)
			return (gx, w, k - 1, v, True)
	return (g, w, k, None, False)

# If there is a vertex v ∈ V (H) of degree 2 in G such
# that at least one neighbor of v in G is from V (H), then delete this vertex
# and make its neighbors adjacent (even if they were adjacent before; the graph
# could become a multigraph now).
def reduction3(g: MultiGraph, w: set, k: int) -> (MultiGraph, set, int, int, bool):
	h = graph_minus(g, w)
	for v in h.nodes():
		if g.degree(v) == 2:
			# If v has a neighbour in H, short-curcuit it.
			if len(h[v]) >= 1:
				# Delete v and make its neighbors adjacent.
				gx = g.copy()
				[n1, n2] = g.neighbors(v)
				gx.remove_node(v)
				gx.add_edge(n1, n2)
				return (gx, w, k, None, True)
	return (g, w, k, None, False)

# Exhaustively apply reductions.
def apply_reductions(g: MultiGraph, w: set, k: int) -> (MultiGraph, set, int, set):
	gx = g
	wx = w
	kx = k
	# Set of vertices included in the solution as a result of reductions.
	x = set()
	while True:
		reduction_applied = False
		for f in [reduction1, reduction2, reduction3]:
			(gx, wx, kx, solx, changed) = f(gx, wx, kx)

			if changed:
				reduction_applied = True
				if solx != None:
					x.add(solx)

		if not reduction_applied:
			return (gx, wx, kx, x)

# Given a graph G and a FVS W of size (k + 1), is it possible to construct
# a FVS X of size at most k using only the vertices of G - W?
def fvs_disjoint(g: MultiGraph, w: set, k: int) -> set:
	# Check that G[W] is a forest.
	# If it isn't, then a solution X not using W can't remove W's cycles.
	if not is_forest(g.subgraph(w)):
		return None

	# Apply reductions exhaustively.
	g, w, k, soln_redux = apply_reductions(g, w, k)

	# If k becomes negative, it indicates that the reductions included
	# more than k vertices, hence no solution of size <= k exists.
	if k < 0:
		return None

	# If G has been reduced to nothing and k is >= 0 then the solution generated by the reductions
	# is already optimal.
	if len(g) == 0:
		return soln_redux

	# Find an x in H of degree at most 1.
	h = graph_minus(g, w)
	x = None
	for v in h.nodes():
		if h.degree(v) <= 1:
			x = v
			break
	assert x != None

	# Branch.
	# G is copied in the left branch (as it is modified), but passed directly in the right.
	soln_left = fvs_compression(graph_minus(g, {x}), w, k - 1)

	if soln_left != None:
		return soln_redux.union(soln_left)

	soln_right = fvs_compression(g, w.union({x}), k)

	if soln_right != None:
		return soln_redux.union(soln_right)

	return None

# Given a graph G and an FVS Z of size (k + 1), construct an FVS of size at most k.
# Return `None` if no such solution exists.
def fvs_compression(g: MultiGraph, z: set, k: int) -> MultiGraph:
	# i in {0 .. k}
	for i in range(0, k + 1):
		for xz in itertools.combinations(z, i):
			xz = set(xz)
			x = fvs_disjoint(graph_minus(g, xz), z.difference(xz), k - i)
			if x != None:
				return x.union(xz)
	return None

# Given a graph G and an integer k, construct an FVS of size at most k.
def fvs_via_compression(g: MultiGraph, k: int) -> set:
	if len(g) <= k + 2:
		return set(g.nodes()[:k])

	# Construct a trivial FVS of size k + 1 on the first k + 3 vertices of G.
	nodes = g.nodes()

	# The set of nodes currently under consideration.
	node_set = set(nodes[:(k + 2)])

	# The current best solution, of size <= (k + 1) at the start of each iteration,
	# and size <= k at the end.
	soln = set(nodes[:k])

	for i in range(k + 2, len(nodes)):
		soln.add(nodes[i])
		node_set.add(nodes[i])

		assert (len(soln) <= (k + 1))
		assert (len(node_set) == (i + 1))

		new_soln = fvs_compression(g.subgraph(node_set).copy(), soln, k)

		if new_soln == None:
			return None

		soln = new_soln
		assert (len(soln) <= k)

	return soln

def compress(g: MultiGraph, t: set, compressed_node) -> MultiGraph:
	gx = g.copy()
	if not t:
		return gx

	if compressed_node in t:
		t.remove(compressed_node)
	gx.add_node(compressed_node)

	for node in t:
		for edge in gx.edges(node):
			if edge[0] == node:
				node_2 = edge[1]
			else:
				node_2 = edge[0]
			if not (node_2 in t or node_2 == compressed_node):
				gx.add_edge(compressed_node, node_2)
		gx.remove_node(node)

	remove = set()
	for node in gx.adj[compressed_node]:
		if len(gx.adj[compressed_node][node]) >= 2:
			# Using a set to remove to avoid messing up iteration of adj
			remove.add(node)

	for node in remove:
		gx.remove_node(node)

	return gx

# TODO
def generalized_degree(g: MultiGraph, f: set, active_node, node) -> (int, set):
	assert g.has_node(node), "Calculating gd for node which is not in g!"

	k = set(g.neighbors(node))
	k.remove(active_node)
	k = k.intersection(f)

	gx = compress(g, k, node)

	neighbors = gx.neighbors(node)
	neighbors.remove(active_node)

	return (len(neighbors), neighbors)

def mif_main(g: MultiGraph, f: set) -> int:
	if f == g.nodes():
		return len(g)
	if (not f):
		g_degree = g.degree()
		g_max_degree_node = max(g_degree, key=lambda n: g_degree[n])
		if (g_degree[g_max_degree_node] <= 1):
			return len(g)
		else:
			fx = f.copy()
			fx.add(g_max_degree_node)
			gx = g.copy()
			gx.remove_node(g_max_degree_node)
			return max(mif_main(g, fx), mif_main(gx, f))
	# Set t as active vertex
	t = g.nodes[0]

	gd_over_3 = None
	gd_2 = None
	for v in g.neighbors_iter(t):
		(gd_v, gn_v) = generalized_degree(g, f, t, v)
		if gd_v <= 1:
			f.add(v)
			return mif_main(g, f)
		elif gd_v >=3:
			gd_over_3 = v
		else:
			gd_2 = (v, gn_v)
	if gd_over_3 != None:
		# Cannot simply use "if gd_over_3" because v might be 0
		fx = f.copy()
		fx.add(gd_over_3)
		gx = g.copy()
		gx.remove_node(gd_over_3)
		return max(mif_main(g, fx), mif_main(gx, f))
	elif gd_2 != None:
		(v, gn) = gd_2
		fx1 = f.copy()
		fx2 = f.copy()
		fx1.add(v)
		for n in gn:
			fx2.add(n)
		gx = g.copy()
		gx.remove(v)
		try:
			cyc.find_cycle(gx.subgraph(fx2))
			gx_mif = 0
		except:
			gx_mif = mif_main(gx, fx2)
		return max(mif_main(g, fx1), gx_mif)
	print("Error - this shouldn't be possible")
	return 0

def mif_preprocess_2(g: MultiGraph, f: set) -> int:
	if 

def mif_preprocess_1(g: MultiGraph, f: set) -> int:
	if nxc.number_connected_components(g) >= 2:
		mif_size = 0
		for component in nxc.connected_components(g):
			nodes = component.nodes()
			f_i = nodes.intersection(f)
			mif_size += mif_preprocess_2(component, f_i)
		return mif_size
	return mif_preprocess_2(g, f)

def fvs_via_mif(g: MultiGraph, f: set) -> int:
	if nxc.number_connected_components(g) >= 2:
		fvs_size = 0
		for component in nxc.connected_components(g):
			nodes = component.nodes()
			f_i = nodes.intersection(f)
			fvs_size += fvs_via_mif(component, f_i)

