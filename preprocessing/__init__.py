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


def calculate_modular_decompositions_and_factor(g: Graph, md_g: ModularDecomposition) -> (Graph, int):
    """
    Determine if modular decomposition yields a simpler graph for further processing, along with a factor to multiply
    with the number of isomorphisms of those simpler graphs.

    :param Graph g: The graph to analyse.
    :param ModularDecomposition md_g: Graph g's modular decomposition.
    :return: 2-tuple of the graph to use in the algorithm and a factor with which to multiply the outcome. The graph
             need not be graph g's modular decomposition.
    """

    # TODO unit test

    if len(md_g) == g.order:  # Implies order of MD of G is not less than order of G
        return g, 1

    g_md = modules_to_graph(md_g)
    return g_md, modular_decomposition_factor(md_g)
