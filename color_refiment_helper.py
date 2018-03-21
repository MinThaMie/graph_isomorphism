"""
Module with helper methods for the Color Refinement Algorithm
"""
from tools import *
from coloring import *

def create_partition(old_coloring: "Coloring", vertex1: "Vertex", vertex2: "Vertex") -> "Coloring":
    """
    Returns a new coloring where both vertices are in a new partition and removed from the one they belonged to.

    :param old_coloring: current coloring
    :param vertex1: vertex to be in the separate partition
    :param vertex2: vertex to be in the separate partition
    :return: a new coloring with vertex1 and vertex2 as a seperate partition
    """
    new_coloring = old_coloring.copy()
    new_color = new_coloring.next_color()
    new_coloring.recolor(vertex1, new_color)
    new_coloring.recolor(vertex2, new_color)
    return new_coloring


def has_same_color_neighbours(u: "Vertex", v: "Vertex", coloring: "Coloring") -> bool:
    """
    Returns whether the vertices u and v have the same colored neighbourhood for the given coloring.

    :param u: vertex of which the neighbourhood must be compared
    :param v: vertex of which the neighbourhood must be compared
    :param coloring: coloring
    :return: `True` if the vertices have the same colored neighbourhood, `False` otherwise
    """
    ncolors_u = [coloring.color(w) for w in u.neighbours]
    ncolors_v = [coloring.color(w) for w in v.neighbours]
    return compare(ncolors_u, ncolors_v)


def choose_color(coloring: "Coloring") -> List["Vertex"]:
    """
    Selects a partition cell (aka color class) with at least four vertices.

    Returns the first partition with at least four vertices that is found.
    :param coloring:
    :return: a partition with at least four vertices, `None` if no partition could be found
    """
    for key in coloring.colors:
        vertices = list(coloring.get(key))
        if len(vertices) >= 4 and len(vertices) % 2 == 0:
            return vertices
    return []


def choose_vertex(partition: List["Vertex"], g: "Graph") -> "Vertex":
    """
    Selects a vertex of graph g which is in the given partition.

    Returns the first vertex of graph g in the partition.
    :param partition:
    :param g: graph of which the vertex must be a part
    :return: a vertex of graph g in the partition, `None` if no vertex of graph g could be found
    """
    for vertex in partition:
        if vertex.in_graph(g):
            return vertex
    return None


#TODO: Do we really want a function for this?
def get_vertices_of_graph(partition: List["Vertex"], g: "Graph") -> List["Vertex"]:
    """
    Returns the vertices of graph g in the given partition.

    :param partition:
    :param g:
    :return: a list of vertices belonging to graph g in the given partition. The list is empty if no vertices of graph g
    are found in the given partition
    """
    return [v for v in partition if g in v.graphs]


def are_twins(u: "Vertex", v: "Vertex") -> bool:
    N_u = [x for x in u.neighbours if x != v]
    N_v = [x for x in v.neighbours if x != u]
    return compare(N_u,N_v)


def get_twins(g: "Graph"):  # -> List[("Vertex", "Vertex")]:
    twins = list()
    false_twins = list()
    for u in g.vertices:
        for v in g.vertices:
            if v.label > u.label:
                if u.is_adjacent(v) and are_twins(u, v):
                    twins.append((u, v))
                if compare(u.neighbours,v.neighbours):
                    false_twins.append((u, v))
    return twins, false_twins


def initialize_coloring(graph: "Graph"):
    """
    Creates an initial coloring where the vertices with the same degree are in the same partition.

    :param graph: graph on which the coloring needs to be applied
    :return: an initial coloring of graph g by degree
    """
    coloring = Coloring()
    for v in graph.vertices:
        coloring.set(v.degree, v)
    debug('Init coloring ', coloring)
    return coloring


def get_unit_coloring(graph: "Graph"):
    coloring = Coloring()
    for v in graph.vertices:
        coloring.set(0, v)
    debug('Init coloring ', coloring)
    return coloring
