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
    sortedOut = []

    def __init__(self, obj):
        self.obj = obj
        self.over = max(obj) + 1                                        # to define over value in merge sort
        self.sortedIn = sorted(obj)                                     # defined to compare output result

    def sort(self):
        obj = self.obj
        output = self._recursiveSort(obj) if len(obj) > 1 else obj
        self.sortedOut = output
        return output

    def repr_results(self):
        is_sorted = self.sortedOut == self.sortedIn
        data = 'List is sorted: {0}'.format(is_sorted)
        return data

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
        if n == 1: return 0
        a, b = self._split(obj, n)
        a, b = self._recursive_comb(a, b)
        d = self._merge(a, b, n, si)
        return d

class SplitInversions(MergeSort):
    inversions = 0

    def _recursiveSort(self, *args):
        return super(SplitInversions, self)._recursiveSort(*args, si=True)

    def repr_results(self):
        data = super(SplitInversions, self).repr_results()
        data += '\nSplit inversions: {0}'.format(self.inversions)
        return data

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

        choices = ['first', 'median', 'last', 'rand']
        assert pivot in choices
        self.choice = pivot
        time = datetime.now()
        self.sortedOut = self._recursiveSort(self.obj)
        print('executed at:', datetime.now()-time)

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
            print(s)
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
            try:
                index = random.randrange(0, lenobj)
            except ValueError:
                index = random.randrange(0, lenobj+1)
        if choice is not 'rand':
            obj[0], obj[index] = self._swap(obj[0], obj[index])         # place pivot to the 0 pos
        return obj

    def _recursiveSort(self, obj):
        n = len(obj)
        if n == 1: return
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

    def repr_results(self):
        data = super(QuickSort, self).repr_results()
        data += '\nNum of comparsions: {0}'.format(self.comparsions)
        return data

# the running time is O(n)
class RSelect(QuickSort):                                               # Randomized Selection

    def select(self, ith):
        _assertions = ['Order statistic must to be an integer',
                       'iterable object much shorter']
        assert isinstance(ith, int), _assertions[0]
        assert ith <= len(self.obj), _assertions[1]
        self.choice = 'rand'
        self.ith = ith
        time = datetime.now()
        self.order_stat = self._recursiveSelect(self.obj, ith)
        print('Executed in:', datetime.now() - time)

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

    def repr_results(self):
        data = super(RSelect, self).repr_results()
        data += '\nThe {0}th order statistics is: {1}'.format(self.ith,
            self.order_stat)
        return data

# the running time is linear
class DSelect(RSelect):                                                 # Deterministic Selection

    def _get_median(self, obj):
        lenobj = len(obj)
        obj = MergeSort(obj).sort()
        half = lenobj // 2
        if lenobj >= 3:
            odd = lenobj % 2
            return obj[half] if odd else obj[half-1]
        else:
            return min(obj) if lenobj == 2 else obj[0]
                                                                        # return index of median
    def _choose_pivot(self, obj):
        ns = 5                                                          # number of length each part
        if len(obj) < ns: return self._get_median(obj)                  # return index of median of medians
        parts = [obj[i:i+ns] for i in range(0, len(obj), ns)]           # logically break list into n/5 groups of size 5 each
        medians = list(map(self._get_median, parts))                    # get indexes of medians of each input list
        return self._choose_pivot(medians)                              # recursively compute median of medians

    def _recursiveSelect(self, obj, i):
        n = len(obj)
        pivot = self._choose_pivot(obj)
        index = obj.index(pivot)
        obj[0], obj[index] = self._swap(obj[0], obj[index])             # place pivot to 0 position
        return self._partitioning(obj, n, i)

if __name__ == '__main__':
    with open('IntegerArray.txt', 'r') as f:
        lines = list(map(int, f.readlines()))
    # or just:
    #lines = [16,1,19,5,8,18,2,6,9,15,4,7,3,17,11,14,10,12,13,22,48]
    #lines = [10, 8, 2, 5]
    s = DSelect(lines)
    s.select(4)
    #print(s.sortedOut)
    #s.sort(pivot='median')
    #s.sort(pivot='last')
    #s.sort(pivot='rand')
    print(s.repr_results())

