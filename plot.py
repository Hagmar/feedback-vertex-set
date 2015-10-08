import matplotlib.pyplot as plt

from benchmark import *

# Combine a set of graphs with a results file to create data suitable for plotting.
#
# Example:
# ic_plottable, ic_timed_out = combine_results('data/01_small_n.graphs', 'results/michael-server/small_ic.results')
def combine_results(graph_file, results_file) -> (list, list):
	graphs = from_disk(graph_file)
	results = from_disk(results_file)

	plottable = [(g, k, res[0], res[1]) for ((g, k), res) in zip(graphs, results) if res is not None]
	timed_out = [(g, k) for ((g, k), res) in zip(graphs, results) if res is None]

	return (plottable, timed_out)

def time_values(data):
	return [t for (_, _, _, t) in data]

def k_values(data):
	return [k for (_, k, _, _) in data]

def n_values(data):
	return [len(g) for (g, _, _, _) in data]

# Make a plot of running time against k.
def plot_time_vs_k(data, annotate=set()):
	x_data = k_values(data)
	y_data = time_values(data)
	n_data = n_values(data)

	fig, ax = plt.subplots()
	ax.scatter(x_data, y_data)

	plt.xlabel("Minimum FVS size, $k$")
	plt.ylabel("Running time [s]")

	# Annotate some k values with their n values.
	for i, n in enumerate(n_values):
		if x_data[i] not in annotate:
			continue
		ax.annotate(n, (x_data[i], y_data[i]))

	plt.show()

# Make a plot of running time against n.
def plot_time_vs_n(data):
	x_data = n_values(data)
	y_data = time_values(data)

	plt.plot(x_data, y_data, "o")
	plt.show()
