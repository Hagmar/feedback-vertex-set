from fvs import *
from generate import generate

def test_cycle_graphs_ic():
	meta_cycle_graphs(fvs_via_ic)

def test_cycle_graphs_mif():
	meta_cycle_graphs(fvs_via_mif)

def meta_cycle_graphs(alg):
	for i in range(3, 20):
		g = MultiGraph(data=nx.cycle_graph(i))
		fvs = alg(g, 1)
		assert fvs != None
		assert is_fvs(g, fvs)

def test_complete_graphs_ic():
	meta_complete_graphs(fvs_via_ic)

def test_complete_graphs_mif():
	meta_complete_graphs(fvs_via_mif)

def meta_complete_graphs(alg):
	for i in range(3, 14):
		g = MultiGraph(data=nx.complete_graph(i))
		fvs = alg(g, i - 2)
		assert fvs != None
		assert is_fvs(g, fvs)
		assert alg(g, i - 3) == None
		assert alg(g, i - 1) != None

def test_example_ic():
	meta_example(fvs_via_ic)

def test_example_mif():
	meta_example(fvs_via_mif)

def meta_example(alg):
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
	fvs = alg(g, 2)
	assert fvs != None
	assert is_fvs(g, fvs)

def test_generated_ic():
	meta_generated(fvs_via_ic)

def test_generated_mif():
	meta_generated(fvs_via_mif)

def meta_generated(alg):
	for i in range(1, 10):
		for _ in range(1, 10):
			g = generate(i)
			fvs = alg(g, i)
			assert fvs != None
			assert is_fvs(g, fvs)
			assert len(fvs) == i

