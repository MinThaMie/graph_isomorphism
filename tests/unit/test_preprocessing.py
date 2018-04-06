import unittest

import preprocessing
import tests


class TestPreprocessing(unittest.TestCase):

    def setUp(self):
        tests.set_up_test_graphs()

    def test_checks(self):
        g = tests.v4e4_connected
        h = tests.v4e4_connected
        self.assertTrue(preprocessing.checks(g, h))

        g = tests.v5e4loop_unconnected
        self.assertFalse(preprocessing.checks(g, h))

    def test_loner_removal(self):
        g = tests.v5e4loop_unconnected  # g has 1 'loner'
        num_vertices = len(g.vertices)
        g = preprocessing.remove_loners(g)
        self.assertEqual(num_vertices - 1, len(g.vertices))

    def test_use_complement(self):
        # A star shaped graph that should use the complement
        many_edges_graph = tests.v5e7
        g, h = preprocessing.check_complement(many_edges_graph, many_edges_graph)
        self.assertTrue(g is not many_edges_graph)
        self.assertTrue(h is not many_edges_graph)
        # A nice W shaped graph that should not return the complement
        w_shaped_graph = tests.v5e4loop_unconnected
        g, h = preprocessing.check_complement(w_shaped_graph, w_shaped_graph)
        self.assertTrue(g is w_shaped_graph)
        self.assertTrue(h is w_shaped_graph)
