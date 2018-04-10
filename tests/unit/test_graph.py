import unittest
from typing import Iterable, Any, Callable

import tests
from color_refinement_helper import compare
from graph import Graph, Vertex, Edge


class GraphTests(unittest.TestCase):

    def setUp(self):
        tests.set_up_test_graphs()

    def test_name(self):
        graph = Graph(directed=False)
        self.assertEqual('G', graph.name)
        graph.name = 'spam'
        self.assertEqual('spam', graph.name)

    def test_order(self):
        self.assertEqual(0, tests.empty_graph.order)
        self.assertEqual(2, tests.connected_graph_order_2.order)
        self.assertEqual(5, tests.non_trivial_graph.order)

    def test_size(self):
        self.assertEqual(0, tests.empty_graph.size)
        self.assertEqual(1, tests.connected_graph_order_2.size)
        self.assertEqual(5, tests.non_trivial_graph.size)

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
        self.assertEqual(expected_vertices, disjoint_union.vertices)

        expected_edges = tests.non_trivial_graph.edges + tests.connected_graph_order_2.edges
        self.assertEqual(expected_edges, disjoint_union.edges)

        # Assert that the inline addition operator form a correct disjoint union
        graph = tests.non_trivial_graph.deepcopy()
        expected_vertices = graph.vertices
        expected_edges = graph.edges

        graph += tests.connected_graph_order_2
        expected_vertices += tests.connected_graph_order_2.vertices
        expected_edges += tests.connected_graph_order_2.edges

        self.assertEqual(expected_vertices, graph.vertices)
        self.assertEqual(expected_edges, graph.edges)

        # Assert that the disjoint union of a graph itself is twice that graph
        graph = tests.non_trivial_graph
        disjoint_union = graph + graph
        expected_vertices = graph.vertices + graph.vertices
        expected_edges = graph.edges + graph.edges

        self.assertEqual(expected_vertices, disjoint_union.vertices)
        self.assertEqual(expected_edges, disjoint_union.edges)

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

    def test_complement(self):
        vertex_label = Vertex.label.__get__
        vertex_degree = Vertex.degree.__get__

        def edge_tail_label(edge: Edge): return edge.tail.label

        def edge_head_label(edge: Edge): return edge.head.label

        def _compare_iterables_by_function(thingies: Iterable[Any], stuffs: Iterable[Any],
                                           fun: Callable[[Any], Any]) -> bool:
            """
            Compare objects by function.

            :param Iterable thingies: One iterable.
            :param Iterable stuffs: Another iterable.
            :param function fun: Callable that maps the specified iterables to whatever being compared.
            :return: `True` if the iterables compare equal based on the mapping made by the callable; `False` otherwise.
            """

            return compare(map(fun, thingies), map(fun, stuffs))

        # Assert that the complement of the empty graph is the empty graph
        complement = tests.empty_graph.complement()
        self.assertEqual([], complement.vertices)
        self.assertEqual([], complement.edges)

        # Assert that the complement of the singly connected graph of order 2 is the disconnected graph of order 2
        graph = tests.connected_graph_order_2
        complement = graph.complement()

        self.assertTrue(_compare_iterables_by_function(graph.vertices, complement.vertices, vertex_label))

        self.assertEqual([], complement.edges)

        # Assert that the complement of the complement of a graph is the graph itself
        complement = complement.complement()

        self.assertTrue(_compare_iterables_by_function(graph.vertices, complement.vertices, vertex_label))
        self.assertTrue(_compare_iterables_by_function(graph.vertices, complement.vertices, vertex_degree))

        self.assertTrue(_compare_iterables_by_function(graph.edges, complement.edges, edge_tail_label))
        self.assertTrue(_compare_iterables_by_function(graph.edges, complement.edges, edge_head_label))

        # Assert that the complement of a non-trivial graph is correctly constructed
        graph = tests.non_trivial_graph
        complement = graph.complement()
        expected = tests.non_trivial_graph_complement

        self.assertTrue(_compare_iterables_by_function(graph.vertices, complement.vertices, vertex_label))
        self.assertTrue(_compare_iterables_by_function(graph.vertices, complement.vertices, vertex_degree))
        self.assertTrue(_compare_iterables_by_function(expected.vertices, complement.vertices, vertex_label))
        self.assertTrue(_compare_iterables_by_function(expected.vertices, complement.vertices, vertex_degree))

        self.assertTrue(_compare_iterables_by_function(expected.edges, complement.edges, edge_tail_label))
        self.assertTrue(_compare_iterables_by_function(expected.edges, complement.edges, edge_head_label))


if __name__ == '__main__':
    unittest.main()
