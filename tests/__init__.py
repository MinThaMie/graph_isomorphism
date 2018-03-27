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
    empty_graph.name = ''

    # Instantiate a connected graph of order 2
    # connected_graph_order_2 =
    #     spam - ham
    connected_graph_order_2 = Graph(directed=False, n=2)
    vertices = connected_graph_order_2.vertices
    connected_graph_order_2.add_edge(Edge(tail=vertices[0], head=vertices[1]))
    for (vertex, label) in zip(connected_graph_order_2.vertices, vertex_labels):
        vertex.label = label

    # Instantiate a non-trivial graph
    # non_trivial_graph =
    #           2
    #          / \
    #     0 - 1   3
    #          \ /
    #           4
    # N.b.: labels probably have different numbers due to unique label generation by tools.unique_integer()
    non_trivial_graph = Graph(directed=False, n=5)
    vertices = non_trivial_graph.vertices
    non_trivial_graph.add_edge(Edge(vertices[0], vertices[1]))
    non_trivial_graph.add_edge(Edge(vertices[1], vertices[2]))
    non_trivial_graph.add_edge(Edge(vertices[1], vertices[4]))
    non_trivial_graph.add_edge(Edge(vertices[2], vertices[3]))
    non_trivial_graph.add_edge(Edge(vertices[3], vertices[4]))
    non_trivial_graph.name = ''
