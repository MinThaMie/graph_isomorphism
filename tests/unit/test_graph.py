import unittest

import tests
from graph import Graph


class GraphTests(unittest.TestCase):

    def setUp(self):
        tests.set_up_test_graphs()

    def test_name(self):
        graph = Graph(directed=False)
        self.assertEqual('G', graph.name)
        graph.name = 'spam'
        self.assertEqual('spam', graph.name)

    def test_add(self):
        # Assert that the empty graph added to itself is itself
        should_be_empty = tests.empty_graph + tests.empty_graph
        self.assertEqual([], should_be_empty.vertices)
        self.assertEqual([], should_be_empty.edges)

        # Assert that adding the empty graph to a non-empty graph is the non-empty graph
        should_be_non_trivial_graph = tests.non_trivial_graph + tests.empty_graph
        self.assertEqual(tests.non_trivial_graph.vertices, should_be_non_trivial_graph.vertices)
        self.assertEqual(tests.non_trivial_graph.edges, should_be_non_trivial_graph.edges)

        # Assert that all vertices and edges of two individual non-empty graphs are in their disjoint union
        disjoint_union = tests.non_trivial_graph + tests.connected_graph_order_2
        expected_vertices = tests.non_trivial_graph.vertices + tests.connected_graph_order_2.vertices
        expected_edges = tests.non_trivial_graph.edges + tests.connected_graph_order_2.edges
        self.assertEqual(expected_vertices, disjoint_union.vertices)
        self.assertEqual(expected_edges, disjoint_union.edges)

        # Assert the same, but use the inline addition operator
        tests.non_trivial_graph += tests.connected_graph_order_2
        self.assertEqual(expected_vertices, tests.non_trivial_graph.vertices)
        self.assertEqual(expected_edges, tests.non_trivial_graph.edges)

        # Assert that the graph name is correctly formed by the disjoint union
        g = Graph(directed=False)
        h = Graph(directed=False)
        h.name = 'H'
        self.assertEqual('G ⊎ H', (g + h).name)
        self.assertEqual('H ⊎ G', (h + g).name)
        g.name = ''
        self.assertEqual('', (g + h).name)
        self.assertEqual('', (h + g).name)

        # Assert that the disjoint union with a directed graph results in a directed graph
        directed = Graph(directed=True)
        undirected = Graph(directed=False)

        self.assertTrue((directed + directed).directed)
        self.assertTrue((directed + undirected).directed)
        self.assertTrue((undirected + directed).directed)
        self.assertFalse((undirected + undirected).directed)

        # Assert that the disjoint unions with a non-simple graph results in a non-simple graph
        simple = Graph(directed=False, simple=True)
        non_simple = Graph(directed=False, simple=False)

        self.assertTrue((simple + simple).simple)
        self.assertFalse((simple + non_simple).simple)
        self.assertFalse((non_simple + simple).simple)
        self.assertFalse((non_simple + non_simple).simple)


if __name__ == '__main__':
    unittest.main()
