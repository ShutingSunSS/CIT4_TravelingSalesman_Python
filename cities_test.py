# File:        cities_test.py
# Programmer:  Shuting Sun
# Time:        Sep 25, 2016
# Description: CIT 590, Assignment 4.
#              The unittest of the file: cities.py
          

# from math import *
from cities import *   # import everything from your module
import unittest  # This loads the testing methods and a main program

class cities(unittest.TestCase):
    # We do not need to test the "distance" function, but I put it here anyway.
    def test_distance(self):
        self.assertAlmostEqual(distance(0, 0, 0, 0), 0)
        self.assertAlmostEqual(distance(0, 0, 0, 90), 2 * pi * 3956 * 90 / 360)
        self.assertAlmostEqual(distance(0, 0, 90, 90), 2 * pi * 3956 * 90 / 360)
        self.assertAlmostEqual(distance(0, 0, 0, -90), 2 * pi * 3956 * 90 / 360)

    # We do not need to test the "read_cities" function, but I put it here anyway.
    def test_read_cities(self):
        res = read_cities("city-data.txt")
        self.assertEqual(res[0], ['Alabama','Montgomery', '32.361538', '-86.279118'])
        self.assertEqual(len(res), 50)
        self.assertEqual(len(res[randrange(50)]), 4) # pick one line randomly to test the length, which should always be 4.
        self.assertEqual(res[len(res) - 1], ['Wyoming', 'Cheyenne', '41.145548', '-104.802042'])
        self.assertEqual(res[len(res) - 1][2], '41.145548') # Could not use [] here.
        self.assertEqual(res[0][1], 'Montgomery')
        self.assertEqual(res[0][len(res[0]) - 1], '-86.279118')

    def test_compute_total_distance(self):
        x = ['X', 'x', '0', '0']
        y = ['Y', 'y', '0', '180']
        self.assertAlmostEqual(compute_total_distance([x, y]), 2 * pi * 3956)

        a = ['A', 'a', '0', '0']
        b = ['B', 'b', '1', '1']
        c = ['C', 'c', '2', '3']
        self.assertAlmostEqual(compute_total_distance([a]), 0)
        self.assertAlmostEqual(compute_total_distance([a, b]), 2 * distance(0, 0, 1, 1))
        self.assertAlmostEqual(compute_total_distance([a, b, c]),\
                               distance(0, 0, 1, 1) + distance(1, 1, 2, 3) + distance(2, 3, 0, 0))

        res = read_cities("city-data.txt")
        self.assertAlmostEqual(compute_total_distance([['Alabama','Montgomery', '32.361538', '-86.279118']]), 0)
        self.assertAlmostEqual(compute_total_distance([res[0]]), 0) # need [] here.
        self.assertAlmostEqual(compute_total_distance([res[0], res[1]]),\
                               2 * distance(32.361538, -86.279118, 58.301935, -134.41974))

    def test_swap_adjacent_cities(self):
        res = read_cities("city-data.txt")
        self.assertEqual(swap_adjacent_cities(res[0:3], 0)[0], [res[1], res[0], res[2]])
        self.assertAlmostEqual(swap_adjacent_cities(res[0:3], 0)[1],\
                         compute_total_distance([res[1], res[0], res[2]]))

        self.assertEqual(swap_adjacent_cities(res, 49)[0], [res[49]] + res[1:49] + [res[0]])
        self.assertAlmostEqual(swap_adjacent_cities(res, 49)[1],\
                         compute_total_distance([res[49]] + res[1:49] + [res[0]]))
 
    def test_swap_cities(self):
        res = read_cities("city-data.txt")
        self.assertEqual(swap_cities([res[0]], 0, 0)[0], [res[0]])
        self.assertEqual(swap_cities([res[0]], 0, 0)[1], 0)
        self.assertEqual(swap_cities(res, 2, 4)[0], res[0:2] + [res[4]] + [res[3]] + [res[2]] + res[5: len(res)])

    def test_find_best_cycle(self):
        res = read_cities("city-data.txt")
        best = find_best_cycle(res)
        self.assertEqual(len(best), 50)

        best_set = []
        original_set = []
        for i in range (0, 50): # Change two road maps to "hashable" lists
            best_set = best_set + best[i]
            original_set = original_set + res[i]
        self.assertEqual(set(best_set), set(original_set)) # Compare the original road map and the resultant road map as sets

        self.assertTrue(compute_total_distance(best) < 30000) # I got several results after 10000 swaps like: 23310.373, 24202.586...
        

unittest.main()
