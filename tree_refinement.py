from collections import defaultdict
from typing import List

from color_refinement_helper import group_by
from graph import Graph, Vertex


def tree_isomorphism(g: Graph, h: Graph, modules: [[Vertex]] = None) -> bool:
    """
    Checks if Tree g and Tree h are isomorphic
    :param modules: list of modules for graph g and h
    :param g: Graph
    :param h: Graph
    :return: Boolean whether they are isomorphic
    """
    # Make all the vertices have the correct attributes
    g = initialize_tree(g)
    h = initialize_tree(h)
    # Initialize module values
    counter = len(g.vertices)
    if modules:
        for module in modules:
            for v in module:
                v.value = counter
            counter += 1
    # Get the root for the trees
    root_g = choose_a_root(g)
    root_h = choose_a_root(h)

    # Assign the levels and get the level lists
    assign_levels(root_g)
    assign_levels(root_h)
    level_dict_g = group_by(g.vertices, lambda v: v.level)
    level_dict_h = group_by(h.vertices, lambda v: v.level)
    # Modules must have the same level
    if modules:
        for module in modules:
            level = module[0].level
            for v in module:
                if v.level != level:
                    return False
    # Gets the lowest level in the tree and since we assume isomorphism the dict which is used does not matter
    lowest_level = max(level_dict_g)
    if max(level_dict_h) != lowest_level:
        return False
    # Loop through the levels
    if max(level_dict_h) != lowest_level:
        return False

    while lowest_level > 0:
        tuples_g, d_g = set_tuples(level_dict_g[lowest_level - 1])
        tuples_h, d_h = set_tuples(level_dict_h[lowest_level - 1])
        sorted_t_g = sorted(tuples_g)
        sorted_t_h = sorted(tuples_h)
        # If the sorted tuples are not identical it is not an isomorphism
        if sorted_t_g != sorted_t_h:
            return False
        # Assign a value to the vertices of the level that is considered
        value = 1
        for t in sorted(d_g):
            for v in d_g[t]:
                if v.value is None:
                    v.value = value
            for v in d_h[t]:
                if v.value is None:
                    v.value = value
            value += 1
        lowest_level -= 1
    # Modules should all have the same tuple, just like roots
    if modules:
        for module in modules:
            tuples = module[0].tuples
            for v in module:
                if v.tuples != tuples:
                    return False
    # If the roots have the same tuple the trees are isomorphic
    return sorted(root_g.tuples) == sorted(root_h.tuples)


def choose_a_root(g: Graph) -> Vertex:
    """
    Determines the root for a tree that cuts the tree most in half, which is unique for a tree, so this should
    result in the same root for both tree
    :param g: Graph
    :return: Root
    """
    # Choose a vertex to be the root (arbitrarily)
    arb_root = g.vertices[0]
    # Assign weights of the induced subgraphs
    set_weight(arb_root)
    # Retrieve the root by shifting
    return shift(arb_root, g.order)


def set_weight(root: Vertex, parent: Vertex = None):
    """
    Recursively assigns weights to the induced subgraphs starting with the root
    :param root: Vertex
    :param parent: The parent of the root, because those do not count in the weight of a subgraph
    :return:
    """
    if root.degree == 1 and root.neighbours[0] == parent:
        root.weight = 1
        return 1
    else:
        for n in root.neighbours:
            if n != parent:
                root.weight += set_weight(n, root)
        root.weight += 1
        return root.weight


def shift(vertex: Vertex, amount_verts: int) -> Vertex:
    """
    Returns the Vertex that is the root for this tree
    :param vertex: the vertex we want to shift
    :param amount_verts: the amount of vertices in the graph [invariant]
    :return:
    """
    # If no neighbour of u has weight > n/2, return u
    result = vertex
    for n in vertex.neighbours:
        if n.weight > amount_verts / 2:
            vertex.weight = vertex.weight - n.weight
            n.weight = vertex.weight + n.weight
            result = shift(n, amount_verts)
    return result


def assign_levels(root: Vertex, parent: Vertex = None, level: int = 0):
    """
    Assigns to a vertex the depth (in the algorithm called level, however our root = 0 instead of the max level)
    :param root: The root of the tree
    :param parent: The parent of the root (for the root of the tree this is None)
    :param level: The level that needs to be assigned to the root
    :return: Nothing because everything is assigned to the vertices
    """
    if root.level is None:
        root.level = level
    level += 1
    for n in root.neighbours:
        if n.level is None:
            n.level = level
        if n != parent:
            root.children.append(n)
            assign_levels(n, root, level)


def initialize_tree(g: Graph):
    """
    The tree isomorphic algorithm and the root detection need certain attributes that are initialized here
    :param g: Graph
    :return: Nothing because everything is assigned to the vertices
    """
    for v in g.vertices:
        v.weight = 0
        v.level = None
        v.children = []
        v.value = None
        v.tuples = []
        # Assign all leaves integer 0
        if v.degree == 1:
            v.value = 0
    return g


def set_tuples(vertices: List[Vertex]):
    """
    Creates the tuples based on the value of its children and a mapping between the tuples and the vertices
    :param vertices: The vertices of the level
    :return: List of the tuples the are on this level and a dictionary tuples: vertices
    """
    tuples = []
    d = defaultdict(list)
    for v in vertices:
        for n in v.children:
            v.tuples.append(n.value)
        if v.value != 0:
            tuples.append(sorted(v.tuples))
            d[tuple(sorted(v.tuples))].append(v)
    return tuples, d
