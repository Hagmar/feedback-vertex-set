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
def plot_time_vs_k(data, colour, annotate=set()):
	xs = k_values(data)
	ys = time_values(data)

	fig, ax = plt.subplots()
	ax.scatter(xs, ys, c=colour)

	plt.xlabel("Minimum FVS size, $k$")
	plt.ylabel("Running time [seconds]")
	plt.xlim([0, max(xs) + 1])
	plt.ylim(ymin=0)

	# Annotate some k values with their n values.
	for i, n in enumerate(n_values(data)):
		if xs[i] not in annotate:
			continue
		ax.annotate(n, (xs[i], ys[i]))

	plt.show()

# Make a plot of running time against n.
def plot_time_vs_n(data, colour):
	xs = n_values(data)
	ys = time_values(data)

	fig, ax = plt.subplots()
	ax.scatter(xs, ys, c=colour)

	plt.xlabel("Number of vertices, $n$")
	plt.ylabel("Running time [seconds]")
	plt.xlim([0, max(xs) + 1])
	plt.ylim(ymin=0)

	plt.show()

# Plot the time for yes instances minus the time for no instances.
def plot_yes_no_difference(yes_data, no_data, colour):
	# Use the true k values on the x axis.
	xs = k_values(yes_data)
	# Time differences on the y axis.
	ys = [yes - no for ((_, _, _, yes),(_, _, _, no)) in zip(yes_data, no_data)]

	fig, ax = plt.subplots()
	ax.scatter(xs, ys, c=colour)

	plt.xlabel("Minimum FVS size, $k$")
	plt.ylabel("Time difference (yes - no) [seconds]")

	plt.show()
