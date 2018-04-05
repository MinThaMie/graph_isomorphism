import tests
import unittest
import os

from color_refinement import *
from graph_io import load_graph

PATH = 'graphs/branching'  # to run locally from PyCharm: PATH = '../../graphs/branching'
TREE1 = 'trees90.grl'
TREE2 = 'trees36.grl'
BIGTREE1 = 'bigtrees1.grl'
BIGTREE2 = 'bigtrees3.grl'


def get_files(expected: dict):
    all_graphs = os.listdir(PATH)
    return [x for x in all_graphs if x in expected.keys()]


def load_graph_from_file(filename):
    """Check if results for the given file are correct"""
    with open(PATH + "/" + filename) as f:
        L = load_graph(f, read_list=True)

    graph = L[0][0]
    return graph


class TestTrees(unittest.TestCase):
    def setUp(self):
        tests.set_up_test_graphs()

    def test_is_tree(self):
        simple_tree_graph = tests.v3e2_connected
        unconnected_tree = tests.v5e4loop_unconnected
        not_a_tree_graph = tests.v4e4_connected
        also_not_a_tree = tests.v5e7
        self.assertTrue(preprocessing.is_tree(simple_tree_graph))
        self.assertTrue(preprocessing.is_tree(unconnected_tree))
        self.assertFalse(preprocessing.is_tree(not_a_tree_graph))
        self.assertFalse(preprocessing.is_tree(also_not_a_tree))

    def test_files(self):
        start = time.time()
        self.assertTrue(preprocessing.is_tree(load_graph_from_file(TREE1)))
        self.assertTrue(preprocessing.is_tree(load_graph_from_file(TREE2)))
        self.assertTrue(preprocessing.is_tree(load_graph_from_file(BIGTREE1)))
        self.assertTrue(preprocessing.is_tree(load_graph_from_file(BIGTREE2)))
        end = time.time()
        print('All trees took', end - start, 'seconds to identify as a tree')

    def test_get_weight(self):
        g = tests.create_graph_helper([(0, 1), (1, 2), (2, 3), (2, 4)])
        arb_root = g.find_vertex(0)
        for v in g.vertices:
            v.weight = 0
        set_weight(arb_root)
        self.assertEqual(5, g.find_vertex(0).weight)
        self.assertEqual(4, g.find_vertex(1).weight)
        self.assertEqual(3, g.find_vertex(2).weight)
        self.assertEqual(1, g.find_vertex(3).weight)
        self.assertEqual(1, g.find_vertex(4).weight)
        for v in g.vertices:
            v.weight = 0
        arb_root = g.find_vertex(2)
        set_weight(arb_root)
        self.assertEqual(5, g.find_vertex(2).weight)
        self.assertEqual(2, g.find_vertex(1).weight)
        self.assertEqual(1, g.find_vertex(0).weight)
        self.assertEqual(1, g.find_vertex(3).weight)
        self.assertEqual(1, g.find_vertex(4).weight)

    def test_shift(self):
        g = tests.create_graph_helper([(0, 1), (0, 2), (2, 3), (0, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (8, 10)])
        arb_root = g.find_vertex(0)
        for v in g.vertices:
            v.weight = 0
        set_weight(arb_root)
        self.assertEqual(11, g.find_vertex(0).weight)
        root = shift(arb_root, g.order)
        self.assertEqual(g.find_vertex(5), root)

    def test_get_root(self):
        g = tests.create_graph_helper([(0, 1), (0, 2), (2, 3), (0, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (8, 10)])
        for v in g.vertices:
            v.weight = 0
        root = choose_a_root(g)
        self.assertEqual(g.find_vertex(5), root)

    def test_levels(self):
        g = tests.create_graph_helper([(0, 1), (0, 2), (0, 3), (1, 4), (1, 5), (2, 6), (6, 8), (3, 7)])
        for v in g.vertices:
            v.weight = 0
            v.level = None
            v.children = []
        root = choose_a_root(g)
        self.assertEqual(g.find_vertex(0), root)
        assign_levels(root)
        self.assertEqual(0, g.find_vertex(0).level)
        self.assertEqual(1, g.find_vertex(1).level)
        self.assertEqual(1, g.find_vertex(2).level)
        self.assertEqual(1, g.find_vertex(3).level)
        self.assertEqual(2, g.find_vertex(4).level)
        self.assertEqual(2, g.find_vertex(5).level)
        self.assertEqual(2, g.find_vertex(6).level)
        self.assertEqual(2, g.find_vertex(7).level)
        self.assertEqual(3, g.find_vertex(8).level)
        g = tests.create_graph_helper(
            [(0, 1), (0, 2), (1, 3), (1, 4), (1, 5), (2, 6), (2, 7), (2, 8), (6, 9), (6, 10), (8, 11), (8, 12)])
        for v in g.vertices:
            v.weight = 0
            v.level = None
            v.children = []
        root = choose_a_root(g)
        self.assertEqual(g.find_vertex(2), root)
        assign_levels(root)
        self.assertEqual(1, g.find_vertex(0).level)
        self.assertEqual(2, g.find_vertex(1).level)
        self.assertEqual(0, g.find_vertex(2).level)
        self.assertEqual(3, g.find_vertex(3).level)
        self.assertEqual(3, g.find_vertex(4).level)
        self.assertEqual(3, g.find_vertex(5).level)
        self.assertEqual(1, g.find_vertex(6).level)
        self.assertEqual(1, g.find_vertex(7).level)
        self.assertEqual(1, g.find_vertex(8).level)
        self.assertEqual(2, g.find_vertex(9).level)
        self.assertEqual(2, g.find_vertex(10).level)
        self.assertEqual(2, g.find_vertex(11).level)
        self.assertEqual(2, g.find_vertex(12).level)

    def test_tree_isomorphism(self):
        # G and H are the trees from the article, but root from our algorithm is different so doesn't match in result
        g = tests.create_graph_helper(
            [(0, 1), (0, 2), (1, 3), (1, 4), (1, 5), (2, 6), (2, 7), (2, 8), (6, 9), (6, 10), (8, 11), (8, 12)])
        h = tests.create_graph_helper(
            [(0, 1), (0, 2), (1, 3), (1, 4), (1, 5), (2, 6), (2, 7), (2, 8), (3, 9), (3, 10), (4, 11), (4, 12)])

        result = tree_isomorphism(g, h)
        self.assertListEqual([0, 0, 0], g.find_vertex(1).tuples)
        self.assertListEqual([0, 0, 0], h.find_vertex(2).tuples)
        self.assertTrue(result)

        # Graph H minus the last edges 4 - 12
        j = tests.create_graph_helper(
            [(0, 1), (0, 2), (1, 3), (1, 4), (1, 5), (2, 6), (2, 7), (2, 8), (3, 9), (3, 10), (4, 11)])

        result = tree_isomorphism(g, j)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
