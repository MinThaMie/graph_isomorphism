"""
Module with helper methods for the Color Refinement Algorithm
"""
from coloring import *

DEBUG = False


def debug(*args):
    """
    Prints debug statements when DEBUG is set to `True`

    :param args: argument to be printed
    """
    if DEBUG:
        print(*args)


def compare(s: List, t: List, my_key=None) -> bool:
    """
    Compares if two lists are equal

    :param s: List to compare
    :param t: List to compare
    :return: Returns `True` if list have the same length and contain the same elements. Elements do not need to have the
    same order. Returns `False` otherwise.
    """
    return sorted(s, key=my_key) == sorted(t, key=my_key)


def create_new_color_class(coloring: Coloring, vertex1: Vertex, vertex2: Vertex) -> Coloring:
    """
    Returns a new coloring where both vertices have the same new color class and are removed from the one they belonged
    to

    :param coloring: current coloring
    :param vertex1: vertex to be in the separate color
    :param vertex2: vertex to be in the separate color
    :return: a new coloring with vertex1 and vertex2 together as a new color class
    """
    new_coloring = coloring.copy()
    new_color = new_coloring.next_color()
    new_coloring.recolor(vertex1, new_color)
    new_coloring.recolor(vertex2, new_color)
    return new_coloring


def has_same_color_neighbours(u: Vertex, v: Vertex, coloring: Coloring) -> bool:
    """
    Returns whether the vertices u and v have the same colored neighbourhood for the given coloring

    :param u: vertex of which the neighbourhood must be compared
    :param v: vertex of which the neighbourhood must be compared
    :param coloring: current coloring
    :return: `True` if the vertices have the same colored neighbourhood, `False` otherwise
    """
    ncolors_u = [coloring.color(w) for w in u.neighbours]
    ncolors_v = [coloring.color(w) for w in v.neighbours]
    return compare(ncolors_u, ncolors_v)


def choose_color(coloring: Coloring) -> List[Vertex]:
    """
    Returns a partition cell (aka color class) with at least four vertices

    Returns the first color class with at least four vertices that is found.
    :param coloring: current coloring
    :return: a color class with at least four vertices, `None` if no color class could be found
    """
    for key in coloring.colors:
        vertices = list(coloring.get(key))
        if len(vertices) >= 4 and len(vertices) % 2 == 0:
            return vertices
    return []


def choose_vertex(color: List[Vertex], g: Graph) -> Vertex:
    """
    Returns a vertex of graph g which is in the given color class

    Returns the first vertex of graph g in the color.
    :param color: color class from which the vertex must be chosen
    :param g: graph of which the vertex must be a part of
    :return: a vertex of graph g in the color class, `None` if no vertex of graph g could be found
    """
    for vertex in color:
        if vertex.in_graph(g):
            return vertex
    return None


# TODO: Do we really want a function for this?
def get_vertices_of_graph(color: List[Vertex], g: Graph) -> List[Vertex]:
    """
    Returns the vertices of graph g in the given color class

    :param color: color class from which the vertices must be retrieved
    :param g: graph of which the vertices must be a part of
    :return: a list of vertices belonging to graph g in the given color class. The list is empty if no vertices of graph
    g are found in the given color class
    """
    return [v for v in color if g in v.graphs]


def are_twins(u: Vertex, v: Vertex) -> bool:
    """
    Returns whether the two given vertices are twins

    Two vertices are twins if they have the same neighbourhood except the other vertex.
    :param u: vertex
    :param v: vertex
    :return: `True` if the vertices are twins, `False` otherwise
    """
    N_u = [x for x in u.neighbours if x != v]
    N_v = [x for x in v.neighbours if x != u]
    return compare(N_u, N_v, lambda vertex: vertex.label)


# TODO: get_modules
def get_twins(g: Graph):  # -> List[(Vertex, Vertex)], List[(Vertex, Vertex)]:
    """
    Returns a list of true twins and a list of false twins

    :param g: graph for which the (false) twins need to be determined
    :return: arg1: a list of tuples of vertices containing the true twins
             arg2: a list of tuples of vertices containing the false twins
    """
    twins = list()
    false_twins = list()
    for u in g.vertices:
        for v in g.vertices:
            if v.label > u.label:
                if u.is_adjacent(v) and are_twins(u, v):
                    twins.append((u, v))
                if compare(u.neighbours, v.neighbours, lambda vertex: vertex.label):
                    false_twins.append((u, v))
    return twins, false_twins


def initialize_coloring(g: Graph) -> Coloring:
    """
    Creates an initial coloring for graph g where the vertices with the same degree are in the same color class

    :param g: graph on which the coloring needs to be applied
    :return: an initial coloring of graph g by degree
    """
    coloring = Coloring()
    for v in g.vertices:
        coloring.set(v.degree, v)
    debug('Init coloring ', coloring)
    return coloring


def get_unit_coloring(g: Graph) -> Coloring:
    """
    Creates a coloring of graph g where all vertices are in the same color class

    :param g: graph on which the coloring needs to be applied
    :return: an initial coloring of graph g with all vertices in the same color class
    """
    coloring = Coloring()
    for v in g.vertices:
        coloring.set(0, v)
    debug('Init coloring ', coloring)
    return coloring


def generate_neighbour_count_with_color(graph, current_color):
    counter = {}
    for v in graph.vertices:
        count = 0
        for x in v.neighbours:
            if x.colornum is current_color:
                count += 1
        if v.colornum not in counter.keys():
            counter[v.colornum] = {}
        counter[v.colornum].update({v: count})
    return counter
