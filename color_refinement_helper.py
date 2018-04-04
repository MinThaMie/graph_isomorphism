"""
Module with helper methods for the Color Refinement Algorithm
"""
from typing import Iterable

from coloring import *
from permv2 import Permutation
from basicpermutationgroup import compute_orbit, stabilizer

DEBUG = False


def debug(*args):
    """
    Prints debug statements when DEBUG is set to `True`

    :param args: argument to be printed
    """
    if DEBUG:
        print(*args)


def compare(s: Iterable, t: Iterable, key=None) -> bool:
    """Compare 2 iterables and will do so on the sorted list.

    :param Iterable s: One iterable to compare
    :param Iterable t: Another iterable to compare
    :param key: Key on which to compare the iterables' contents on, e.g. Vertex.label or a lambda function.
    :return: `True` if the iterables' contents are the same; `False` otherwise.
    """
    return sorted(s, key=key) == sorted(t, key=key)


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
    n_u = [x for x in u.neighbours if x != v]
    n_v = [x for x in v.neighbours if x != u]
    return compare(n_u, n_v, lambda vertex: vertex.label)


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
        coloring.set(v, v.degree)
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
        coloring.set(v, 0)
    debug('Init coloring ', coloring)
    return coloring


def generate_neighbour_count_with_color(coloring: Coloring, current_color: int) -> {}:
    """
    This methode creates a mapping from a vertex to the amount of neighbours with current_color.
    :param coloring: coloring used for the counting of the neighbours
    :param current_color: the color which is used to refine the graph
    :return: mapping of colors to a vertex-neighbour_count mapping, the vertex-neighbour_count mapping
                is a dictionary which maps vertices to the amount of neighbours with current_color
    """
    counter = {}
    for v in coloring.vertices:
        count = 0
        for x in v.neighbours:
            if coloring.color(x) is current_color:
                count += 1
        if coloring.color(v) not in counter.keys():
            counter[coloring.color(v)] = {}
        counter[coloring.color(v)].update({v: count})
    return counter

  
def group_by(obj, group_rule=None) -> dict:
    """
    Group the given object according to the given key.

    Eg. group_by(List[int]) groups by number
    Eg. group_by(List[Vertex], key=Vertex.degree) groups by vertex degree
    Eg. group_by(dict{List}, key=lambda x:len(x)) groups by length of the lists
    :param obj: Object over which one can iterate
    :param group_rule: Rule to use for grouping, if not set `lambda x:x` is used
    :return: A dict in which the elements of 'obj' are grouped by results of the 'group_rule'
    """
    d = {}
    if not group_rule:
        for elem in obj:
            d.setdefault(elem, []).append(elem)
    else:
        for elem in obj:
            key = group_rule(elem)
            d.setdefault(key, []).append(elem)
    return d


def member_of(f: Permutation, H: [Permutation]) -> bool:
    alpha = 0
    beta = f.P[alpha]
    # compute orbit, transversal and stabalizer for given alpha
    orb, transversal = compute_orbit(H, alpha, return_transversal=True)
    if beta not in orb:
        return False
    stab_alpha = stabilizer(H, alpha)

    u = transversal[beta]
    # p = permutation(n=len(u), cycles=u)
    u_inverse = u.__neg__()
    perm = u_inverse.__mul__(f)

    if perm.P[alpha] == beta:
        return True
    else:
        return member_of(perm, stab_alpha)

# def member_of(orbit, transversal: [], cycle: permutation, permutations: set(permutation)) -> bool:
#     # cycle = (Vertex, Vertex)
#     from_Vertex, to_Vertex = cycle
#     perm = transversal[to_Vertex].__mul__(permutation)
#     return perm in Stabilizer(permutations, cycle)