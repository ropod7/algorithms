import os
from math import log

class SplitInversions(object):
    inversions = 0
    sortedOut = []
    
    def __init__(self, obj):
        self.obj = obj
        self.sortedIn = sorted(obj) # defined to compare result
        self.largest = max(obj)     # to define over value in merge sort
        
    def run(self):
        self.sortedOut = self.split(self.obj)

    def merge(self, a, b, lenl):
        d = []
        i = j = si = 0  # si is split inversions
        over = self.largest + 1
        for k in range(lenl):
            A = a[i] if i != len(a) else over
            B = b[j] if j != len(b) else over
            if A < B:
                d.append(A)
                i += 1
            else:
                d.append(B)
                j += 1            
                si += len(a) - i
            
        self.inversions += si
        return d

    def split(self, lines):
        lenl = len(lines)
        if lenl == 1: return 0 
        a, b = lines[:lenl/2], lines[lenl/2:]
        a = self.split(a) if len(a) > 1 else a
        b = self.split(b) if len(b) > 1 else b
        d = self.merge(a, b, lenl)
        return d
        
    def repr_results(self):
        data = 'Split inversions: {0}\nList is sorted: {1}'.format(
            self.inversions, self.sortedOut == self.sortedIn)
        return data

if __name__ == '__main__':
    lines = [1, 3, 0, 10, 23, 11, 6, 5, 2, 9, 4, 8, 7, 12]
    si = SplitInversions(lines)
    si.run()
    print si.repr_results()

