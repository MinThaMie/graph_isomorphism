from graph_io import *
from mygraph import *


def load_file(file: str):
    with open(file) as f:
        graphs = load_graph(f, read_list=True)
        return graphs[0]


def write_file(G):
    with open('colorful.dot', 'w') as f:
        write_dot(G, f)


def solve(g: list()):
    h = preprocess(g)
    old_colorlist = get_colornums(h)
    check_for_isomorphism(h, old_colorlist)


def preprocess(g: list()):
    processes_graph = assign_primary_colornums(g)
    return processes_graph


def assign_primary_colornums(g: list()):
    for graph in g:
        for vertex in graph.vertices:
            vertex.colornum = vertex.degree
    return g


def get_colornums(g: list()):
    colorlist = []
    for graph in g:
        graph_colornums = []
        for vertex in graph:
            graph_colornums.append(vertex.colornum)
        colorlist.append(graph_colornums)
    return colorlist


def check_for_isomorphism(g: list(), old_colorlist: list()):
    pass
