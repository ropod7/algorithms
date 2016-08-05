#!/usr/bin/env/python3
#-*- coding: utf8 -*-

class MaxMirror:                                                        # maximum length of mirroring items
    def __init__(self):
        self.count = 0
        self.obj = []

    def search(self, obj):
        lenobj = len(obj)
        if obj > self.obj: self.obj = obj
        if lenobj is 1: return self._get_count(1)
        elif lenobj is 0: return 0
        pivot = obj[0]
        for i in range(lenobj-1, 0, -1):
            if pivot is obj[i]:
                part = obj[:i+1]                                        # set partition of sequence with equivalent tails
                lenpart = len(part)
                odd = lenpart % 2                                       # get odd
                a = part[:lenpart//2]                                   # define 1st part
                b = part[lenpart//2 + odd:]                             # define 2nd part
                count = self._partitioning(a, b, odd=odd)               # explore 1st and 2nd part of partition
                self.count = self._get_count(count)
                if self.count * 2 < len(self.obj)//2:                   # check, is there reason to explore next sequence
                    i -= count                                          # continue from items that not explored yet
                    continue
                else:                                                   # if explored more than half of obj redefine maxmirror
                    break
        # shift object 1 index to the left and explore recursively to
        # find higher maxmirror, if obj contains elements more than explored
        # and if explored more than half of obj return final result
        reason = len(self.obj)//2 > self.count
        return self.search(obj[1:]) if reason else self.count

    def _partitioning(self, a, b, shift=False, odd=0):
        len_a = len(a)
        if len_a is 1 and not odd and not shift:
            return 2                                                    # if items are neighbors return 2
        elif a == list(reversed(b)):                                    # compare parts
            return len_a * 2 + odd if not shift else len_a              # check for middle single item in first call and return length
        else:
            return self._partitioning(a[:-1], b[1:], shift=True)        # recursively explore shifted parts

    def _get_count(self, value):
        return value if value > self.count else self.count              # if current maxmirror higher than global set as global

if __name__ == '__main__':
    import unittest
    # testcases:
    class MirrorTest(unittest.TestCase):
        def setUp(self):
            self.objects = (
                # header objects:
                ([1, 2, 3, 8, 9, 3, 2, 1], 3),
                ([1, 2, 1, 4], 3),
                ([7, 1, 2, 9, 7, 2, 1], 2),
                # test objects:
                ([1, 2, 3, 8, 9, 3, 2, 1], 3),
                ([1, 2, 1, 4], 3),
                ([7, 1, 2, 9, 7, 2, 1], 2),
                ([21, 22, 9, 8, 7, 6, 23, 24, 6, 7, 8, 9, 25, 7, 8, 9], 4),
                ([1, 2, 1, 20, 21, 1, 2, 1, 2, 23, 24, 2, 1, 2, 1, 25], 4),
                ([1, 2, 3, 2, 1], 5),
                ([1, 2, 3, 3, 8], 2),
                ([1, 2, 7, 8, 1, 7, 2], 2),
                ([1, 1, 1], 3),
                ([1], 1),
                ([], 0),
                ([5, 9, 9, 4, 5, 4, 9, 9, 2], 7),
                ([5, 9, 9, 6, 5, 4, 9, 9, 2], 2),
                ([5, 9, 1, 6, 5, 4, 1, 9, 5], 3),
                ([9, 1, 1, 4, 2, 1, 1, 1], 3),
                # extra objects:
                ([4, 6, 7, 2, 1, 3, 4, 1, 2, 4, 5, 7, 2, 1], 2),
            )

        def test_equals(self):
            for obj, value in self.objects:
                maxmir = MaxMirror().search(obj)
                self.assertEqual(maxmir, value,
                    'obj: %s:\n\tresult: %d != %d' % (obj, maxmir, value))

    suite = unittest.TestLoader().loadTestsFromTestCase(MirrorTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
