#!/usr/bin/python

class Graph():
	def __init__(self):
		self.v = {}

	def add_vertex(self, vertex):
		if not vertex in self.v:
			self.v[vertex] = set()
		else:
			print("Warning: adding already existing vertex")
	
	def remove_vertex(self, vertex):
		if vertex in self.v:
			for v2 in self.v[vertex]:
				self.v[v2].remove(vertex)
			del self.v[vertex]
		else:
			print("Warning: removing non-existing vertex")
	
	def add_edge(self, v_from, v_to):
		if v_from in self.v and v_to in self.v:
			if v_from != v_to:
				self.v[v_from].add(v_to)
				self.v[v_to].add(v_from)
			else:
				print("Warning: adding edge from vertex to self")
		else:
			print("Warning: adding edge between non-existant vertices")
	
	def remove_edge(self, v_from, v_to):
		if v_from in self.v and v_to in self.v:
			if (v_to in self.v[v_from]) and (v_from in self.v[v_to]):
				self.v[v_from].remove(v_to)
				self.v[v_to].remove(v_from)
			else:
				print("Warning: removing non-existant edge")
		else:
			print("Warning: removing edge from non-existant vertices")
