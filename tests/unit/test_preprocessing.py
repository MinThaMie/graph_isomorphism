import unittest
import preprocessing
from graph import Graph
from tests import *


class TestPreprocessing(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.v4e4 = graph_vertex4edge4()
        cls.v5e4loop = graph_vertex5edge4loop()

    def test_checks(self):
        g = self.v4e4
        h = self.v4e4
        self.assertTrue(preprocessing.checks(g, h))

        g = self.v5e4loop
        self.assertFalse(preprocessing.checks(g, h))

    def test_loner_removal(self):
        g = self.v5e4loop  # g has 1 'loner'
        num_vertices = len(g.vertices)
        g = preprocessing.remove_loners(g)
        self.assertEqual(num_vertices - 1, len(g.vertices))

    def test_use_complement(self):
        # A nice star shaped graph that should use the complement
        many_edges_graph = create_graph_helper([(0, 3), (1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)])
        g, h = preprocessing.check_complement(many_edges_graph, many_edges_graph)
        self.assertTrue(g is not many_edges_graph)
        self.assertTrue(h is not many_edges_graph)
        # A nice W shaped graph that should not return the complement
        w_shaped_graph = create_graph_helper([(1, 3), (0, 3), (0, 4), (2, 4)])
        g, h = preprocessing.check_complement(w_shaped_graph, w_shaped_graph)
        self.assertTrue(g is w_shaped_graph)
        self.assertTrue(h is w_shaped_graph)

