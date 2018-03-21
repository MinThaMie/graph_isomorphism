"""
This is a module for the color refinement algorithm
version: 20-3-18, Claudia Reuvers & Dorien Meijer Cluwen
"""

import time
from graph_io import *
from coloring import *
from tools import *
from color_refiment_helper import *

PATH = './graphs/treepaths/'
GRAPH = 'threepaths320.gr'


def color_refine(coloring: "Coloring"=None) -> "Coloring":
    """
    Color Refinement Algorithm

    Returns a stable coloring based on the input coloring.
    #TODO: Also add how it does it?
    :param coloring: Initial coloring
    :return: A stable coloring alpha_i of G
    """
    #TODO: Make recursive like Claudia's version?
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
                    if identical_colored_neighborhood(u, v, coloring):
                        new_coloring.set(new_color, v)
                        vertices.remove(v)
                        unbalanced = not unbalanced
            # Check if coloring is unbalanced, then we must stop
            if unbalanced: #len(new_coloring.get(new_color)) == 1: #TODO 1 or odd?
              debug('Coloring is unbalanced')
              return new_coloring

        debug('New coloring ', new_coloring)
        has_changed = (coloring.num_colors != new_coloring.num_colors)
        coloring = new_coloring


    debug('No changes found')

    return coloring


def isomorphic(G: "Graph", H: "Graph"):
    """
    Determine if G and H are isomporhic (using color refinement)
    :param G: Graph G
    :param H: Graph H
    :return: graph G + H, True/False/None (if they are (not) isomorph or maybe)
    """
    g2 = G + H
    coloring = color_refine(get_degree_coloring(g2))

    # Determine isomorphism
    status = coloring.status(G,H)
    if status == "Bijection":
        return g2, True
    elif status == "Unbalanced":
        return g2, False
    else:
        return g2, None


def count_isomorphism(g: "Graph", h: "Graph", coloring: "Coloring"=None, count=True):
    """
    Returns the number of isomorphisms from G to H using branching and color refinement for the given coloring.
    :param g: Graph G
    :param h: Graph H
    :param coloring: Initial coloring
    :param count: True if want to count the number of isomorphisms, otherwise stop as soon as one is found
    :return: The number of isomorphisms from G to H that follow the given coloring
    """
    graph = g + h
    # Initialize coloring (if needed) #TODO: Do here or in get_number_isomorphisms?
    if coloring is None:
        coloring = get_degree_coloring(graph)

    # Refine the initial coloring
    coloring = color_refine(coloring)
    coloring_status = coloring.status(g, h)

    if coloring_status == "Bijection":
        return 1
    if coloring_status == "Unbalanced":
        return 0

    # Choose a color class C with |C| >= 4
    # TODO use partion and choose_vertex methods
    num = 0
    for color in coloring.colors:
        vertices = coloring.get(color)
        if len(vertices) >= 4:
            vertices_in_g = [v for v in vertices if v.in_graph(g)]
            vertices_in_h = [v for v in vertices if v.in_graph(h)]

            # Choose an x st. x in C and x in V(G)
            x = vertices_in_g[0]
            for y in vertices_in_h:
                # Give x and y a new color (give rest the same color as they had)
                # TODO use create_partition method?
                new_coloring = coloring.copy()
                new_color = new_coloring.next_color()
                new_coloring.recolor(x, new_color, color=color)
                new_coloring.recolor(y, new_color, color=color)
                num += count_isomorphism(g,h,new_coloring)
                if not count and num > 0:
                    return num
            break
    return num


def are_isomorphic(G: "Graph", H: "Graph"):
    if count_isomorphism(G, H, count=False) > 0:
        return True
    return False


def get_number_isomorphisms(g: "Graph", h: "Graph") -> int:
    """
    Returns the number of isomorphisms for graph g and h.

    First, the coloring is initialized by degree of the vertices. Next, the number of isomorphisms is counted by
    applying the color-refinement algorithm and branching the
    :param g: graph for which to determine the number of isomorphisms
    :param h: graph for which to determine the number of isomorphisms
    :return: The number of isomorphisms for graph g and h
    """
    # Preprocess #TODO: Add preprocess methods
    if len(g) != len(h) or len(g.edges) != len(h.edges):
        return 0

    coloring = get_degree_coloring(g+h) #TODO: Do here or in count_isomporphism?
    start = time.time()
    num = count_isomorphism(g, h, coloring)
    print('There are', num, 'isomorphisms')
    print('Took', time.time() - start, 'seconds\n')
    return num


def get_number_automorphisms(g: "Graph") -> int:
    """
    Returns the number of automorphisms of graph g.

    Applies the GI-problem to itself.
    :param g: graphs for which to determine the number of isomorphisms
    :return: The number of automorphisms for graph g
    """
    return get_number_isomorphisms(g, g.deepcopy())


if __name__ == "__main__":
    with open(PATH + GRAPH) as f:
        L = load_graph(f,read_list=True)

    graphs = L[0]

    for i in range(len(graphs)):
        for j in range(len(graphs)):
            if j == i:
                start= time.time()
                num = get_number_automorphisms(graphs[i])
            if j > i:
                start = time.time()
                G, isomorph = isomorphic(graphs[i], graphs[j])
                print(graphs[i].name,'and',graphs[j].name,'isomorphic?',isomorph)
                num = count_isomorphism(graphs[i], graphs[j])
                print('There are',num,'isomorphisms')
                print('Took',time.time()-start,'seconds\n')

    # with open('graphs/colorful.dot','w') as f:
    #     write_dot(G,f)

