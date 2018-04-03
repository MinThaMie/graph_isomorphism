"""
Test file for Fast Color Refinement Algorithm
"""
import os
import unittest

import color_refinement
import tests
from graph_io import *

PATH = 'graphs/colorref'
EXPECTED = dict()
EXPECTED['colorref_smallexample_2_49.grl'] = {'G0G1': "Bijection"}
EXPECTED['colorref_smallexample_4_7.grl'] = {'G1G3': "Bijection", 'G0G2': None}
EXPECTED['colorref_smallexample_6_15.grl'] = {'G0G1': "Bijection", 'G2G3': None, 'G4G5': None}


def get_expected_result(filename, g_name, h_name):
    if filename in EXPECTED.keys():
        key = g_name + h_name
        if key in EXPECTED[filename].keys():
            return EXPECTED[filename][key]
        else:
            return "Unbalanced"


def get_color_ref_files():
    all_graphs = os.listdir(color_refinement.PATH)
    return [x for x in all_graphs if x in EXPECTED.keys()]


def testfile(filename):
    """Check if results for the given file are correct"""
    with open(color_refinement.PATH + "/" + filename) as f:
        L = load_graph(f, read_list=True)

    graphs = L[0]
    results = []
    for i in range(len(graphs)):
        for j in range(len(graphs)):
            if j > i:
                coloring = color_refinement.initialize_coloring(graphs[i] + graphs[j])
                coloring = color_refinement.fast_color_refine(coloring)
                status = coloring.status(graphs[i], graphs[j])
                expected = get_expected_result(filename, graphs[i].name, graphs[j].name)
                message = "Expected " + str(expected) + " for " + graphs[i].name + " and " + graphs[
                    j].name + " in " + filename
                results.append([expected, status, message])
    return results


class FastColorRefineCase(unittest.TestCase):
    """Tests for `color_refinement.py`."""

    def test_files(self):
        files = get_color_ref_files()
        for file in files:
            results = testfile(file)
            for result in results:
                self.assertEqual(result[0], result[1], result[2])
                color_refinement.debug(result[2], 'got', result[1])

    def test_storing_known_isomorphisms(self):
        # Assert that initially there are no known isomorphisms
        self.assertEqual({}, color_refinement.known_isomorphisms)

        # Assert that, after processing a list of graphs containing some isomorphisms and anisomorphisms, the known
        # isomorphisms are correct
        tests.set_up_test_graphs()
        graphs = tests.isomorphic_graphs + tests.anisomorphic_graphs
        color_refinement.process(graphs)

        self.assertEqual({1}, color_refinement.known_isomorphisms[0])
        self.assertEqual({0}, color_refinement.known_isomorphisms[1])
        self.assertEqual(set(), color_refinement.known_isomorphisms[2])
        self.assertEqual(set(), color_refinement.known_isomorphisms[3])


if __name__ == '__main__':
    unittest.main()
