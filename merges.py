#!/usr/bin/env/python3

# In this script case using Divide & Conquer paradigm (at this moment), 
# to sort and count number of split inversions in unsorted list object 
# by Recursive Tree and Merge Sort algorithms

import os

class Merge(object):
    def __init__(self, obj):
        self.obj = obj
        self.largest = max(obj)     # to define over value in merge sort
        
    def merge(self, a, b, lenl):
        output = []
        i = j = si = 0              # si is split inversions
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
                si += len(a) - i
        return output, si

class SplitInversions(Merge):
    inversions = 0
    sortedOut = []
    
    def __init__(self, obj):
        super(SplitInversions, self).__init__(obj)
        self.sortedIn = sorted(obj)     # defined to compare output result
        
    def run(self):
        self.sortedOut = self.split(self.obj)
        
    def merge(self, *args):
        output, si = super(SplitInversions, self).merge(*args)
        self.inversions += si
        return output

    def split(self, obj):
        lenl = len(obj)
        if lenl == 1: return 0 
        a, b = obj[:lenl//2], obj[lenl//2:]
        a = self.split(a) if len(a) > 1 else a  # recursive call for 1st half
        b = self.split(b) if len(b) > 1 else b  # recursive call for 2nd half
        d = self.merge(a, b, lenl)
        return d
        
    def repr_results(self):
        data = 'Split inversions: {0}\nList is sorted: {1}'.format(
            self.inversions, self.sortedOut == self.sortedIn)
        return data

if __name__ == '__main__':
    with open('/path_to_unsorted/IntegerArray.txt') as f:
        lines = list(map(int, f.readlines()))
    
    si = SplitInversions(lines)
    si.run()
    print(si.repr_results())

