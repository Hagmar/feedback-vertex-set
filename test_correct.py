from fvs import *

def test_cycle_graphs():
	for i in range(3, 20):
		g = MultiGraph(data=nx.cycle_graph(i))
		fvs = fvs_via_compression(g, 1)
		assert fvs != None
		assert is_fvs(g, fvs)

def test_complete_graphs():
	for i in range(3, 14):
		g = MultiGraph(data=nx.complete_graph(i))
		fvs = fvs_via_compression(g, i - 2)
		assert fvs != None
		assert is_fvs(g, fvs)
		assert fvs_via_compression(g, i - 3) == None
		assert fvs_via_compression(g, i - 1) != None
