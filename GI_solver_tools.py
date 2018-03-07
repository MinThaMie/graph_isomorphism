from graph_io import *
from mygraph import *


def load_file(file: str):
    with open(file) as f:
        graphs = load_graph(f, read_list=True)
        return graphs[0]


def write_file(G):
    with open('colorful.dot', 'w') as f:
        write_dot(G)


def give_colornums(g: List[Graph], init: bool):
    for graph in g:
        if init:
            for v in graph.vertices:
                v.colornum = v.degree
                init = False
        else:
            for v in graph.vertices:
                print('isomorphic!')


def solve(g: List[Graph]):
    give_colornums(g, True)
