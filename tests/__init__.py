import unittest
from copy import deepcopy

from mygraph import Graph, Edge, Vertex


class Tests(unittest.TestCase):

    def setUp(self):
        # Prepare some vertex labels for general use
        vertex_labels = ['spam', 'ham', 'eggs', 'foo', 'bar', 'baz', 'qux', 'quux', 'quuz', 'corge', 'grault', 'garply',
                         'waldo', 'fred', 'plugh', 'xyzzy', 'thud']

        # Instantiate the empty graph
        empty_graph = Graph()
        # empty_graph.tag = 'empty_graph'  # Don't uncomment
        self.empty_graph = empty_graph

        # Instantiate a connected graph of order 2
        connected_graph_order_2 = Graph(n=2)
        vertices = connected_graph_order_2.vertices
        connected_graph_order_2.add_edge(Edge(tail=vertices[0], head=vertices[1]))
        connected_graph_order_2.tag = 'connected_graph_order_2'
        for (vertex, label) in zip(connected_graph_order_2.vertices, vertex_labels):
            vertex.label = label
        self.connected_graph_order_2 = connected_graph_order_2

        # Instantiate the disconnected graph of order 2, which is the complement of a connected graph of order 2
        disconnected_graph_order_2 = Graph(n=2)
        # disconnected_graph_order_2 = 'disconnected_graph_order_2'  # Don't uncomment
        self.disconnected_graph_order_2 = disconnected_graph_order_2

        # Instantiate a non-trivial graph
        non_trivial_graph = Graph(n=5)
        vertices = non_trivial_graph.vertices
        non_trivial_graph.add_edge(Edge(vertices[0], vertices[1]))
        non_trivial_graph.add_edge(Edge(vertices[1], vertices[2]))
        non_trivial_graph.add_edge(Edge(vertices[1], vertices[4]))
        non_trivial_graph.add_edge(Edge(vertices[2], vertices[3]))
        non_trivial_graph.add_edge(Edge(vertices[3], vertices[4]))
        non_trivial_graph.tag = 'non_trivial_graph'
        self.non_trivial_graph = non_trivial_graph

        # Create two instances of the same non-trivial graph, each with one different sub-element field
        non_trivial_graph_different_label = deepcopy(self.non_trivial_graph)
        non_trivial_graph_different_label.vertices[0].label = 'spam'
        non_trivial_graph_different_label.tag = 'non_trivial_graph_different_label'
        self.non_trivial_graph_different_label = non_trivial_graph_different_label

        non_trivial_graph_different_weight = deepcopy(self.non_trivial_graph)
        edge = non_trivial_graph_different_weight.edges[0]
        non_trivial_graph_different_weight.del_edge(edge)
        non_trivial_graph_different_weight.add_edge(Edge(tail=edge.tail, head=edge.head, weight=1))
        non_trivial_graph_different_weight.tag = 'non_trivial_graph_different_weight'
        self.non_trivial_graph_different_weight = non_trivial_graph_different_weight

    def test_mygraph_vertex_graphs(self):
        vertex = Vertex()

        self.assertEqual(set(), vertex.graphs)

        self.non_trivial_graph.add_vertex(vertex)
        self.assertTrue(self.non_trivial_graph in vertex.graphs)

        self.connected_graph_order_2.add_vertex(vertex)
        self.assertTrue(self.connected_graph_order_2 in vertex.graphs)
        self.assertTrue(self.non_trivial_graph in vertex.graphs)

        self.non_trivial_graph.del_vertex(vertex)
        self.assertFalse(self.non_trivial_graph in vertex.graphs)
        self.assertTrue(self.connected_graph_order_2 in vertex.graphs)

    def test_mygraph_graph_tag(self):
        graph = Graph()
        self.assertEqual(None, graph.tag)
        graph.tag = 'spam'
        self.assertEqual('spam', graph.tag)

    def test_mygraph_graph_eq(self):
        # Assert that a graph is not an object of a different type
        self.assertNotEqual(None, Graph())

        # Assert that the empty graph is equal to itself
        self.assertEqual(self.empty_graph, self.empty_graph)

        # Assert that the tagless empty graph is unequal to the empty graph with a tag
        graph = Graph()
        graph.tag = 'spam'
        self.assertNotEqual(self.empty_graph, graph)

        # Assert that a non-trivial graph is equal to itself
        self.assertEqual(self.non_trivial_graph, self.non_trivial_graph)

        # Assert that a non-trivial graph and others with the same structure but with different sub-element fields
        # are unequal
        self.assertNotEqual(self.non_trivial_graph, self.non_trivial_graph_different_label)
        self.assertNotEqual(self.non_trivial_graph, self.non_trivial_graph_different_weight)

    def test_mygraph_graph_add(self):
        # Assert that the empty graph added to itself is itself
        self.assertEqual(self.empty_graph, self.empty_graph + self.empty_graph)

        # Assert that adding the empty graph to a non-empty graph is the non-empty graph
        self.non_trivial_graph.tag = Graph().tag  # Get the default graph tag

        self.assertEqual(self.non_trivial_graph, self.non_trivial_graph + self.empty_graph)
        self.assertEqual(self.non_trivial_graph, self.empty_graph + self.non_trivial_graph)

        # Assert that all vertices and edges of two individual non-empty graphs are in their disjoint union
        disjoint_union = self.non_trivial_graph + self.connected_graph_order_2
        expected_vertices = self.non_trivial_graph.vertices + self.connected_graph_order_2.vertices
        expected_edges = self.non_trivial_graph.edges + self.connected_graph_order_2.edges
        self.assertEqual(expected_vertices, disjoint_union.vertices)
        self.assertEqual(expected_edges, disjoint_union.edges)

        # Assert the same, but use the inline addition operator
        self.non_trivial_graph += self.connected_graph_order_2
        self.assertEqual(expected_vertices, self.non_trivial_graph.vertices)
        self.assertEqual(expected_edges, self.non_trivial_graph.edges)


    def test_mygraph_graph_next_label(self):
        generated_max = max(Graph._generated_label_values, default=0)
        Graph._generated_label_values |= set(range(0, 2 * generated_max))
        self.assertEqual(2 * generated_max, Graph.next_label())
        self.assertEqual(2 * generated_max + 1, Graph._next_label_value)
        self.assertEqual(Graph._next_label_value, Graph.next_label())


if __name__ == '__main__':
    unittest.main()
