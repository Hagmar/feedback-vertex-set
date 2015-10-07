#!/usr/bin/python3

class Graph():
	def __init__(self):
		self.v = {}

	def __repr__(self):
		return "Graph " + self.v.__repr__()

	def add_vertex(self, vertex):
		if not self.contains_vertex(vertex):
			self.v[vertex] = dict()
		else:
			print("Warning: adding already existing vertex")

	def remove_vertex(self, vertex):
		if self.contains_vertex(vertex):
			for v2 in self.v[vertex]:
				self.v[v2].pop(vertex)
			del self.v[vertex]
		else:
			print("Warning: removing non-existing vertex")

	def remove_vertex_neighbourhood(self, vertex):
		if self.contains_vertex(vertex):
			for v2 in self.v[vertex]:
				self.v[v2].pop(vertex)
				self.remove_vertex(v2)
			del self.v[vertex]
		else:
			print("Warning: removing neighbourhood of non-existant vertex")

	def add_edge(self, v_from, v_to):
		if self.contains_vertex(v_from) and self.contains_vertex(v_to):
			if not self.contains_edge(v_from, v_to):
				self.v[v_from][v_to] = 0
				self.v[v_to][v_from] = 0
			self.v[v_from][v_to] += 1
			if v_from != v_to:
				self.v[v_to][v_from] += 1
		else:
			print("Warning: adding edge between non-existant vertices")

	def remove_edge(self, v_from, v_to):
		if self.contains_vertex(v_from) and self.contains_vertex(v_to):
			if self.contains_edge(v_from, v_to):
				self.v[v_from][v_to] -= 1
				if v_from != v_to:
					self.v[v_to][v_from] -= 1
				if self.v[v_from][v_to] == 0:
					self.v[v_from].pop(v_to)
					if v_from != v_to:
						self.v[v_to].pop(v_from)
			else:
				print("Warning: removing non-existant edge")
		else:
			print("Warning: removing edge from non-existant vertices")

	def contains_vertex(self, vertex):
		return vertex in self.v

	def contains_edge(self, v_from, v_to):
		return (v_to in self.v[v_from]) and (v_from in self.v[v_to])


def fvs_compression(g: Graph, k: int) -> bool:
	return True

def fvs_branch(g: Graph, k: int) -> bool:
	return True
