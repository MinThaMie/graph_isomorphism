from typing import Tuple

import tests
from graph import *

# Declare module variables
empty_graph: Graph
connected_graph_order_2: Graph
disconnected_graph_order_2: Graph
non_trivial_graph: Graph
non_trivial_graph_different_label: Graph
non_trivial_graph_different_weight: Graph
non_trivial_graph_complement: Graph


def set_up_test_graphs():
    global empty_graph, connected_graph_order_2, disconnected_graph_order_2, non_trivial_graph, \
        non_trivial_graph_different_label, non_trivial_graph_different_weight, non_trivial_graph_complement

    # Prepare some vertex labels for general use
    vertex_labels = ['spam', 'ham', 'eggs', 'foo', 'bar', 'baz', 'qux', 'quux', 'quuz', 'corge', 'grault', 'garply',
                     'waldo', 'fred', 'plugh', 'xyzzy', 'thud']

    # Instantiate the empty graph
    empty_graph = Graph(directed=False)

    # Instantiate a connected graph of order 2
    # connected_graph_order_2 =
    #     spam - ham
    connected_graph_order_2 = create_graph_helper([(vertex_labels[0], vertex_labels[1])])

    # Instantiate a non-trivial graph
    # non_trivial_graph =
    #           2
    #          / \
    #     0 - 1   3
    #          \ /
    #           4
    non_trivial_graph = create_graph_helper([(0, 1), (1, 2), (1, 4), (2, 3), (3, 4)])

    # Instantiate the non-trivial graph's complement
    # non_trivial_graph_complement =
    #               2
    #              / \
    #     1 - 3 - 0 - 4
    non_trivial_graph_complement = create_graph_helper([(2, 0), (3, 0), (4, 0), (3, 1), (4, 2)])


def create_graph_helper(edges: List[Tuple[object, object]] = list()):
    """
    Create a graph from the specified edges.

    :param edges: A list of 2-tuples of vertex labels (of any type) between which to create edges.
    :return: The graph with labelled vertices and edges
    """

    graph = Graph(False)
    vertices = {}

    for head, tail in edges:
        if head not in vertices:
            vertices[head] = Vertex(graph=graph, label=head)
            graph.add_vertex(vertices[head])

        if tail not in vertices:
            vertices[tail] = Vertex(graph=graph, label=tail)
            graph.add_vertex(vertices[tail])

        graph.add_edge(Edge(vertices[head], vertices[tail]))

    return graph
