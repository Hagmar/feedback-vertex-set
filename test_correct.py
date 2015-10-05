from fvs import *
from generate import generate

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

def test_simple1():
	# This graph has a minimum FVS of size 2.
	g = MultiGraph([
		(1, 2),
		(2, 3),
		(3, 4),
		(4, 5),
		(5, 1),
		(1, 3),
		(1, 4),
		(2, 4)
	])
	fvs = fvs_via_compression(g, 2)
	assert fvs != None
	assert is_fvs(g, fvs)

def test_generated():
	for i in range(1, 10):
		for _ in range(1, 10):
			g = generate(i)
			fvs = fvs_via_compression(g, i)
			assert fvs != None
			assert is_fvs(g, fvs)
			assert len(fvs) == i
