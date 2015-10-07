import itertools
import networkx as nx
import networkx.algorithms.components.connected as nxc
import networkx.algorithms.cycles as cyc

from networkx import MultiGraph
from networkx.algorithms.tree import is_forest

# Original (unused) code for G - W.
def graph_minus_slow(g: MultiGraph, w: set) -> MultiGraph:
	gx = g.copy()
	gx.remove_nodes_from(w)
	return gx

# Optimised code for G - W (yields an approx 2x speed-up).
def graph_minus(g: MultiGraph, w: set) -> MultiGraph:
	gx = MultiGraph()
	for (n1, n2) in g.edges():
		if n1 not in w and n2 not in w:
			gx.add_edge(n1, n2)
	for n in g.nodes():
		if n not in w:
			gx.add_node(n)
	return gx

def is_fvs(g: MultiGraph, w) -> bool:
	h = graph_minus(g, w)
	return ((len(h) == 0) or is_forest(h))

def is_independent_set(g: MultiGraph, f: set) -> bool:
	for edge in itertools.combinations(f, 2):
		if g.has_edge(edge[0], edge[1]):
			return False
	return True

# Note: Reduction functions return (k, new, changed) and mutate their graph arguments (G and H)!

# Delete all vertices of degree 0 or 1 (as they can't be part of any cycles).
def reduction1(g: MultiGraph, w: set, h: MultiGraph, k: int) -> (int, int, bool):
	changed = False
	for v in g.nodes():
		if g.degree(v) <= 1:
			g.remove_node(v)
			h.remove_nodes_from([v])
			changed = True
	return (k, None, changed)

# If there exists a vertex v in H such that G[W ∪ {v}]
# contains a cycle, then include v in the solution, delete v and decrease the
# parameter by 1. That is, the new instance is (G - {v}, W, k - 1).
# If v introduces a cycle, it must be part of X as none of the vertices in W
# will be available to neutralise this cycle.
def reduction2(g: MultiGraph, w: set, h: MultiGraph, k: int) -> (int, int, bool):
	for v in h.nodes():
		# Check if G[W ∪ {v}] contains a cycle.
		if not is_forest(g.subgraph(w.union({v}))):
			g.remove_node(v)
			h.remove_nodes_from([v])
			return (k - 1, v, True)
	return (k, None, False)

# If there is a vertex v ∈ V (H) of degree 2 in G such
# that at least one neighbor of v in G is from V (H), then delete this vertex
# and make its neighbors adjacent (even if they were adjacent before; the graph
# could become a multigraph now).
def reduction3(g: MultiGraph, w: set, h: MultiGraph, k: int) -> (int, int, bool):
	for v in h.nodes():
		if g.degree(v) == 2:
			# If v has a neighbour in H, short-curcuit it.
			if len(h[v]) >= 1:
				# Delete v and make its neighbors adjacent.
				[n1, n2] = g.neighbors(v)
				g.remove_node(v)
				g.add_edge(n1, n2)
				# Update H accordingly.
				h.remove_nodes_from([v])
				if n1 not in w and n2 not in w:
					h.add_edge(n1, n2)
				return (k, None, True)
	return (k, None, False)

# Exhaustively apply reductions.
# This function owns G.
def apply_reductions(g: MultiGraph, w: set, k: int) -> (int, set):
	# Current H.
	h = graph_minus(g, w)

	# Set of vertices included in the solution as a result of reductions.
	x = set()
	while True:
		reduction_applied = False
		for f in [reduction1, reduction2, reduction3]:
			(k, solx, changed) = f(g, w, h, k)

			if changed:
				reduction_applied = True
				if solx != None:
					x.add(solx)

		if not reduction_applied:
			return (k, x)

# Given a graph G and a FVS W of size at least (k + 1), is it possible to construct
# a FVS X of size at most k using only the vertices of G - W?
# This function owns G and can mutate it freely.
def fvs_disjoint(g: MultiGraph, w: set, k: int) -> set:
	# Check that G[W] is a forest.
	# If it isn't, then a solution X not using W can't remove W's cycles.
	if not is_forest(g.subgraph(w)):
		return None

	# Apply reductions exhaustively.
	k, soln_redux = apply_reductions(g, w, k)

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
	assert x is not None

	# Branch.
	# G is copied in the left branch (as it is modified), but passed directly in the right.
	soln_left = fvs_disjoint(graph_minus(g, {x}), w, k - 1)

	if soln_left is not None:
		return soln_redux.union(soln_left).union({x})

	soln_right = fvs_disjoint(g, w.union({x}), k)

	if soln_right is not None:
		return soln_redux.union(soln_right)

	return None

# Given a graph G and an FVS Z of size (k + 1), construct an FVS of size at most k.
# Return `None` if no such solution exists.
def ic_compression(g: MultiGraph, z: set, k: int) -> MultiGraph:
	assert (len(z) == k + 1)
	# i in {0 .. k}
	for i in range(0, k + 1):
		for xz in itertools.combinations(z, i):
			x = fvs_disjoint(graph_minus(g, xz), z.difference(xz), k - i)
			if x is not None:
				return x.union(xz)
	return None

# Given a graph G and an integer k, construct an FVS of size at most k using
# the iterative compression based algorithm from Parametrzed Algorithms 4.3.1
def fvs_via_ic(g: MultiGraph, k: int) -> set:
	if len(g) <= k + 2:
		return set(g.nodes()[:k])

	# Construct a trivial FVS of size k + 1 on the first k + 3 vertices of G.
	nodes = g.nodes()

	# The set of nodes currently under consideration.
	node_set = set(nodes[:(k + 2)])

	# The current best solution, of size (k + 1) before each compression step,
	# and size <= k at the end.
	soln = set(nodes[:k])

	for i in range(k + 2, len(nodes)):
		soln.add(nodes[i])
		node_set.add(nodes[i])

		if len(soln) < k + 1:
			continue

		assert (len(soln) == (k + 1))
		assert (len(node_set) == (i + 1))

		new_soln = ic_compression(g.subgraph(node_set), soln, k)

		if new_soln is None:
			return None

		soln = new_soln
		assert (len(soln) <= k)

	return soln

def compress(g: MultiGraph, t: set, compressed_node) -> MultiGraph:
	gx = g.copy()
	if not t:
		return gx

	tx = t
	if compressed_node in tx:
		tx = t.copy()
		tx.remove(compressed_node)
	gx.add_node(compressed_node)

	for node in tx:
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

def generalized_degree(g: MultiGraph, f: set, active_node, node) -> (int, set):
	assert g.has_node(node), "Calculating gd for node which is not in g!"

	k = set(g.neighbors(node))
	k.remove(active_node)
	k = k.intersection(f)

	gx = compress(g, k, node)

	neighbors = gx.neighbors(node)
	neighbors.remove(active_node)

	return (len(neighbors), neighbors)

def mif_main(g: MultiGraph, f: set, t, k: int) -> set:
	k_set = k != None
	new_k1 = new_k2 = None
	if k_set and k > g.order():
		return None
	if f == g.nodes() or (k_set and k <= 0):
		return f
	if (not f):
		g_degree = g.degree()
		g_max_degree_node = max(g_degree, key=lambda n: g_degree[n])
		if (g_degree[g_max_degree_node] <= 1):
			return set(g.nodes())
		else:
			fx = f.copy()
			fx.add(g_max_degree_node)
			gx = g.copy()
			gx.remove_node(g_max_degree_node)
			if k_set:
				new_k1 = k-1
				new_k2 = k
			mif_set1 = mif_preprocess_1(g, fx, t, new_k1)
			mif_set2 = mif_preprocess_1(gx, f, t, new_k2)
			if not mif_set1:
				return mif_set2
			elif not mif_set2:
				return mif_set1
			else:
				return max(mif_set1, mif_set2, key=len)

	# Set t as active vertex
	if t == None or not t in f:
		t = next(iter(f))

	gd_over_3 = None
	gd_2 = None
	for v in g.neighbors_iter(t):
		(gd_v, gn_v) = generalized_degree(g, f, t, v)
		if gd_v <= 1:
			f.add(v)
			if k_set:
				new_k1 = k-1
			return mif_preprocess_1(g, f, t, new_k1)
		elif gd_v >= 3:
			gd_over_3 = v
		else:
			gd_2 = (v, gn_v)
	if gd_over_3 != None:
		# Cannot simply use "if gd_over_3" because v might be 0
		fx = f.copy()
		fx.add(gd_over_3)
		gx = g.copy()
		gx.remove_node(gd_over_3)
		if k_set:
			new_k1 = k-1
			new_k2 = k
		mif_set1 = mif_preprocess_1(g, fx, t, new_k1)
		mif_set2 = mif_preprocess_1(gx, f, t, new_k2)
		if not mif_set1:
			return mif_set2
		elif not mif_set2:
			return mif_set1
		else:
			return max(mif_set1, mif_set2, key=len)
	elif gd_2 != None:
		(v, gn) = gd_2
		fx1 = f.copy()
		fx2 = f.copy()
		fx1.add(v)
		for n in gn:
			fx2.add(n)
		gx = g.copy()
		gx.remove_node(v)
		if k_set:
			new_k1 = k-2
			new_k2 = k-1
		try:
			cyc.find_cycle(gx.subgraph(fx2))
			mif_set1 = None
		except:
			mif_set1 = mif_preprocess_1(gx, fx2, t, new_k1)
		mif_set2 = mif_preprocess_1(g, fx1, t, new_k2)
		if not mif_set1:
			return mif_set2
		elif not mif_set2:
			return mif_set1
		else:
			return max(mif_set1, mif_set2, key=len)
	return None

def mif_preprocess_2(g: MultiGraph, f: set, active_v, k: int) -> set:
	mif_set = set()
	while not is_independent_set(g, f):
		mif_set = mif_set.union(f)
		for component in nxc.connected_components(g.subgraph(f)):
			if len(component) > 1:
				if active_v in component:
					active_v = component.pop()
					compressed_node = active_v
				else:
					compressed_node = component.pop()
				g = compress(g, component, compressed_node)
				f = f.intersection(g.nodes())
				# Maybe faster with
				# f = f.difference(component)
				# f.add(compressed_node)
				mif_set = mif_set.union(component)
				break
	mif_set2 = mif_main(g, f, active_v, k)
	if mif_set2:
		mif_set = mif_set2.union(mif_set)
	if k == None or len(mif_set) >= k:
		return mif_set
	return None

def mif_preprocess_1(g: MultiGraph, f: set, active_v, k: int) -> set:
	if nxc.number_connected_components(g) >= 2:
		mif_set = set()
		for component in nxc.connected_components(g):
			f_i = component.intersection(f)
			gx = g.subgraph(component)
			component_mif_set = mif_preprocess_2(gx, f_i, active_v, None)
			if component_mif_set:
				mif_set = mif_set.union(component_mif_set)
				if k != None:
					k -= (len(component_mif_set) - len(f_i))
					if k <= 0:
						return mif_set
		if k == None or len(mif_set) >= k:
			return mif_set
		return None
	return mif_preprocess_2(g, f, active_v, k)

def mif(g: MultiGraph, k=None) -> set:
	mif_set = mif_preprocess_1(g, set(), None, k)
	if k != None and mif_set:
		if len(mif_set) < k:
			mif_set = None
	return mif_set

def fvs_via_mif(g: MultiGraph, k: int) -> set:
	mif_set = mif(g, g.order()-k)
	if mif_set:
		nodes = set(g.nodes())
		mif_set = nodes.difference(mif_set)
	return mif_set
