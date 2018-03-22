from graph import Graph
from color_refiment_helper import compare


def check_graph_order(g: Graph, f: Graph):
    """
    This method checks the orders (amount of vertices) of the graphs are the same

    :param g: Graph
    :param f: Graph
    :return: Boolean: True if the amount of vertices are the same
    """
    return len(g.vertices) == len(f.vertices)


def check_graph_size(g: Graph, f: Graph):
    """
    This method checks if the sizes (the amount of edges) of the graphs are the same

    :param g: Graph
    :param f: Graph
    :return: Boolean: True if the amount of edges are the same
    """
    return len(g.edges) == len(f.edges)


def check_degrees(g: Graph, f: Graph):
    """
    This method checks if the degrees of all the vertices in the graphs are all the same

    :param g: Graph
    :param f: Graph
    :return: Boolean: True if the degrees are the same
    """
    degree_g = [v.degree for v in g.vertices]
    degree_f = [v.degree for v in f.vertices]
    return compare(degree_g, degree_f)
