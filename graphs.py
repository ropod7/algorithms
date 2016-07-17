# -*- coding: utf-8 -*-

import os
import random

class RContraction(object):                                             # Random Contraction Algorithm

    def __init__(self, lines):
        self.lines = lines
        self.F = 0                                                      # number of edges crossing (A, B)
        self._represent_lines(lines)

    def _represent_lines(self, lines):
        self.n = [int(line[0]) for line in lines]
        self.m = m = []
        for line in lines:
            for item in line[1:]:
                a, b = [int(line[0]), int(item)]
                if [a, b] in m or [b, a] in m:
                    continue
                else:
                    m.append([a, b])

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
        self.F = len(self.m)

    def repr_results(self):
        data = 'Minimum cuts is: {0}'.format(self.F)
        return data

if __name__ == '__main__':
    with open('data/Simplegraphs.txt') as f:
        lines = [line[:-2].split('\t') for line in f.readlines()]
    # 0 position of every list is a vertex label, that form an edge with followings
    #lines = [[1, 2, 5, 4], [2, 3, 4, 1], [3, 2, 5], [4, 2, 1, 5], [5, 1, 3, 4],]   
    cuts = 0
    for i in range(10):
        rc = RContraction(lines)
        rc.merge()
        if rc.F < cuts:
            cuts = rc.F
            cedges = rc.m
            strres = rc.repr_results()
        elif i == 0:
            cuts = rc.F
            cedges = rc.m
            strres = rc.repr_results()

    print(strres)
    print(cedges)
