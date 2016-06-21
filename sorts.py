#!/usr/bin/env/python3

# In this script case using Divide & Conquer paradigm, to:
# 1. Sort list objects (MergeSort, QuickSort, SplitInversions) and
# 2. Count number of SplitInversions in unsorted list object
# by RecursiveTree, MergeSort and QuickSort algorithms

import os
import random
import datetime

class MergeSort(object):
    sortedOut = []

    def __init__(self, obj):
        self.obj = obj
        self.over = max(obj) + 1         # to define over value in merge sort
        self.sortedIn = sorted(obj)     # defined to compare output result

    def sort(self):
        time = datetime.datetime.now()
        self.sortedOut = self._recursiveSort(self.obj)
        print('executed at:', datetime.datetime.now()-time)

    def _get_value(self, obj, i):
        return obj[i] if i != len(obj) else self.over

    def _merge(self, a, b, lenl):
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
        return output

    def _split(self, obj, n):
        return obj[:n//2], obj[n//2:]

    def _recursiveSort(self, obj):
        n = len(obj)
        if n == 1: return 0
        a, b = self._split(obj, n)
        a = self._recursiveSort(a) if len(a) > 1 else a  # recursive call for 1st half
        b = self._recursiveSort(b) if len(b) > 1 else b  # recursive call for 2nd half
        d = self._merge(a, b, n)
        return d

    def repr_results(self):
        is_sorted = self.sortedOut == self.sortedIn
        data = 'List is sorted: {0}'.format(is_sorted)
        return data

class SplitInversions(MergeSort):
    inversions = 0

    def _merge(self, a, b, lenl):
        output = []
        i = j = 0
        len_a = len(a)
        for k in range(lenl):
            A = self._get_value(a, i)
            B = self._get_value(b, j)
            if A < B:
                output.append(A)
                i += 1
            else:
                output.append(B)
                j += 1
                self.inversions += len_a - i
        return output

    def repr_results(self):
        data = super(SplitInversions, self).repr_results()
        data += '\nSplit inversions: {0}'.format(self.inversions)
        return data

class QuickSort(MergeSort):

    def _swap(self, item0, item1):
        return item1, item0

    def _choose_pivot(self, obj):
        half = len(obj)//2
        index = random.randrange(0, half+1)     # choosen randomly from 50% of n
        pivot = obj[index]
        return index, pivot

    def _recursiveSort(self, obj):
        self.obj = obj
        n = len(obj)
        if n == 1: return
        index, pivot = self._choose_pivot(obj)
        obj[0], obj[index] = self._swap(obj[0], obj[index]) # place pivot to the 0 pos
        obj = self._partitionSort(obj, pivot, n)
        index = obj.index(pivot)                            # get index of current pos of pivot
        a, b = obj[:index], obj[index+1:]                   # split partitions around pivot
        obj[:index]   = self._recursiveSort(a) if len(a) > 1 else a
        obj[index+1:] = self._recursiveSort(b) if len(b) > 1 else b
        return obj

    def _partitionSort(self, obj, pivot, n):
        i = 1
        for j in range(1, n):
            if obj[j] < pivot:
                obj[j], obj[i] = self._swap(obj[j], obj[i])
                i += 1
        obj[0], obj[i-1] = self._swap(obj[0], obj[i-1])
        return obj

if __name__ == '__main__':
    with open('IntegerArray.txt') as f:
        lines = list(map(int, f.readlines()))
    # or just:
    #lines = [1,5,8,2,6,9,4,7,3,11,14,10,12,13]
    si = QuickSort(lines)
    si.sort()
    #print('output:', si.sortedOut)
    print(si.repr_results())

