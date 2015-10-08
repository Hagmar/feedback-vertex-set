# Generate and solve a random instance using the iterative compression algorithm.

from fvs import *
from generate import *
from benchmark import *

def main():
	k = 10
	g = generate(k)

	print("Graph parameters:\n")
	print("|V| = {}\n".format(len(g)))
	print("E = {}\n".format(g.edges()))
	print("|E| = {}\n".format(len(g.edges())))

	print("Algorithm: iterative compression with k = {}.".format(k))
	fvs, time = time_instance(g, k, alg=fvs_via_ic, n=1)

	print("\nDone!")
	print("FVS = {} with size {}.".format(fvs, len(fvs)))

	print("Computation took {:.3f} seconds.".format(time))

if __name__ == "__main__":
	main()
