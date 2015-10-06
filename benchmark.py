import time

from multiprocessing import Pool

from fvs import *
from generate import *

# Solve the given instance and return the time required to do so.
def time_instance(gk: (MultiGraph, int), algorithm=fvs_via_compression, n=10) -> float:
	g, k = gk
	start = time.process_time()
	for _ in range(0, n):
		algorithm(g, k)
	end = time.process_time()
	return (end - start) / n

# Example benchmark.
if __name__ == "__main__":
	data = [(generate(i), i) for i in range(2, 8)]
	with Pool(1) as p:
		print(p.map(time_instance, data))
