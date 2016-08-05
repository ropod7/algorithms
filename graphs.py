#!/usr/bin/env/python3
# -*- coding: utf-8 -*-
import os
import random
import unittest
from datetime import datetime

class RContraction(object):                                             # Random Contraction Algorithm

    def __init__(self, lines):
        self._represent_lines(lines)

    def _represent_lines(self, lines):
        self.n = [int(line[0]) for line in lines]                       # generate list of vertices
        self.m = m = []
        for line in lines:
            for item in line[1:]:
                a, b = [int(line[0]), int(item)]
                if [a, b] not in m and [b, a] not in m:
                    m.append([a, b])                                    # generate list of edges
                else:
                    continue                                            # exclude duplicates

    def _contracter(self, n, m):
        index = random.randrange(0, len(m))                             # pick a remaining edge (u,v) uniformly at random
        to_merge = m[index]
        vmin = min(to_merge)
        vmax = max(to_merge)
        del(n[n.index(vmax)])
        k = []
        for edge in m:
            if vmax in edge:
                edge[edge.index(vmax)] = vmin                           # merge (or “contract”) u and v into a single vertex
            k += [edge] if edge[0] != edge[1] else []                   # compare vertices and remove self-loops if equals
        return self._contracter(n, k) if len(n) > 2 else (n, k)         # While there are more than 2 vertices, run recursively,
                                                                        # or return cut represented by final 2 vertices
    def merge(self):
        self.n, self.m = self._contracter(self.n, self.m)
        self.F = len(self.m)                                            # number of edges crossing (A, B)

    def repr_results(self):
        data = 'The minimum Graphs crossing edges: %d \n' % self.F
        return data

class Graph(object):

    def __init__(self, obj):
        self.obj = obj
        self.vertex = False
        self.explored = False
        self.connected = []

    def search(self, vertex):
        self.vertex = vertex
        connected = self.connected
        connected.append(vertex)
        return connected

    def _get_group(self, v):
        for group in self.obj:
            if v is group[0]:
                return group

    def repr_results(self):
        string = 'Explored nodes: %s \n' % self.connected
        return string

class BFS(Graph):                                                       # Breadth First Search algorithm

    def search(self, vertex):
        connected = super(BFS, self).search(vertex)
        queue = [vertex]
        self.dist = 0
        while queue:
            v = queue.pop(0)
            group = self._get_group(v)
            for w in group[1:]:
                if w not in connected:
                    # check distance computation
                    self.dist = 1 if v is vertex else self.dist + 1     # distance starting from 0
                    connected.append(w)
                    queue.append(w)

    def exploreConnected(self):
        self.explored = explored = []
        self.pieces = pieces = 0
        for group in self.obj:
            v = group[0]
            if v not in explored:
                self.search(v)
                explored.extend(sorted(self.connected))
                pieces += 1
        self.pieces = pieces

    def repr_results(self):
        string = super(BFS, self).repr_results()
        if not self.explored:
            string += 'Layers: %d \n' % self.dist
        else:
            string += 'Graph Connected Components: %d \n' % self.pieces
        return string

class DFS(Graph):                                                       # Depth First Search algorithm

    def search(self, vertex):
        connected = super(DFS, self).search(vertex)
        group = self._get_group(vertex)
        for w in group[1:]:
            if w not in connected:
                self.search(w)

    def repr_results(self):
        string = super(DFS, self).repr_results()
        return(string)

if __name__ == '__main__':
    import unittest

    class TestGraphs(unittest.TestCase):
        def setUp(self):

            with open('data/Simplegraphs.txt') as f:
                graph = [list(map(int, line[:-2].split('\t'))) for line in f.readlines()]

            self.connected = (
                    (graph, 17),
                    ([[1, 2, 5, 4, 6], [2, 3, 4, 1], [3, 2, 5], [4, 2, 1, 5], [5, 1, 3, 4], [6, 1]], 1),

                )
            self.disconnected = (
                    [[1, 3, 5], [2, 4], [3, 1, 5], [4, 2], [5, 1, 3, 7, 9], [6, 8, 10], [7, 5, 9], [8, 6, 10], [9, 5, 7], [10, 6, 8]],
            )

        def test_RContraction(self):
            for graph, crossing in self.connected:
                leng = len(graph)
                F = leng
                n = leng//6 if leng//6 > 1 else leng
                for i in range(n):
                    contr = RContraction(graph)
                    contr.merge()
                    F = contr.F if contr.F < F else F
                self.assertEqual(F, crossing)

        def test_BFS_disconnected(self):
            for graph in self.disconnected:
                s = BFS(graph)
                s.exploreConnected()

        def test_BFS_connected(self):
            for graph, crossing in self.connected:
                s = BFS(graph)
                s.search(6)

        def test_DFS(self):
            for graph, crossing in self.connected:
                s = DFS(graph)
                s.search(6)

    suite = unittest.TestLoader().loadTestsFromTestCase(TestGraphs)
    unittest.TextTestRunner(verbosity=2).run(suite)
