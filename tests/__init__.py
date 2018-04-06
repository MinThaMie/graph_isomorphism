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
isomorphic_graphs: List[Graph]
anisomorphic_graphs: List[Graph]
v4e4_connected: Graph
v5e4loop_unconnected: Graph
v5e7: Graph
v3e2_connected: Graph
v5e4_connected: Graph


def set_up_test_graphs():
    global empty_graph, connected_graph_order_2, disconnected_graph_order_2, non_trivial_graph, \
        non_trivial_graph_different_label, non_trivial_graph_different_weight, non_trivial_graph_complement, \
        isomorphic_graphs, anisomorphic_graphs, v4e4_connected, v5e4loop_unconnected, v5e7, v3e2_connected, \
        v5e4_connected

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
    non_trivial_graph.name = 'non_trivial_graph'

    # Instantiate the non-trivial graph's complement
    # non_trivial_graph_complement =
    #               2
    #              / \
    #     1 - 3 - 0 - 4
    non_trivial_graph_complement = create_graph_helper([(2, 0), (3, 0), (4, 0), (3, 1), (4, 2)])
    non_trivial_graph_complement.name = 'non_trivial_graph_complement'

    # Instantiate some isomorphic graphs
    # iso_0 =
    #           - 0 -
    #          /     \
    #     3 - 4 - 1 - 5
    #          \     /
    #           - 2 -
    # iso_1 =
    #           - 2 -
    #          /     \
    #     3 - 4 - 0 - 5
    #          \     /
    #           - 1 -
    # iso_2 =
    #           - 1 -
    #          /     \
    #     3 - 4 - 2 - 5
    #          \     /
    #           - 0 -
    changing_labels = [0, 1, 2]
    isomorphic_graphs = []
    for _ in range(len(changing_labels)):  # Because changing_labels changes, this can't simply be changing_labels
        _0 = changing_labels[0]
        _1 = changing_labels[1]
        _2 = changing_labels[2]
        isomorphism = create_graph_helper([(3, 4), (4, _0), (_0, 5), (4, _1), (_1, 5), (4, _2), (_2, 5)])
        isomorphism.name = f'isomorphism_{_0}_{_1}_{_2}'
        isomorphic_graphs.append(isomorphism)
        changing_labels = [changing_labels.pop()] + changing_labels

    # Instantiate some anisomorphic graphs
    # anisomorphism_0 =
    #           - 4 -
    #          /  |  \
    #     3 - 0   1   2
    #          \  |  /
    #           - 5 -
    # anisomorphism_1 =
    #           - 4 -
    #          /  |  \
    #     3 - 0 - 1   2
    #          \     /
    #           - 5 -
    anisomorphism_0 = create_graph_helper([(3, 0), (0, 4), (4, 1), (4, 2), (0, 5), (1, 5), (2, 5)])
    anisomorphism_0.name = 'anisomorphism_0'
    anisomorphism_1 = create_graph_helper([(3, 0), (0, 4), (4, 1), (4, 2), (0, 5), (1, 0), (2, 5)])
    anisomorphism_1.name = 'anisomorphism_1'
    anisomorphic_graphs = [anisomorphism_0, anisomorphism_1]

    # Create a graph with 4 vertices and 4 edges with a cycle:
    # v4e4_connected =
    #         1 - 2 - 3
    #              \ /
    #               4
    v4e4_connected = create_graph_helper([(1, 2), (2, 3), (2, 4), (3, 4)])
    v4e4_connected.name = 'v4e4'

    # Create a graph with 5 vertices and 4 edges, including looped egde at vertex 4:
    # v5e4loop_unconnected =
    #         1 - 2 - 3   4--
    #                 |
    #                 5
    v5e4loop_unconnected = create_graph_helper([(1, 2), (2, 3), (3, 5), (4, 4)])
    v5e4loop_unconnected.name = 'v5e4_loop4'

    # Create a graph where the complement should be taken during preprocessing :
    # v5e7 =
    #               5 --
    #              / \  \
    #         1 - 2 - 3 |
    #              \ /  /
    #               4 --
    v5e7 = create_graph_helper([(0, 3), (1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)])
    v5e7.name = 'v5e7'

    # Create a graph with 3 vertices and 2 edges :
    # v3e2_connected =
    #         1 - 2 - 3
    v3e2_connected = create_graph_helper([(1, 2), (2, 3)])
    v3e2_connected.name = 'v3e2_connected'

    # Create a tree graph with 5 vertices and 4 edges :
    # v5e4_connected =
    #         1 - 2 - 3 - 4
    #                 |
    #                 5
    v5e4_connected = create_graph_helper([(1, 2), (2, 3), (3, 5), (3, 4)])
    v5e4_connected.name = 'v5e4_connected'


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
    Converts a dictionary of (int,[Vertex]) pairs to a Coloring
    :param mapping: dictionary of (int,[Vertex]) pairs
    """
    coloring = Coloring()
    for key in mapping:
        for vertex in mapping[key]:
            coloring.set(vertex=vertex, color=key)
    return coloring


def create_coloring_helper(vertices: List[int], map: dict):
    """
    Converts a dictionary of (int,[int]) pairs to a coloring,
    assuming that the given values in [int] are the labels of the given vertices
    :param vertices: list of vertex labels
    :param map: dict of (int, [int]) pairs
    :return:
    """
    coloring = Coloring()
    for color in map:
        for value in map[color]:
            vertex = [v for v in vertices if v.label == value][0]
            coloring.set(vertex, color)
    return coloring
