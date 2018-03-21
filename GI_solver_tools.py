from graph_io import *
from mygraph import *


def load_file(file: str):
    with open(file) as f:
        graphs = load_graph(f, read_list=True)
        return graphs[0]


def write_file(G):
    with open('colorful.dot', 'w') as f:
        write_dot(G)


def solve(old: List[Graph], colorlist: list()):
    new_graph = preprocess(old)
    new_colornums_list = colorlist
    new_colornums_list.append(get_colornums(new))
    return is_omorph(h)


def preprocess(g: List[Graph], colorlist: list()):
    h = assign_colornums(g)
    return h

def get_colornums(g: Graph):
    colorlist = []
    for v in g.vertices:
        colorlist.append(v.colornum)
    return colorlist


def unique_colornums(g: Graph):
    colornums = get_colornums(g)
    if len(colornums) == len(set(colornums)):
        return True
    return False


def assign_colornums(g: List[Graph]):
    for graph in g:
        if unique_colornums(graph):
            return g
        for v in graph.vertices:
            if v.colornum is None:
                v.colornum = v.degree
    return g


def is_omorph(g: List[Graph], list_colornums_old: list()):
    assign_colornums()
    list_colornums_old.append(get_colornums(graph))
