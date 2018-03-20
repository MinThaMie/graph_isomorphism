"""
This is a module for the color refinement algorithm
"""
# version: 14-3-18, Dorien Meijer Cluwen

from graph_io import *
import time
from coloring_dorien import *
from tools import *
PATH = 'graphs/branching/'
GRAPH = 'trees90.grl'


def color_refine(graph: "Graph", coloring: "Coloring"=None):
    """
    Do the color refinement alg.
    :param graph: A graph G = (V,E)
    :param coloring: Initial coloring
    :return: The input Graph 'graph' and a stable coloring alpha_i of G
    """
    # Initialize coloring (if needed)
    if coloring is None:
        coloring = get_degree_coloring(graph)

    # Refine coloring
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
              return graph, new_coloring

        debug('New coloring ', new_coloring)
        has_changed = (coloring.num_colors != new_coloring.num_colors)
        coloring = new_coloring


    debug('No changes found')

    return graph, coloring


def isomorphic(G: "Graph", H: "Graph"):
    """
    Determine if G and H are isomporhic (using color refinement)
    :param G: Graph G
    :param H: Graph H
    :return: graph G + H, True/False/None (if they are (not) isomorph or maybe)
    """
    g2, coloring = color_refine(G + H)

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
    Count the number of isomorphisms from G to H using branching and color refinement.
    :param g: Graph G
    :param h: Graph H
    :param coloring: Initial coloring
    :param count: True if want to count the number of isomorphisms, otherwise stop as soon as one is found
    :return: The number of isomorphisms from G to H that follow the initial coloring
    """
    graph = g + h
    # Initialize coloring (if needed)
    if coloring is None:
        coloring = get_degree_coloring(graph)

    # Refine the initial coloring
    graph, coloring = color_refine(graph, coloring)
    coloring_status = coloring.status(g, h)

    if coloring_status == "Bijection":
        return 1
    if coloring_status == "Unbalanced":
        return 0

    # Choose a color class C with |C| >= 4
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


def identical_colored_neighborhood(u: "Vertex", v: "Vertex", coloring: "Coloring"):
    ncolors_u = [coloring.color(w) for w in u.neighbours]
    ncolors_v = [coloring.color(w) for w in v.neighbours]
    return compare(ncolors_u, ncolors_v)


def get_degree_coloring(graph: "Graph"):
    # Initialize colors to degrees
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


if __name__ == "__main__":
    with open(PATH + GRAPH) as f:
        L = load_graph(f,read_list=True)

    graphs = L[0]

    for i in range(len(graphs)):
        for j in range(len(graphs)):
            if j > i:
                start = time.time()
                G, isomorph = isomorphic(graphs[i], graphs[j])
                print(graphs[i].name,'and',graphs[j].name,'isomorphic?',isomorph)
                num = count_isomorphism(graphs[i], graphs[j])
                print('There are',num,'isomorphisms')
                print('Took',time.time()-start,'seconds\n')

    with open('graphs/colorful.dot','w') as f:
        write_dot(G,f)

