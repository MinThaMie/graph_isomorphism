from graph_io import *
from graphingable import *


def load_file(file: str):
    with open(file) as f:
        graphs = load_graph(f, read_list=True)
        return graphs[0]


def write_file(G):
    with open('colorful.dot', 'w') as f:
        write_dot(G, f)


def solve(g: list()) -> list():
    h = preprocess(g)
    old_colorlist = get_colornums(h)
    refine(h, old_colorlist)


def preprocess(g: list()) -> list():
    preprocessesed_graphs = assign_primary_colornums(g)
    return preprocessesed_graphs


def assign_primary_colornums(g: list()) -> list():
    for graph in g:
        for vertex in graph.vertices:
            vertex.colornum = vertex.degree
    return g


def get_colornums(g: list()) -> list():
    colorlist = []
    for graph in g:
        graph_colornums = []
        for vertex in graph:
            graph_colornums.append(vertex.colornum)
        colorlist.append(graph_colornums)
    return colorlist


def is_omorph(g: list()) -> bool:
    graph1 = g[0]
    graph2 = g[1]
    if graph1 == graph2:
        return True
    return False


def refine(g: list(), old_colorlist: list()) -> list():
    if not is_omorph(g):
        old_colorlist
