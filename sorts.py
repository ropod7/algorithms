#!/usr/bin/env/python3

# In this script case using Divide & Conquer paradigm, to:
# 1. Sort lists objects (MergeSort, QuickSort, SplitInversions) and
# 2. Count number of SplitInversions in unsorted list object
# by RecursiveTree, MergeSort and QuickSort algorithms

import os
import random
import datetime

class MergeSort(object):
    sortedOut = []

    def __init__(self, obj):
        self.obj = obj
        self.largest = max(obj)         # to define over value in merge sort
        self.sortedIn = sorted(obj)     # defined to compare output result

    def sort(self):
        time = datetime.datetime.now()
        self.sortedOut = self._recursiveSort(self.obj)
        print('executed at:', datetime.datetime.now()-time)

    def _merge(self, a, b, lenl):
        output = []
        i = j = 0
        over = self.largest + 1
        for k in range(lenl):
            A = a[i] if i != len(a) else over
            B = b[j] if j != len(b) else over
            if A < B:
                output.append(A)
                i += 1
            else:
                output.append(B)
                j += 1
                try:
                    self.inversions += len(a) - i
                except AttributeError: pass
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
        obj[0], obj[index] = self._swap(obj[0], obj[index])
        obj = self._partition(obj, pivot, n)
        index = obj.index(pivot)
        a, b = obj[:index], obj[index+1:]
        obj[:index]   = self._recursiveSort(a) if len(a) > 1 else a
        obj[index+1:] = self._recursiveSort(b) if len(b) > 1 else b
        return obj

    def _partition(self, obj, pivot, n):
        i = 1
        for j in range(1, n):
            if obj[j] < pivot:
                obj[j], obj[i] = self._swap(obj[j], obj[i])
                i += 1
        obj[0], obj[i-1] = self._swap(obj[0], obj[i-1])
        return obj

if __name__ == '__main__':
    with open('/media/roman/100GB/Downloads/IntegerArray.txt') as f:
    #with open('/path_to_unsorted/IntegerArray.txt') as f:
        lines = list(map(int, f.readlines()))
    si = QuickSort(lines)
    si.sort()
    #print('output:', si.sortedOut)
    print(si.repr_results())
