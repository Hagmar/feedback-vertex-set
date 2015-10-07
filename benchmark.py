import time

from multiprocessing import Pool

from fvs import *
from generate import *

# Solve the given instance and return the time required to do so.
def time_instance(gk: (MultiGraph, int), algorithm=fvs_via_compression, n=10) -> (set, float):
	g, k = gk
	start = time.process_time()
	for _ in range(0, n):
		fvs = algorithm(g, k)
	end = time.process_time()
	return (fvs, (end - start) / n)

# Time a list of instances.
# graphs: (MultiGraph, int)
# returns: (fvs, time in seconds)
def time_all(graphs) -> list:
	with Pool(1) as p:
		return p.map(time_instance, graphs)
