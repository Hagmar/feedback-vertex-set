import os
import sys
from benchmark import *

def main():
	# Create output dir.
	os.makedirs('results', mode=0o775, exist_ok=True)

	sys.setrecursionlimit(10000)

	# Load data.
	data_sets = [
		("tiny", "data/00_tiny.graphs"),
		("small", "data/01_small_n.graphs"),
		("medium", "data/02_medium_n.graphs"),
		("large", "data/03_large_n.graphs"),
		("k12_large", "data/04_k12_large.graphs")
	]

	# Set of tests to run.
	run = {"tiny", "k12_large"}

	for (name, filename) in data_sets:
		if name not in run:
			continue

		print("Now processing:", name)
		graphs = from_disk(filename)

		ic_results = time_all(graphs, alg=fvs_via_ic)
		to_disk(ic_results, 'results/{}_ic.results'.format(name))

		mif_results = time_all(graphs, alg=fvs_via_mif)
		to_disk(mif_results, 'results/{}_mif.results'.format(name))

		del ic_results
		del mif_results
		del graphs

if __name__ == "__main__":
	main()
