from graph_io import *
from collections import Counter
from graph import *
from coloring import *
from colour_refinement_dorien import *
from color_refiment_helper import *


def count_isomorphism(g: "Graph", h: "Graph", coloring: "Coloring") -> int:
    """
    Returns the number of isomorphisms of graph g and h for a given stable coloring. #Is the starting coloring always stable?

    If the coloring is unbalanced, it will return 0.
    If the coloring defines a bijection, it will return 1.
    If neither applies, a partition is chosen from which a vertex of graph g is mapped to all possible vertices of graph
    h in the same partition. For each mapping, the number of isomorphisms is calculated and summed. #You normally tell what the method does, not how
    :param g: first graph to compare
    :param h: second graph to compare
    :param coloring: stable coloring of graph g and h
    :return: the number of isomorphisms of graph g and h for a given coloring
    """
    new_coloring = color_refinement(coloring)
    if is_unbalanced(new_coloring):
        return 0
    if is_bijection(new_coloring):
        return 1
    partition = choose_partition(new_coloring)
    first_vertex = choose_vertex(partition, g)
    number_isomorphisms = 0
    for second_vertex in get_vertices_of_graph(partition, h):
        adapted_coloring = create_partition(new_coloring, first_vertex, second_vertex)
        number_isomorphisms = number_isomorphisms + count_isomorphism(g, h, adapted_coloring)
    return number_isomorphisms


def color_refinement(old_coloring: "Coloring") -> "Coloring":
    """
    Returns a stable coloring based on the input coloring.

    For each partition, the vertices in that partition are compared. If their neighbours are in the same partition, the
    vertices stay in the same partition. If not, the vertices will be put in separate partitions.
    When there is no change in the coloring, the coloring is considered stable. When the coloring is unstable, the
    color-refinement algorithm is applied again.
    :param old_coloring:
    :return: a stable coloring
    """
    new_coloring = Coloring()
    colornr = new_coloring.next_color()
    for key in old_coloring.colors:
        vertices = old_coloring.get(key) #get() does list copy
        while len(vertices) > 0:
            u = vertices.pop(0)
            # if colornr not in new_coloring.keys():
            #     new_coloring[colornr] = []
            # new_coloring[colornr].append(u)
            new_coloring.set(colornr, u)
            for v in list(vertices):
                if has_same_color_neignhours(u, v, old_coloring):
                    new_coloring.set(colornr,v)
                    vertices.remove(v)
            colornr = new_coloring.next_color()
    changed = old_coloring.num_colors != new_coloring.num_colors
    if changed:
        if is_unbalanced(new_coloring):
            return new_coloring
        return color_refinement(new_coloring)
    else:
        return new_coloring


def get_number_isomorphisms(g: "Graph", h: "Graph") -> int:
    """
    Returns the number of isomorphisms for graph g and h.

    First, the coloring is initialized by degree of the vertices. Next, the number of isomorphisms is counted by
    applying the color-refinement algorithm and branching the
    :param g: graph for which to determine the number of isomorphisms
    :param h: graph for which to determine the number of isomorphisms
    :return: The number of isomorphisms for graph g and h
    """
    if len(g) != len(h):
        return 0
    if len(g.edges) != len(h.edges):
        return 0
    added_graph = g + h
    coloring = initialize_coloring(added_graph)
    return count_isomorphism(g, h, coloring)


def get_number_automorphisms(g: "Graph") -> int:
    """
    Returns the number of automorphisms of graph g.

    Applies the GI-problem to itself.
    :param g: graphs for which to determine the number of isomorphisms
    :return: The number of automorphisms for graph g
    """
    return get_number_isomorphisms(g, g.deepcopy())

