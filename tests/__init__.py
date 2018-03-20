import unittest
from copy import deepcopy

from mygraph import Graph, Edge


class Tests(unittest.TestCase):

    def setUp(self):
        # Instantiate the empty graph
        self.empty_graph = Graph()

        # Instantiate a connected graph of order 2
        connected_graph_order_2 = Graph(n=2)
        vertices = connected_graph_order_2.vertices
        connected_graph_order_2.add_edge(Edge(tail=vertices[0], head=vertices[1]))
        self.connected_graph_order_2 = connected_graph_order_2

        # Instantiate a non-trivial graph
        non_trivial_graph = Graph(n=5)
        vertices = non_trivial_graph.vertices
        non_trivial_graph.add_edge(Edge(vertices[0], vertices[1]))
        non_trivial_graph.add_edge(Edge(vertices[1], vertices[2]))
        non_trivial_graph.add_edge(Edge(vertices[1], vertices[4]))
        non_trivial_graph.add_edge(Edge(vertices[2], vertices[3]))
        non_trivial_graph.add_edge(Edge(vertices[3], vertices[4]))
        self.non_trivial_graph = non_trivial_graph

        # Create two instances of the same non-trivial graph, each with one different sub-element field
        non_trivial_graph_different_label = deepcopy(self.non_trivial_graph)
        non_trivial_graph_different_label.vertices[0].label = 'spam'
        self.non_trivial_graph_different_label = non_trivial_graph_different_label

        non_trivial_graph_different_weight = deepcopy(self.non_trivial_graph)
        edge = non_trivial_graph_different_weight.edges[0]
        non_trivial_graph_different_weight.del_edge(edge)
        non_trivial_graph_different_weight.add_edge(Edge(tail=edge.tail, head=edge.head, weight=1))
        self.non_trivial_graph_different_weight = non_trivial_graph_different_weight

    def test_mygraph_graph_eq(self):
        # Assert that a graph is not an object of a different type
        self.assertNotEqual(None, Graph())

        # Assert that the empty graph is equal to itself
        self.assertEqual(self.empty_graph, self.empty_graph)
        self.assertEqual(Graph(), self.empty_graph)

        # Assert that a non-trivial graph is equal to itself
        self.assertEqual(self.non_trivial_graph, self.non_trivial_graph)

        # Assert that a non-trivial graph and others with the same structure but with different sub-element fields
        # are unequal
        self.assertNotEqual(self.non_trivial_graph, self.non_trivial_graph_different_label)
        self.assertNotEqual(self.non_trivial_graph, self.non_trivial_graph_different_weight)

if __name__ == '__main__':
    unittest.main()
