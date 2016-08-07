#!/usr/bin/env/python3

# In this script case using Divide & Conquer paradigm, to define recursive
# tree algorithm in following tasks:
# 1. Sort list objects using MergeSort and QuickSort algorithms
# 2. Count number of SplitInversions in unsorted list object using MergeSort
# 3. Count number of comparsions in unsorted list object using QuickSort
#   - Four types of pivot choices for all recursively partitioned subobjects:
#       * as first element
#       * as 'median-of-three' element
#       * as last element
#       * as randomly choosen element
# 4. Getting ith order statistics in unsorted list object using:
#   - Randomized Selection algorithm
#   - Deterministic Selection algorithm (the median of medians)

import os
import random
from datetime import datetime

class BaseSort(object):

    def __init__(self, obj):
        self.obj = obj
        self.over = max(obj) + 1                                        # to define over value in merge sort

    def sort(self):
        obj = self.obj
        return self._recursiveSort(obj) if len(obj) > 1 else obj

    def _recursive_comb(self, a, b):
        a = self._recursiveSort(a) if len(a) > 1 else a                 # recursive call for 1st half
        b = self._recursiveSort(b) if len(b) > 1 else b                 # recursive call for 2nd half
        return a, b

# the running time is O(nlog(n))
class MergeSort(BaseSort):

    def _get_value(self, obj, i):
        return obj[i] if i != len(obj) else self.over

    def _merge(self, a, b, lenl, si):
        output = []
        i = j = 0
        for k in range(lenl):
            A = self._get_value(a, i)
            B = self._get_value(b, j)
            if A < B:
                output.append(A)
                i += 1
            else:
                output.append(B)
                j += 1
                if si: self.inversions += len(a) - i
        return output

    def _split(self, obj, n):
        return obj[:n//2], obj[n//2:]

    def _recursiveSort(self, obj, si=False):
        n = len(obj)
        if n is 1: return 0
        a, b = self._split(obj, n)
        a, b = self._recursive_comb(a, b)
        d = self._merge(a, b, n, si)
        return d

class SplitInversions(MergeSort):
    inversions = 0

    def _recursiveSort(self, *args):
        return super(SplitInversions, self)._recursiveSort(*args, si=True)

# the running time is O(nlog(n))
# can't apply Master Method [random, unbalanced subproblems]
class QuickSort(BaseSort):
    comparsions = 0

    def sort(self, pivot='rand'):
        """Four types of pivot choice for all recursively partitioned
        subobjects:
        1. as first element: s.sort(pivot='first')
        2. as 'median-of-three' element: s.sort(pivot='median')
        3. as last element: s.sort(pivot='last')
        4. as randomly choosen element: s.sort([pivot='rand'])"""

        choices = ('first', 'median', 'last', 'rand')
        assert pivot in choices
        self.choice = pivot
        return self._recursiveSort(self.obj)

    def _swap(self, item0, item1):
        return item1, item0

    def _get_median(self, obj):
        lenobj = len(obj)
        half = lenobj // 2
        if lenobj >= 3:
            odd = lenobj % 2
            left, right = obj[0],  obj[-1]
            mid = obj[half] if odd else obj[half-1]
            s = {left, mid, right}                                      # define set 'of-three'
            median = [i for i in s - {min(s), max(s)}][0]               # get 'median-of-three'
        else:
            median = min(obj)
        return obj.index(median)                                        # return index of median

    def _choose_pivot(self, obj):
        choice = self.choice
        lenobj = len(obj)
        if choice is 'median':
            index = self._get_median(obj)
        elif choice is 'last':
            index = -1
        elif choice is 'rand':
            index = random.randrange(0, lenobj)
            index = index if index else 1
        obj[0], obj[index] = self._swap(obj[0], obj[index])             # place pivot to the 0 pos
        return obj

    def _recursiveSort(self, obj):
        n = len(obj)
        if n is 1: return
        choice = self.choice
        obj = obj if choice is 'first' else self._choose_pivot(obj)     # every pivot compared in input array exactly once
        obj, index = self._partitionSort(obj, n)
        a, b = obj[:index], obj[index+1:]                               # split partitions around pivot
        obj[:index], obj[index+1:] = self._recursive_comb(a, b)
        return obj

    def _partitionSort(self, obj, n):
        i = 1
        pivot = obj[0]
        self.comparsions += len(obj)-1
        for j in range(1, n):
            if obj[j] < pivot:
                obj[j], obj[i] = self._swap(obj[j], obj[i])
                i += 1
        obj[0], obj[i-1] = self._swap(obj[0], obj[i-1])
        return obj, i-1

if __name__ == '__main__':
    import unittest

    class TestSorts(unittest.TestCase):
        def setUp(self):
            with open('data/IntegerArray.txt', 'r') as f:
                self.arrs = [
                    list(map(int, f.readlines())),
                    [16,1,19,5,8,18,2,6,9,15,4,7,3,17,11,14,10,12,13,22,48],
                    [10, 8, 2, 5],
                    [random.randrange(2**32) for i in range(2**16)],    # list of randomized generated integers
                ]

        def runForloop(self, pivot):
            for arr in self.arrs:
                s = QuickSort(arr)
                output = s.sort(pivot=pivot)
                self.assertEqual(output, sorted(arr))

        def test_MergeSort(self):
            for arr in self.arrs:
                sort = MergeSort(arr)
                output = sort.sort()
                self.assertEqual(output, sorted(arr))

        def test_QuickSort_first(self):
            self.runForloop('first')

        def test_QuickSort_median(self):
            self.runForloop('median')

        def test_QuickSort_last(self):
            self.runForloop('last')

        def test_QuickSort_rand(self):
            self.runForloop('rand')

    suite = unittest.TestLoader().loadTestsFromTestCase(TestSorts)
    unittest.TextTestRunner(verbosity=2).run(suite)
