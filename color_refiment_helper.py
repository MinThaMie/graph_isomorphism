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
    # new_coloring = {}
    # new_partition = list()
    # new_partition.append(vertex1)
    # new_partition.append(vertex2)
    # new_coloring[0] = new_partition
    # for key in old_coloring.keys():
    #     vertices = list(old_coloring[key])
    #     if vertex1 in vertices:
    #         vertices.remove(vertex1)
    #         vertices.remove(vertex2)
    #     new_coloring[key + 1] = list(vertices)
    # return new_coloring
    new_coloring = old_coloring.copy()
    new_color = new_coloring.next_color()
    new_coloring.recolor(vertex1, new_color)
    new_coloring.recolor(vertex2, new_color)
    return new_coloring

# DEPRECATED by get_degree_coloring
# def initialize_coloring(g: "Graph") -> "Coloring":
#     """
#     Creates an initial coloring where the vertices with the same degree are in the same partition.
#
#     :param g: graph on which the coloring needs to be applied
#     :return: an initial coloring of graph g
#     """
#     # coloring = {}
#     # for vertex in g.vertices:
#     #     if vertex.degree not in coloring.keys():
#     #         coloring[vertex.degree] = []
#     #     coloring[vertex.degree].append(vertex)
#     # return coloring
#     return get_degree_coloring(g)



def has_same_color_neignhours(u: "Vertex", v: "Vertex", coloring: "Coloring") -> bool:
    """
    Returns whether the vertices u and v have the same colored neighbourhood for the given coloring.

    :param u: vertex of which the neighbourhood must be compared
    :param v: vertex of which the neighbourhood must be compared
    :param coloring: coloring
    :return: `True` if the vertices have the same colored neighbourhood, `False` otherwise
    """
    return identical_colored_neighborhood(u,v,coloring)
    # color_u = [find_key(w, coloring) for w in u.neighbours]
    # color_v = [find_key(w, coloring) for w in v.neighbours]
    # return Counter(color_u) == Counter(color_v)


def find_key(value, dictionary: "dict"):
    """
    Returns the key of the value for the given dictionary.

    :param value: value to find the key of
    :param dictionary: dictionary with key,value-pairs in which to search
    :return: Returns the key of the given value, returns `None` if no key can be found
    """
    for key in dictionary.keys():
        if value in dictionary[key]:
            return key
    return None


def is_unbalanced(coloring: "Coloring") -> bool:
    """
    Returns whether the coloring is balanced.

    The coloring is balanced if all partitions have a even number of vertices.
    :param coloring:
    :return: `True` if the coloring is unbalanced, `False` if the coloring is balanced
    """
    for k in coloring.colors:
        values = coloring.get(k)
        if (len(values) % 2) == 1:
            return True
    return False


def is_bijection(coloring: "Coloring") -> bool:
    """
    Returns whether the coloring defines a bijection.

    A coloring defines a bijection if all colors are appear only one time in one graph, and one time in the other. So,
    if all partitions contain two vertices. By definition of the color-refinement algorithm, it is not possible that a
    partition with two vertices are both in the same graph.
    :param coloring:
    :return: `True` if the coloring defines a bijection, `False` otherwise
    """
    for key in coloring.colors:
        values = coloring.get(key)
        if len(values) != 2:
            return False
    return True


def choose_partition(coloring: "Coloring") -> List["Vertex"]:
    """
    Selects a partition with at least four vertices.

    Returns the first partition with at least four vertices that is found.
    :param coloring:
    :return: a partition with at least four vertices, `None` if no partition could be found
    """
    for key in coloring.colors:
        values = list(coloring.get(key))
        if len(values) >= 4 and len(values) % 2 == 0:
            return values
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
        if g in vertex.graphs:
            return vertex
    return None


def get_vertices_of_graph(partition: List["Vertex"], g: "Graph") -> List["Vertex"]:
    """
    Returns the vertices of graph g in the given partition.

    :param partition:
    :param g:
    :return: a list of vertices belonging to graph g in the given partition. The list is empty if no vertices of graph g
    are found in the given partition
    """
    vertices = list()
    for v in partition:
        if g in v.graphs:
            vertices.append(v)
    return vertices
    #Same as `return [v for v in partition if g in v.graphs]
    #Or equivalently [v for v in partion if v.in_graph(G)]



def is_twins(u: "Vertex", v: "Vertex") -> bool:
    N_u = u.neighbours
    N_u.remove(v)
    N_v = v.neighbours
    N_v.remove(u)
    return Counter(N_u) == Counter(N_v)


def get_twins(g: "Graph"):  # -> List[("Vertex", "Vertex")]:
    twins = list()
    false_twins = list()
    for u in g.vertices:
        for v in g.vertices:
            if v.label > u.label:
                if u.is_adjacent(v) and is_twins(u, v):
                    twins.append((u, v))
                if Counter(u.neighbours) == Counter(v.neighbours):
                    false_twins.append((u, v))
    return twins, false_twins



def identical_colored_neighborhood(u: "Vertex", v: "Vertex", coloring: "Coloring"):
    ncolors_u = [coloring.color(w) for w in u.neighbours]
    ncolors_v = [coloring.color(w) for w in v.neighbours]
    return compare(ncolors_u, ncolors_v)


def get_degree_coloring(graph: "Graph"):
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
