"""
This is a module for the color refinement algorithm
version: 20-3-18, Claudia Reuvers & Dorien Meijer Cluwen
"""
import time
from typing import Dict

import preprocessing
from basicpermutationgroup import order_computation, member_of
from color_refinement_helper import *
from graph_io import *
from permv2 import Permutation
from tools import IsomorphismMapping, update_known_isomorphisms
from tree_refinement import tree_isomorphism

IsomorphismMapping = Dict[int, Set[int]]


def count_isomorphism(g: Graph, h: Graph, coloring: Coloring, count: bool = True) -> int:
    """
    Returns the number of isomorphisms of `Graph` g and h for a given coloring

    If the coloring is unbalanced, it will return 0.
    If the coloring defines a bijection, it will return 1.
    If neither applies, a color class is chosen from which a vertex of graph g is mapped to all possible vertices of
    graph h in the same color class. For each mapping, the number of isomorphisms is calculated and summed.
    :param g: first graph to compare
    :param h: second graph to compare
    :param coloring: coloring of `Graph` g and h
    :param count: if `True` the number of isomorphisms is returned, if `False` 0 is returned if no isomorphisms is found
    and 1 is returned when the first isomorphism is found
    :return: the number of isomorphisms of graph g and h for a given coloring
    """

    new_coloring = fast_color_refine(coloring)
    coloring_status = new_coloring.status(g, h)

    if coloring_status == "Unbalanced":
        return 0
    if coloring_status == "Bijection":
        return 1

    vertices = choose_color(new_coloring)
    first_vertex = choose_vertex(vertices, g)
    vertices_in_h = (v for v in vertices if v.in_graph(h))
    number_isomorphisms = 0
    for second_vertex in vertices_in_h:
        adapted_coloring = create_new_color_class(new_coloring, first_vertex, second_vertex)
        number_isomorphisms += count_isomorphism(g, h, adapted_coloring, count)

        if not count and number_isomorphisms > 0:
            return number_isomorphisms
    return number_isomorphisms


def color_refine(coloring: Coloring) -> Coloring:
    """
    Returns a stable or unbalanced coloring as a result of the basic color refinement algorithm

    For each color class, the first vertex is chosen to compare with the other vertices. If these two vertices have
    neighbours in the same color class, the vertices stay in the same color class. If their neighbourhood differs, the
    vertices will be put in different color classes.
    When the coloring does not change, it is considered stable and returned.
    Also, when the coloring is unbalanced (a color class has an odd number of vertices) it is returned.
    :param coloring: initial coloring
    :return: a stable or unbalanced coloring
    """

    has_changed = True
    while has_changed:
        new_coloring = Coloring()
        for color in coloring.colors:
            unbalanced = False

            vertices = coloring.get(color)
            while len(vertices) > 0:
                new_color = new_coloring.next_color()
                unbalanced = True
                u = vertices.pop()
                new_coloring.set(u, new_color)

                for v in list(vertices):
                    if has_same_color_neighbours(u, v, coloring):
                        new_coloring.set(v, new_color)
                        vertices.remove(v)
                        unbalanced = not unbalanced

            if unbalanced:
                debug('Coloring is unbalanced')
                return new_coloring

        debug('New coloring ', new_coloring)
        has_changed = (len(coloring) != len(new_coloring))
        coloring = new_coloring

    debug('No changes found')
    return coloring


def fast_color_refine(coloring: Coloring) -> Coloring:
    """
    The fast color refine algorithm refines a given coloring by looking at the amount of neighbours of a given color.
    A queue is used to keep track of colors for which we still have to check if they lead to refinements.
    Whenever a refining operations splits a color class C_i into new classes one of them keeps color i
    and the others receive a new unused color i_l. One or more of the new classes are then added to the queue.
    For this the following rule is used:
    1. if color 'i' is already in the queue, add all new color classes i_l to the queue as well.
    2. if color 'i' is not in the queue, add the smallest 'new' (i or one of the i_l) color class to the queue.
    The algorithm stops when the queue is empty (and starts with all current colors of the given coloring in the queue).
    : param coloring: Given coloring which needs refinement
    : return: The refined coloring of the graph
    """

    # Push the first color into the queue
    queue = DoubleLinkedList()
    for c in sorted(coloring.colors):
        queue.append(c)
    debug('Queue', queue)

    while len(queue) > 0:
        # Start refining with the first color from the queue
        current_color = queue.pop_left()
        counter = generate_neighbour_count_with_color(coloring, current_color)

        # Loop over all the colors in the graph and refine them
        for color_class in counter.keys():
            debug('Refining the following color:', color_class)
            neighbour_map = counter[color_class]

            # Partition class 'c' into cells according to #neighbours of current_color
            vertices_of_c = list(neighbour_map.keys())
            debug('Vertices of color', color_class, vertices_of_c)
            debug('Neighbours', neighbour_map)

            # Keep split_count so the first vertices you encounter are not recolored
            split_count = 0

            # Keep a list of the color_classes from this iteration so we can count them afterwards and see which one is
            # the smallest and should be added to the queue
            new_color_classes = []

            while len(vertices_of_c) > 0:
                u = vertices_of_c.pop()
                new_color = color_class

                if split_count > 0:
                    new_color = coloring.next_color()
                    coloring.recolor(u, new_color)

                for v in list(vertices_of_c):
                    n_neighbours_u = neighbour_map[u]
                    n_neighbours_v = neighbour_map[v]

                    # Compare the amount of neighbours of u with the amount of neighbours of v
                    # If they are equal u and v are in the same cell
                    # If the split count is larger then zero they should both be colored with the same color
                    if n_neighbours_u == n_neighbours_v:
                        if split_count > 0:
                            coloring.recolor(v, new_color)
                        vertices_of_c.remove(v)

                split_count += 1
                # Each color_class is added to the list
                new_color_classes.append(new_color)

            # Initialize 'largest_color' with the first color class, because this is the original color
            largest_color = new_color_classes[0]

            if split_count > 1:
                debug('New color classes:', new_color_classes)

                # If the original color is in the queue, all the other colors should be added to the queue
                if queue.find(color_class) is not None:
                    for color in new_color_classes:
                        if queue.find(color) is None:
                            queue.append(color)

                # Otherwise all the colors except the largest should be added to the queue
                else:
                    for color in new_color_classes:
                        if len(coloring.get(largest_color)) > len(coloring.get(color)):
                            if queue.find(color) is None:
                                queue.append(color)
                        else:
                            if queue.find(largest_color) is None:
                                queue.append(largest_color)
                            largest_color = color

            debug('Queue', queue)
        debug('Queue', queue)
    return coloring


def get_number_isomorphisms(g: Graph, h: Graph, coloring: Coloring, count: bool,
                            modular_decomposition_factor: int = 1) -> int:
    """
    Returns the number of isomorphisms of graph g and h

    First, it is determined if graph have potential to be isomorphic by the number of vertices and edges. Next, the
    coloring is initialized by degree of the vertices. Next, the number of isomorphisms is counted by the algorithm of
    `count_isomorphism`.
    :param coloring: initial coloring
    :param modular_decomposition_factor: modular_decomposition_factor
    :param Graph g: graph for which to determine the number of isomorphisms
    :param Graph h: graph for which to determine the number of isomorphisms
    :param count: whether the number of isomorphisms
    :return: The number of isomorphisms of graph g and h
    """
    return modular_decomposition_factor * count_isomorphism(g, h, coloring, count)


def is_isomorphisms(g: Graph, h: Graph) -> bool:
    """
    Returns whether the two graphs are isomorphic

    Uses the algorithm of `get_number_isomorphisms` with count set to `False` is used to determine the number of
    isomorphisms. When the number of isomorphisms is 0, graphs are not isomorphic. Otherwise, the graphs are isomorphic.
    :param Graph g: One graph to compare for isomorphism.
    :param Graph h: Another graph to compare for isomorphism.
    :return: `True` if graph g and h are isomorphic, `False` otherwise
    """

    if preprocessing.is_tree(g):
        if preprocessing.is_tree(h):
            return tree_isomorphism(g, h)
        else:
            return False
    elif preprocessing.is_tree(h):
        return False
    else:
        is_potential_isomorph, g, h, factor, md_iso_groups_g, md_iso_groups_h = modular_decomposition(g, h)
        if is_potential_isomorph:
            if preprocessing.is_tree(g):
                if preprocessing.is_tree(h):
                    return tree_isomorphism(g, h)
                else:
                    return False
            elif preprocessing.is_tree(h):
                return False
            else:
                md_iso_groups_g_h = [group_g + group_h for group_g, group_h in zip(md_iso_groups_g, md_iso_groups_h)]
                coloring = initialize_coloring(g + h)
                for i in range(len(md_iso_groups_g_h)):
                    coloring.add(md_iso_groups_g_h[i])

                return get_number_isomorphisms(g, h, coloring, False) > 0
        else:
            return False


def modular_decomposition(g: Graph, h: Graph) -> (bool, Graph, Graph, int, [[Vertex]], [[Vertex]]):
    md_g = graph_to_modules(g)
    md_h = graph_to_modules(h)

    if not preprocessing.is_similar_modular_decomposition(md_g, md_h):
        debug('Modular decomposition detected anisomorphism!')
        return False, md_g, md_h, 1, [], []

    # At this point, g and h must have the same MD factor
    g, modular_decomposition_factor, md_iso_groups_g = preprocessing.calculate_modular_decomposition_and_factor(g, md_g)
    h, md_iso_groups_h = preprocessing.calculate_modular_decomposition_without_factor(h, md_h)

    return True, g, h, modular_decomposition_factor, md_iso_groups_g, md_iso_groups_h


def get_number_automorphisms(g: Graph) -> int:
    """
    Returns the number of automorphisms of graph g

    The algorithm of `compute_generators` is used with graph g and a copy of graph g.
    :param g: graph for which to determine the number of automorphisms.
    :return: The number of automorphisms of graph g
    """
    copy_g = g.deepcopy()
    _, g, copy_g, factor, md_iso_groups_g, md_iso_groups_h = modular_decomposition(g, copy_g)
    md_iso_groups_g_h = [group_g + group_h for group_g, group_h in zip(md_iso_groups_g, md_iso_groups_h)]

    for idx, v in enumerate(g.vertices):
        v.set_id(idx)
    for idx, v in enumerate(copy_g.vertices):
        v.set_id(idx)

    coloring = initialize_coloring(g + copy_g)
    for i in range(len(md_iso_groups_g_h)):
        coloring.add(md_iso_groups_g_h[i])
    lastvisited = [coloring]
    generators = []
    generators, _ = compute_generators(g, copy_g, coloring, generators=generators, lastvisited=lastvisited)
    return factor * order_computation(generators)


def compute_generators(g: Graph, h: Graph, start_coloring: Coloring, generators: list() = [],
                       lastvisited: list() = list()) -> (list(), list()):
    """
    Computes a set of generators of the mapping from graph g to graph h

    (Implements the algorithm of lecture 4)
    The coloring is refined using the fast_color-refine-algorithm.
    If the coloring then defines a bijection, it is checked whether this mapping is already in the set of generators. If
    not, the permutation is added to the set. In both cases, the coloring is put back to the last visited trivial
    mapping.
    When the coloring is undecided, the coloring branches. The first pick is the trivial mapping (if possible) and the
    generating set is computed recursively. Thereafter, the non-trivial mapping is computed recursively.
    :param Graph g: graph to determine the generators from
    :param Graph h: graph to be mapped to
    :param Coloring start_coloring: an unstable coloring
    :param set generators: list of generators
    :param DoubleLinkedList lastvisited: list of lastvisited trivial mappings
    :return (list, [Coloring]): a list of generators of the mapping from graph g to h
    """
    # Do colorrefinement -> returns stable or unbalanced coloring
    is_previous_node_trivial = start_coloring in lastvisited
    new_coloring = fast_color_refine(start_coloring)
    coloring_status = new_coloring.status(g, h)
    # # No automorphism with given coloring
    if coloring_status == "Unbalanced":
        return generators, lastvisited
    # Unique automorphism
    elif coloring_status == "Bijection":
        perm_f = Permutation(len(g.vertices), coloring=new_coloring, g=g)
        # is this coloring already in the set of colorings?
        if len(generators) == 0 or not member_of(perm_f, generators):
            # put f in the set and return to last visited node
            generators.append(perm_f)
        return generators, lastvisited
    # Undecided
    else:
        # choose branching vertex x and cell C
        chosen_vertex_g, vertices = choose_color_trivial(new_coloring, g)
        if chosen_vertex_g is None:
            vertices = choose_color(new_coloring)
            chosen_vertex_g = choose_vertex(vertices, g)
        vertices_in_h = [v for v in vertices if v.in_graph(h)]
        trivial_mapping, non_trivial_mapping = get_mappings(chosen_vertex_g, vertices_in_h)
        # add this coloring to a map
        # if this coloring is not trivial: only do left branch (if there is a trivial, do trivial, else, do one of non_trivial)
        if not is_previous_node_trivial:
            if trivial_mapping is not None:
                # lastvisited[coloring] = is_trivial
                trivial_coloring = create_new_color_class(new_coloring, chosen_vertex_g, trivial_mapping)
                generators, lastvisited = compute_generators(g, h, trivial_coloring, generators=generators,
                                                             lastvisited=lastvisited)
            else:
                # lastvisited[coloring] = is_trivial
                adapted_coloring = create_new_color_class(new_coloring, chosen_vertex_g, non_trivial_mapping[0])
                generators, lastvisited = compute_generators(g, h, adapted_coloring, generators=generators,
                                                             lastvisited=lastvisited)
        # if coloring is trivial: do all branches
        else:
            if trivial_mapping is not None:
                # lastvisited[coloring] = True
                trivial_coloring = create_new_color_class(new_coloring, chosen_vertex_g, trivial_mapping)
                lastvisited.append(trivial_coloring)
                generators, lastvisited = compute_generators(g, h, trivial_coloring, generators=generators,
                                                             lastvisited=lastvisited)
                # lastvisited[coloring] = False
            for second_vertex in non_trivial_mapping:
                adapted_coloring = create_new_color_class(new_coloring, chosen_vertex_g, second_vertex)
                generators, lastvisited = compute_generators(g, h, adapted_coloring, generators=generators,
                                                             lastvisited=lastvisited)
    return generators, lastvisited


def process(graphs: List[Graph]) -> IsomorphismMapping:
    """
    Process a list of graphs to find indices into that list of isomorphic graphs.

    :param list graphs: The list of graphs to process.
    :return: An `IsomorphismMapping`, which is a mapping of graph indices to sets of isomorphic graph indices.
    """

    graph_indices = range(len(graphs))

    # Note: trivial automorphisms are never stored
    isomorphism_index_mapping = {}.fromkeys(graph_indices, set())
    automorphisms = {}

    for i in graph_indices:
        for j in graph_indices:
            if j == i:
                start = time.time()
                num = get_number_automorphisms(graphs[i])
                end = time.time()

                automorphisms[graphs[i]] = num

                debug('Graph', graphs[i].name, 'has', num, 'automorphisms')
                debug('Took', end - start, 'seconds')
                debug()

            if j > i:
                if j in isomorphism_index_mapping[i]:
                    debug(graphs[i].name, 'and', graphs[j].name, 'are already known to be isomorphic')

                else:
                    start = time.time()
                    isomorphism = is_isomorphisms(graphs[i], graphs[j])
                    end = time.time()

                    debug(graphs[i].name, 'and', graphs[j].name, 'isomorphic?', isomorphism)

                    if isomorphism:
                        isomorphism_index_mapping = update_known_isomorphisms(i, j, isomorphism_index_mapping)
                        debug('There are', automorphisms.get(graphs[i]), 'isomorphisms')

                    debug('Took', end - start, 'seconds')
                debug()

    return isomorphism_index_mapping
