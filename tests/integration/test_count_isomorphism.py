"""
Test file for Color Refinement Algorithm
"""
import os
import time
import unittest

from color_refinement import get_number_isomorphisms
from color_refinement_helper import debug, initialize_coloring
from graph_io import *

PATH = 'graphs/branching'  # to run locally from PyCharm: PATH = '../../graphs/branching'


def expected_result(filename, g_name, h_name, expected):
    key = g_name + h_name
    if key in expected[filename].keys():
        return expected[filename][key]
    else:
        return 0


def get_files(expected: dict):
    all_graphs = os.listdir(PATH)
    return [x for x in all_graphs if x in expected.keys()]


def testfile(filename, file_expected):
    print('Testing #Iso', filename, end=' ', flush=True)
    start_time = time.time()

    """Check if results for the given file are correct"""
    with open(PATH + "/" + filename) as f:
        graphs = load_graph(f, read_list=True)

    graphs = graphs[0]
    results = []
    for i in range(len(graphs)):
        for j in range(len(graphs)):
            if j > i:
                num = get_number_isomorphisms(graphs[i], graphs[j], initialize_coloring(graphs[i] + graphs[j]), True)
                expected = expected_result(filename, graphs[i].name, graphs[j].name, file_expected)
                message = "Expected " + str(expected) + " for " + graphs[i].name + " and " + graphs[
                    j].name + " in " + filename
                results.append([expected, num, message])

    print(f'({time.time() - start_time})', flush=True)
    return results


class CountIsomorphismCase(unittest.TestCase):
    """Tests for `color_refinement.py`."""

    EXPECTED = None

    def setUp(self):
        with open(PATH + "/" + 'expected_results_small.txt') as f:
            self.EXPECTED = read_expected_result(f)

    def test_files(self):
        files = get_files(self.EXPECTED)
        for file in files:
            results = testfile(file, self.EXPECTED)
            for result in results:
                self.assertEqual(result[0], result[1], result[2])
                debug(result[2], 'got', result[1])


if __name__ == '__main__':
    unittest.main()
