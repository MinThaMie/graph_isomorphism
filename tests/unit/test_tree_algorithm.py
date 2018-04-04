import time

import preprocessing
import tests
import unittest
import os

from graph_io import load_graph

PATH = 'graphs/branching'  # to run locally from PyCharm: PATH = '../../graphs/branching'
TREE1 = 'trees90.grl'
TREE2 = 'trees36.grl'
BIGTREE1 = 'bigtrees1.grl'
BIGTREE2 = 'bigtrees2.grl'


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
        print('All trees took', end - start, 'seconds to identify it as a tree')

