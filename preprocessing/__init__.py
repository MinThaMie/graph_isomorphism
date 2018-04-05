from graph import *
from color_refinement_helper import compare, debug


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
    amount_of_vertices = g.order
    if g.size > (amount_of_vertices * (amount_of_vertices - 1)) / 4:
        debug("Uses complements")
        return g.complement(), h.complement()
    else:
        return g, h


def is_tree(g: Graph):
    """
    This method checks whether graph g is a tree. First iteration.

    :param g: Graph
    :return: Boolean: True if the degrees are the same
    """
    visited = []

    if len(g.vertices) is 0:
        return True
    vertex = g.vertices[0]
    visited.append(vertex.label)

    return not is_cycle(g, vertex, vertex, visited)


def is_cycle(g: Graph, vertex: Vertex, predecessor: Vertex, visited):
    """
    Recursive function to detect cycles in a graph

    :param g: input graph
    :param vertex: vertex to start from
    :param predecessor: predecessor vertex of vertex
    :param visited: List with visited vertices
    :return: Boolean: True if the degrees are the same
    """
    visited.append(vertex.label)
    cyclic = False

    for v in vertex.neighbours:
        if v.label in visited and v is not predecessor:
            cyclic = True
        else:
            cyclic = is_cycle(g, v, vertex, visited)
    return cyclic
