"""
Test file for Color Refinement Algorithm
"""
import os
import unittest

from color_refinement import is_isomorphisms
from graph_io import *

PATH = 'graphs/colorref'
EXPECTED = dict()
EXPECTED['colorref_smallexample_2_49.grl'] = {'G0G1': True}
EXPECTED['colorref_smallexample_4_7.grl'] = {'G1G3': True, 'G0G2': True}
EXPECTED['colorref_smallexample_6_15.grl'] = {'G0G1': True, 'G2G3': True, 'G4G5': True}


def get_expected_result(filename, g_name, h_name):
    if filename in EXPECTED.keys():
        key = g_name + h_name
        if key in EXPECTED[filename].keys():
            return EXPECTED[filename][key]
        else:
            return False


def get_color_ref_files():
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
                isomorph = is_isomorphisms(graphs[i], graphs[j])
                expected = get_expected_result(filename, graphs[i].name, graphs[j].name)
                message = "Expected " + str(expected) + " for " + graphs[i].name + " and " + graphs[
                    j].name + " in " + filename
                results.append([expected, isomorph, message])
    return results


class ColorRefineCase(unittest.TestCase):
    """Tests for `color_refinement.py`."""

    def test_files(self):
        files = get_color_ref_files()
        for file in files:
            results = testfile(file)
            for result in results:
                self.assertEqual(result[0], result[1], result[2])
                # print(result[2], 'got', result[1])


if __name__ == '__main__':
    unittest.main()
