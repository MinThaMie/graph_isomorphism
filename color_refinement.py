"""
This is a module for the color refinement algorithm
version: 20-3-18, Claudia Reuvers & Dorien Meijer Cluwen
"""
from color_refiment_helper import *
import time
from graph_io import *

PATH = './graphs/treepaths/'
GRAPH = 'threepaths160.gr'

def count_isomorphism(g: "Graph", h: "Graph", coloring: "Coloring", count: bool=True) -> int:
    """
    Returns the number of isomorphisms of graph g and h for a given stable coloring.

    If the coloring is unbalanced, it will return 0.
    If the coloring defines a bijection, it will return 1.
    If neither applies, a partition is chosen from which a vertex of graph g is mapped to all possible vertices of graph
    h in the same partition. For each mapping, the number of isomorphisms is calculated and summed.
    :param g: first graph to compare
    :param h: second graph to compare
    :param coloring: stable coloring of graph g and h
    :return: the number of isomorphisms of graph g and h for a given coloring
    """
    # TODO: make sure initial coloring is done
    new_coloring = color_refine(coloring)
    coloring_status = new_coloring.status(g, h)
    if coloring_status == "Unbalanced":
        return 0
    if coloring_status == "Bijection":
        return 1

    vertices = choose_color(new_coloring)
    first_vertex = choose_vertex(vertices, g)
    vertices_in_h = [v for v in vertices if v.in_graph(h)]
    number_isomorphisms = 0
    for second_vertex in vertices_in_h:
        adapted_coloring = create_partition(new_coloring, first_vertex, second_vertex)
        number_isomorphisms = number_isomorphisms + count_isomorphism(g, h, adapted_coloring, count)
        # for if you want to know if isomorphic and not number
        if not count and number_isomorphisms > 0:
            return number_isomorphisms
    return number_isomorphisms


def color_refine(coloring: "Coloring") -> "Coloring":
    """
    Do the color refinement alg.
    :param coloring: Initial coloring
    :return: The input Graph 'graph' and a stable coloring alpha_i of G
    """
    has_changed = True
    while has_changed:
        new_coloring = Coloring()
        for color in coloring.colors:
            vertices = coloring.get(color)
            while len(vertices) > 0:
                new_color = new_coloring.next_color()
                unbalanced = True
                u = vertices.pop()
                new_coloring.set(new_color, u)
                for v in list(vertices):
                    if has_same_color_neighbours(u, v, coloring):
                        new_coloring.set(new_color, v)
                        vertices.remove(v)
                        unbalanced = not unbalanced
            # Check if coloring is unbalanced, then we must stop
            if unbalanced:
                # len(new_coloring.get(new_color)) == 1:
                # TODO 1 or odd?
                debug('Coloring is unbalanced')
                return new_coloring

        debug('New coloring ', new_coloring)
        has_changed = (coloring.num_colors != new_coloring.num_colors)
        coloring = new_coloring
    debug('No changes found')
    return coloring


def get_number_isomorphisms(g: "Graph", h: "Graph", count: bool) -> int:
    """
        Returns the number of isomorphisms for graph g and h.

        First, the coloring is initialized by degree of the vertices. Next, the number of isomorphisms is counted by
        applying the color-refinement algorithm and branching the
        :param g: graph for which to determine the number of isomorphisms
        :param h: graph for which to determine the number of isomorphisms
        :param count:
        :return: The number of isomorphisms for graph g and h
        """
    if len(g) != len(h):
        return 0
    if len(g.edges) != len(h.edges):
        return 0
    added_graph = g + h
    coloring = initialize_coloring(added_graph)
    return count_isomorphism(g, h, coloring, count)


def is_isomorphisms(g: "Graph", h: "Graph") -> bool:
    """
        Returns the number of isomorphisms for graph g and h.

        First, the coloring is initialized by degree of the vertices. Next, the number of isomorphisms is counted by
        applying the color-refinement algorithm and branching the
        :param g: graph for which to determine the number of isomorphisms
        :param h: graph for which to determine the number of isomorphisms
        :return: The number of isomorphisms for graph g and h
        """
    return get_number_isomorphisms(g, h, False) > 0


def get_number_automorphisms(g: "Graph") -> int:
    return get_number_isomorphisms(g, g.deepcopy(), True)


if __name__ == "__main__":
    with open(PATH + GRAPH) as f:
        L = load_graph(f,read_list=True)

    graphs = L[0]

    for i in range(len(graphs)):
        for j in range(len(graphs)):
            if j == i:
                start= time.time()
                num = get_number_automorphisms(graphs[i])
                print('There are', num, 'automorphisms')
                print('Took', time.time() - start, 'seconds\n')
            if j > i:
                start = time.time()
                isomorph = is_isomorphisms(graphs[i], graphs[j])
                print(graphs[i].name,'and',graphs[j].name,'isomorphic?',isomorph)
                num = count_isomorphism(graphs[i], graphs[j])
                print('There are',num,'isomorphisms')
                print('Took',time.time()-start,'seconds\n')
