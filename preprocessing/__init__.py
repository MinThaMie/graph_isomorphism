from graph import *
from color_refinement_helper import compare, debug
from preprocessing.tree_algorithm_helper import has_cycle


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


def is_tree(g: Graph):
    """
    This method checks whether graph g is a tree. First iteration.
    Uses the is_cycle method from tree_algorithm_helper.py

    :param g: Graph
    :return: Boolean: True if the graph is a Tree
    """
    if len(g.vertices) is 0:
        return True
    if len(g.edges) > len(g.vertices) - 1:
        return False

    vertex = g.vertices[0]

    return not has_cycle(g, vertex, vertex, [])
