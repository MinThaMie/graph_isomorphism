"""
Test file for Color Refinement Algorithm
"""
import os
import unittest

from color_refinement import get_number_isomorphisms
from graph_io import *

PATH = 'graphs/branching'
EXPECTED = dict()


def expected_result(filename, g_name, h_name):
    key = g_name + h_name
    if key in EXPECTED[filename].keys():
        return EXPECTED[filename][key]
    else:
        return 0


def get_files():
    all_graphs = os.listdir(PATH)
    return [x for x in all_graphs if x in EXPECTED.keys()]


def testfile(filename):
    """Check if results for the given file are correct"""
    with open(PATH + "/" + filename) as f:
        L = load_graph(f, read_list=True)

    graphs = L[0]
    results = []
    for i in range(len(graphs)):
        for j in range(len(graphs)):
            if j > i:
                num = get_number_isomorphisms(graphs[i], graphs[j], True)
                expected = expected_result(filename, graphs[i].name, graphs[j].name)
                message = "Expected " + str(expected) + " for " + graphs[i].name + " and " + graphs[
                    j].name + " in " + filename
                results.append([expected, num, message])
    return results


class CountIsomorphismCase(unittest.TestCase):
    """Tests for `color_refinement.py`."""

    def test_files(self):
        files = get_files()
        for file in files:
            results = testfile(file)
            for result in results:
                self.assertEqual(result[0], result[1], result[2])
                # print(result[2], 'got', result[1])


if __name__ == '__main__':
    with open(PATH + "/" + 'expected_results.txt') as f:
        EXPECTED = read_expected_result(f)

    unittest.main()
