import math

from color_refinement_helper import compare, debug, modules_to_graph, ModularDecomposition
from graph import *


def checks(g, h) -> bool:
    """
    Collection method of all preprocessing checks

    :param g: Graph
    :param h: Graph
    :return: Boolean: True if everything checks out
    """
    return check_graph_size(g, h) and check_graph_order(g, h) and check_degrees(g, h)


def check_graph_order(g: Graph, h: Graph):
    """
    This method checks if the order (amount of vertices) of the graphs are equal

    :param g: Graph
    :param h: Graph
    :return: Boolean: True if the amount of vertices are the same
    """
    return len(g.vertices) == len(h.vertices)


def check_graph_size(g: Graph, h: Graph):
    """
    This method checks if the number of edges of the graphs are equal

    :param g: Graph
    :param h: Graph
    :return: Boolean: True if the amount of edges are the same
    """
    return len(g.edges) == len(h.edges)


def check_degrees(g: Graph, h: Graph):
    """
    This method checks if the degrees of all the vertices in the graphs are all the same

    :param g: Graph
    :param h: Graph
    :return: Boolean: True if the degrees are the same
    """
    degree_g = [v.degree for v in g.vertices]
    degree_h = [v.degree for v in h.vertices]
    return compare(degree_g, degree_h)


def remove_loners(g: Graph):
    """
        Method removes
        - Vertices with degree 0.
        - corrollas & knots (vertices that have one or more loops and no non-loop edges)

    :param g: Graph
    :return: processed Graph g
    """
    for vertex in g.vertices:
        if vertex.degree is 0 or (all(neigh == vertex for neigh in vertex.neighbours)):
            g.del_vertex(vertex)
    return g


def check_complement(g: Graph, h: Graph) -> (Graph, Graph):
    """
        Method checks if complement is necessary

    :param g: Graph
    :param h: Graph
    :return: Graph g and h, complemented if necessary
    """
    amount_of_vertices = g.order
    if g.size > (amount_of_vertices * (amount_of_vertices - 1)) / 4:
        debug("Uses complements")
        return g.complement(), h.complement()
    else:
        return g, h


"""
Exercise 4: Algorithms on graphs
"""
from graph import *
from graph_io import load_graph, save_graph, write_dot


# Program a breadth-first search (BFS) algorithm.
# Use this to:
# – test whether a given graph is connected,
# – compute distances from a given vertex (unit edge weights), and
# – label vertices in the order they are visited.

# Use a queue to store the vertices that should be visited next.
# (A queue can be implemented using a Python list, or using a doubly-linked list for more efficiency.)


def BFS(G: Graph, s: Vertex):
    """
    Breadth First Search Alg. Which also:
    tests if the graph is connected,
    computes the distance from s to the other edges
    labels the vertices in the order they are visited
    :param G: Graph
    :param s: start node
    :return: (isConnected, {dict of distances}, {dict of labels})
    """
    L = [s]  # queue
    dist = {s: 0}
    label = {s: 1}
    label_counter = 1
    # s.label = 1 # Store visiting order in label

    # Label nodes (and compute distance to s meanwhile)
    while len(L) > 0:
        v = L[0]  # BFS so FIFO
        for w in v.neighbours:
            # If w not labeled
            if w not in label:
                label_counter += 1
                label[w] = label_counter
                # w.label = k # Store visiting order in vertex label
                dist[w] = dist[v] + 1
                w.colornum = dist[w]  # Color according to dist.
                L.append(w)
        L.pop(0)

    is_connected = (len(label) == len(G.vertices))
    return is_connected, dist, label


def DFS(G: Graph, s: Vertex):
    """
    Depth First Search Alg. Which also:
    tests if the graph is connected,
    computes the distance from s to the other edges
    labels the vertices in the order they are visited
    :param G: Graph
    :param s: start node
    :return: (isConnected, {dict of distances}, {dict of labels})
    """
    L = [s]  # stack
    pred = {}  # predecessor of each node u in the s-u path
    dist = {s: 0}
    label = {s: 1}
    label_counter = 1
    s.label = label_counter

    # Label nodes (and compute distance to s meanwhile)
    while len(L) > 0:
        v = L[-1]  # BFS so LIFO
        # Pick first unlabeled neighbour (and set predecessor if needed)
        next_v = None
        for w in v.neighbours:
            if w not in pred.keys():
                pred[w] = v

            if w not in label:
                next_v = w

        if next_v != None:
            # Label neighbour
            label_counter += 1
            label[next_v] = label_counter
            next_v.label = label_counter  # Store visiting order in vertex label
            # calculate distance using predecessor
            dist[next_v] = dist[pred[next_v]] + 1
            next_v.colornum = dist[next_v]  # Color according to dist.
            L.append(next_v)
        else:
            L.pop()

    is_connected = (len(label) == len(G.vertices))
    return is_connected, dist, label


def find_vertex(G: Graph, label):
    """
    Find the vertex with the given label in the given graph
    :param G: Graph
    :param label: label of the vertex
    :return: vertex with the given label or None when no such vertex is found
    """
    for v in G.vertices:
        if v.label == label:
            return v
    return None


def print_result(result):
    isConnected, dist, label = result[0], result[1], result[2]
    print('isConnected?', isConnected)
    print('v,label,dist')
    for v in dist.keys():
        print(v, ',', label[v], ',', dist[v])


# generate a .dot  le from examplegraph.gr.
with open('mygraph.gr') as f:
    G = load_graph(f)

print('\nBFS')
a = BFS(G, G.vertices[0])
print_result(a)
print('G:', G)

print('\nDFS')
a = DFS(G, G.vertices[0])
print_result(a)
print('G:', G)

with open('mygraph2.dot', 'w') as f:
    write_dot(G, f)


def is_tree(g: Graph):
    """
    This method checks whether graph g is a tree. First iteration.
    Uses the is_cycle method from tree_algorithm_helper.py

    :param g: Graph
    :return: Boolean: True if the graph is a Tree
    """
    if len(g.vertices) is 0:
        return True
    if len(g.edges) != len(g.vertices) - 1:
        return False

    vertex = g.vertices[0]

    return not has_cycle(g, vertex, vertex, [])


def has_cycle(g: Graph, vertex: Vertex, predecessor: Vertex, visited):
    """
    Recursive function to detect cycles in a graph

    :param g: input graph
    :param vertex: vertex to start from
    :param predecessor: predecessor vertex of vertex
    :param visited: List with visited vertices
    :param result: list containing the "Truth Of The Tree"
    :return: result: [True] if has_cycle
    """
    visited.append(vertex)

    for v in vertex.neighbours:
        if v in visited and v is not predecessor:
            return True
        elif v not in visited:
            return has_cycle(g, v, vertex, visited)


def get_modular_decomposition_sizes(md: ModularDecomposition):
    return map(len, md)


def check_modular_decomposition(md_g: ModularDecomposition, md_h: ModularDecomposition) -> bool:
    """
    Check if modular decompositions of two graphs indicate anisomorphism.

    :param ModularDecomposition md_g: One modular decomposition.
    :param ModularDecomposition md_h: Another modular decomposition.
    :return: `False` if the graphs cannot be isomorphic; `True` otherwise.
    """

    return \
        len(md_g) == len(md_h) \
        and compare(get_modular_decomposition_sizes(md_g), get_modular_decomposition_sizes(md_h))


def modular_decomposition_factor(md: ModularDecomposition) -> int:
    result = 1
    factors = [math.factorial(len(module)) for module in md]

    for factor in factors:
        result *= factor

    return result


def _check_modular_decomposition_length(g: Graph, md_g: ModularDecomposition) -> bool:
    return len(md_g) == g.order


def calculate_modular_decomposition_and_factor(g: Graph, md_g: ModularDecomposition) -> (Graph, int):
    """
    Determine if modular decomposition yields a simpler graph for further processing, along with a factor to multiply
    with the number of isomorphisms of those simpler graphs.

    :param Graph g: The graph to analyse.
    :param ModularDecomposition md_g: Graph g's modular decomposition.
    :return: 2-tuple of the graph to use in the algorithm and a factor with which to multiply the outcome. The graph
             need not be graph g's modular decomposition.
    """

    if _check_modular_decomposition_length(g, md_g):  # Implies order of MD of G is not less than order of G
        return g, 1

    factor = modular_decomposition_factor(md_g)
    debug(f'Using modular decomposition with factor = {factor}')

    g_md = modules_to_graph(md_g)
    return g_md, factor


def calculate_modular_decomposition_without_factor(g: Graph, md_g: ModularDecomposition) -> Graph:
    if _check_modular_decomposition_length(g, md_g):  # Implies order of MD of G is not less than order of G
        return g
    return modules_to_graph(md_g)
