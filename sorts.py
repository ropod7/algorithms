#!/usr/bin/env/python3

# In this script case using Divide & Conquer paradigm, to:
# 1. Sort list objects and
# 2. Count number of SplitInversions in unsorted list object
# by RecursiveTree, MergeSort and QuickSort algorithms

import os
import random
import datetime

class BaseSort(object):
    sortedOut = []

    def __init__(self, obj):
        self.obj = obj
        self.over = max(obj) + 1         # to define over value in merge sort
        self.sortedIn = sorted(obj)      # defined to compare output result

    def sort(self):
        time = datetime.datetime.now()
        self.sortedOut = self._recursiveSort(self.obj)
        print('executed at:', datetime.datetime.now()-time)

    def repr_results(self):
        is_sorted = self.sortedOut == self.sortedIn
        data = 'List is sorted: {0}'.format(is_sorted)
        return data

    def _recursive_comb(self, a, b):
        a = self._recursiveSort(a) if len(a) > 1 else a  # recursive call for 1st half
        b = self._recursiveSort(b) if len(b) > 1 else b  # recursive call for 2nd half
        return a, b

# running time is O(nlog(n))
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

# running time is O(nlog(n))
# can't apply Master Method [random, unbalanced subproblems]
class QuickSort(BaseSort):

    def _swap(self, item0, item1):
        return item1, item0

    def _choose_pivot(self, obj):
        half = len(obj)//2
        index = random.randrange(0, half+1)                 # choosen randomly from 50% of n
        obj[0], obj[index] = self._swap(obj[0], obj[index]) # place pivot to the 0 pos
        return obj

    def _recursiveSort(self, obj):
        n = len(obj)
        if n == 1: return
        obj = self._choose_pivot(obj)             # every pivot compared in input array exactly once
        obj, index = self._partitionSort(obj, n)
        a, b = obj[:index], obj[index+1:]         # split partitions around pivot
        obj[:index], obj[index+1:] = self._recursive_comb(a, b)
        return obj

    def _partitionSort(self, obj, n):
        i = 1
        pivot = obj[0]
        for j in range(1, n):
            if obj[j] < pivot:
                obj[j], obj[i] = self._swap(obj[j], obj[i])
                i += 1
        obj[0], obj[i-1] = self._swap(obj[0], obj[i-1])
        return obj, i-1

if __name__ == '__main__':
    with open('/media/roman/100GB/Downloads/IntegerArray.txt') as f:
        lines = list(map(int, f.readlines()))
    # or just:
    #lines = [1,5,8,2,6,9,4,7,3,11,14,10,12,13]
    si = QuickSort(lines)
    si.sort()
    #print('output:', si.sortedOut)
    print(si.repr_results())

