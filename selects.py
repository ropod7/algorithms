#!/usr/bin/env/python3

# In this script case using Divide & Conquer paradigm, to define recursive
# tree algorithm in following tasks:
# 1. Getting ith order statistics in unsorted list object using:
#   - Randomized Selection algorithm
#   - Deterministic Selection algorithm (the median of medians)

import os
import random

from sorts import QuickSort, MergeSort

# the running time is O(n)
class RSelect(QuickSort):                                               # Randomized Selection
    """Getting ith order statistics in unsorted list object using
    Randomized Selection algorithm"""

    def select(self, ith):
        ith += 1
        _assertions = ['Order statistic must to be an integer',
                       'iterable object much shorter']
        assert isinstance(ith, int), _assertions[0]
        assert ith <= len(self.obj), _assertions[1]
        self.choice = 'rand'
        self.ith = ith
        self.order_stat = self._recursiveSelect(self.obj, ith)
        return self.order_stat

    def _partitioning(self, obj, n, i):
        obj, j = self._partitionSort(obj, n)
        if j is i-1:  return obj[j]
        elif j > i-1: return self._recursiveSelect(obj[:j], i)
        else: return self._recursiveSelect(obj[j+1:], i-1-j)

    def _recursiveSelect(self, obj, i):
        n = len(obj)
        if n is 1: return obj[0]
        obj = self._choose_pivot(obj)
        return self._partitioning(obj, n, i)

# the running time is linear O(n)
class DSelect(RSelect):                                                 # Deterministic Selection
    """Getting ith order statistics in unsorted list object using
    Deterministic Selection algorithm (the median of medians)"""

    def _get_median(self, obj):
        lenobj = len(obj)
        obj = MergeSort(obj).sort()
        half = lenobj // 2
        if lenobj >= 3:
            return obj[half] if lenobj % 2 else obj[half-1]             # if odd return obj[half] as pivot
        else:
            return min(obj) if lenobj == 2 else obj[0]

    def _choose_pivot(self, obj):
        ns = 5                                                          # number of length each part
        if len(obj) < ns: return self._get_median(obj)                  # return pivot as median of medians
        parts = [obj[i:i+ns] for i in range(0, len(obj), ns)]           # logically break list into n/5 groups of size 5 each
        medians = list(map(self._get_median, parts))                    # get medians of each input list
        return self._choose_pivot(medians)                              # recursively compute median of medians and return pivot

    def _recursiveSelect(self, obj, i):
        n = len(obj)
        pivot = self._choose_pivot(obj)
        index = obj.index(pivot)
        obj[0], obj[index] = self._swap(obj[0], obj[index])             # place pivot to 0 position
        return self._partitioning(obj, n, i)

if __name__ == '__main__':
    import unittest

    class TestSelects(unittest.TestCase):
        def setUp(self):
            with open('data/IntegerArray.txt', 'r') as f:
                self.arrs = (
                    list(map(int, f.readlines())),
                    [16,1,19,5,8,18,2,6,9,15,4,7,3,17,11,14,10,12,13,22,48],
                    [10, 8, 2, 5],
                    [random.randrange(2**32) for i in range(2**16)],    # list of randomized generated integers
                )

        def runForloop(self, cls):
            for arr in self.arrs:
                lenarr = len(arr)
                s = cls(arr)
                order_stat = s.select(lenarr//2)
                self.assertEqual(order_stat, sorted(arr)[lenarr//2])

        def test_RSelect(self):
            self.runForloop(RSelect)

        def test_DSelect(self):
            self.runForloop(DSelect)

    suite = unittest.TestLoader().loadTestsFromTestCase(TestSelects)
    unittest.TextTestRunner(verbosity=2).run(suite)
