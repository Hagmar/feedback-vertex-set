import time
import multiprocessing as mp

from multiprocessing import Pool

from fvs import *
from generate import *

TEN_MINUTES = 10*60 # seconds

# Solve the given instance and return the time required to do so.
def time_instance(g: MultiGraph, k: int, alg, n=1) -> (set, float):
	start = time.process_time()
	for _ in range(0, n):
		fvs = alg(g, k)
	end = time.process_time()
	return (fvs, (end - start) / n)

# Time a list of instances, waiting at most 10m for any single instance.
# If an instance times out, its result is None.
# graphs: [(MultiGraph, int)]
# returns: [(fvs, time in seconds)]
def time_all(graphs, alg) -> list:
	with Pool(8) as p:
		results = []
		for (g, k) in graphs:
			promise = p.apply_async(func=time_instance, args=(g, k, alg))
			try:
				t = promise.get(TEN_MINUTES)
				results.append(t)
			except mp.TimeoutError:
				results.append(None)

		return results
