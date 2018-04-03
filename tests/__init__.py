from typing import Tuple

import tests
from graph import *
from coloring import *
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


def create_coloring_helper_vertex(mapping: dict) -> Coloring:
    """
    Converts a dictionary to Coloring
    """
    coloring = Coloring()
    for key in mapping:
        for vertex in mapping[key]:
            coloring.set(vertex=vertex, color=key)
    return coloring


def create_coloring_helper(vertices: List[int], map: dict):
    coloring = Coloring()
    for color in map:
        for value in map[color]:
            vertex = [v for v in vertices if v.label == value][0]
            coloring.set(vertex, color)
    return coloring


def graph_vertex2edge1() -> Graph:
    """
        Create a graph with structure:

        1 - 2

        :return: The created graph
        """
    v2e1 = Graph(False)
    v_g1 = Vertex(v2e1)
    v_g2 = Vertex(v2e1)
    e_g = Edge(v_g1, v_g2)
    v2e1.add_edge(e_g)
    return v2e1


def graph_vertex3edge2() -> Graph:
    """
        Create a graph with structure:

        1 - 2 - 3

        :return: The created graph
        """
    v3e2 = Graph(False, name='G')
    v_g1 = Vertex(v3e2)
    v_g2 = Vertex(v3e2)
    v_g3 = Vertex(v3e2)
    e_g1 = Edge(v_g1, v_g2)
    e_g2 = Edge(v_g2, v_g3)
    v3e2.add_edge(e_g1)
    v3e2.add_edge(e_g2)
    return v3e2


def graph_vertex4edge4() -> Graph:
    """
        Create a graph with structure:

        1 - 2 - 3
         \ /
          4

        :return: The created graph
        """
    v4e4 = Graph(False)
    v_g1 = Vertex(v4e4)
    v_g2 = Vertex(v4e4)
    v_g3 = Vertex(v4e4)
    v_g4 = Vertex(v4e4)
    e_g1 = Edge(v_g1, v_g2)
    e_g2 = Edge(v_g2, v_g3)
    e_g3 = Edge(v_g2, v_g4)
    e_g4 = Edge(v_g3, v_g4)
    v4e4.add_edge(e_g1)
    v4e4.add_edge(e_g2)
    v4e4.add_edge(e_g3)
    v4e4.add_edge(e_g4)
    return v4e4


def graph_vertex5edge4() -> Graph:
    """
        Create a graph with structure:

        1 - 2 - 3 - 4
                |
                5

    :return: The created graph
    """
    v4e4 = Graph(False)
    v_h1 = Vertex(v4e4)
    v_h2 = Vertex(v4e4)
    v_h3 = Vertex(v4e4)
    v_h4 = Vertex(v4e4)
    v_h5 = Vertex(v4e4)
    e_h1 = Edge(v_h1, v_h2)
    e_h2 = Edge(v_h2, v_h3)
    e_h3 = Edge(v_h3, v_h4)
    e_h4 = Edge(v_h3, v_h5)
    v4e4.add_edge(e_h1)
    v4e4.add_edge(e_h2)
    v4e4.add_edge(e_h3)
    v4e4.add_edge(e_h4)
    return v4e4


def graph_vertex5edge4loop() -> Graph:
    """
        Create a graph with structure:

        1 - 2 - 3   4
                |
                5

    :return: The created graph
    """
    v5e4loop = Graph(False)
    v_h1 = Vertex(v5e4loop)
    v_h2 = Vertex(v5e4loop)
    v_h3 = Vertex(v5e4loop)
    v_h4 = Vertex(v5e4loop)
    v_h5 = Vertex(v5e4loop)
    e_h1 = Edge(v_h1, v_h2)
    e_h2 = Edge(v_h2, v_h3)
    e_h3 = Edge(v_h4, v_h4)
    e_h4 = Edge(v_h3, v_h5)
    v5e4loop.add_edge(e_h1)
    v5e4loop.add_edge(e_h2)
    v5e4loop.add_edge(e_h3)
    v5e4loop.add_edge(e_h4)
    return v5e4loop
