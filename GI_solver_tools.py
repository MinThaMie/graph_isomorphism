from graph_io import *
from mygraph import *


def load_file(file: str):
    with open(file) as f:
        graphs = load_graph(f, read_list=True)
        return graphs[0]


def write_file(G):
    with open('colorful.dot', 'w') as f:
        write_dot(G)


def solve(G: list):
    H = preprocess(G)
    old_colorlist = get_colornums(H)
    check_for_isomorphism(H, old_colorlist)


def preprocess(G):
    processes_graph = assign_primary_colornums(G)


def assign_primary_colornums(G):
    for graph in G:
        for vertex in graph.vertices:
            vertex.colornum = vertex.degree


def get_colornums(H):
    pass


def check_for_isomorphism(H, old_colorlist):
    pass
