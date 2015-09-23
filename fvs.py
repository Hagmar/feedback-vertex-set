import networkx as nx

from networkx import MultiGraph
from networkx.algorithms.tree import is_forest

def is_fvs(g: MultiGraph, w) -> bool:
	gx = g.copy()
	gx.remove_nodes_from(w)
	return is_forest(gx)

def reduction1(g: MultiGraph) -> MultiGraph:
	gx = g.copy()
	for v in gx.nodes():
		if gx.degree(v) <= 1:
			gx.remove_node(v)
	return gx

def reduction2(g: MultiGraph, w: set, k: int) -> (MultiGraph, set, int):
	gx = g.copy()
	for v in gx.nodes():
		wv = w.copy()
		wv.add(v)
		if is_forest(gx.subgraph(wv)):
			gx.remove_node(v)
			return (gx, w, k - 1)
	return (gx, w, k)

def fvs_compression(g: MultiGraph, k: int) -> bool:
	return False
