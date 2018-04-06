"""
Test file for Color Refinement Algorithm
"""
import os
import unittest

from color_refinement import get_number_automorphisms
from color_refinement_helper import debug
from graph_io import *

PATH_auto = 'graphs/branching'# to run locally from PyCharm: PATH = '../../graphs/branching'


def expected_result(filename, key, expected):
    if key in expected[filename].keys():
        return expected[filename][key]
    else:
        return 0


def get_files(expected: dict):
    all_graphs = os.listdir(PATH_auto)
    return [x for x in all_graphs if x in expected.keys()]


def testfile(filename, file_expected):
    """Check if results for the given file are correct"""
    with open(PATH_auto + "/" + filename) as f:
        L = load_graph(f, read_list=True)

    graphs = L[0]
    results = []
    # for i in range(len(graphs)):
    for graph_nr in file_expected.get(filename).keys():
        num = get_number_automorphisms(graphs[graph_nr])
        expected = expected_result(filename, graph_nr, file_expected)
        message = "Expected " + str(expected) + " for G" + str(graph_nr) + " in " + filename
        results.append([expected, num, message])
    return results


class CountIsomorphismCase(unittest.TestCase):
    """Tests for `color_refinement.py`."""

    EXPECTED = None

    def setUp(self):
        with open(PATH_auto + "/" + 'expected_results_auto_small') as f:
            self.EXPECTED = read_expected_result_auto(f)

    def test_files(self):
        files = get_files(self.EXPECTED)
        for file in files:
            results = testfile(file, self.EXPECTED)
            for result in results:
                self.assertEqual(result[0], result[1], result[2])
                debug(result[2], 'got', result[1])


if __name__ == '__main__':
    unittest.main()
