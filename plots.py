from benchmark import *

import matplotlib.pyplot as plt

def time_vs_n():
	plt.figure(figsize=(5, 3)) # inches
	graphs = load_graphs('graphs.pickle')

	results = time_all(graphs)

	# Lengths on the x axis.
	x_data = [len(g) for g in graphs]

	# Running times on the y axis.
	y_data = [time for (_, time) in results]

	plt.plot(x_data, y_data, 'ro')
	# plt.show()
	plt.savefig('time_vs_n.pgf')

if __name__ == "__main__":
	time_vs_n()
