from graph_io import *
from graph import *


def load_file(file: str):
    with open(file) as f:
        graphs = load_graph(f, read_list=True)
        return graphs[0]


def write_file(G):
    with open('colorful.dot', 'w') as f:
        write_dot(G, f)


def solve(g: list(), graphs_preprocessed: list()) -> list():
    for i in range(len(g)):
        for j in range(len(g)):
            if i is not j:
                if i not in graphs_preprocessed:
                    preprocess(g[i])
                    graphs_preprocessed.append(i)
                if j not in graphs_preprocessed:
                    preprocess(g[j])
                    graphs_preprocessed.append(j)
                refine(g[i], g[j])


def preprocess(g: "Graph") -> Graph:
    g = assign_primary_colornums(g)
    return g


def assign_primary_colornums(g: "Graph") -> Graph:
    for vertex in g.vertices:
        vertex.colornum = vertex.degree
    return g


def get_colornums(g: Graph) -> list():
    graph_colornums = []
    for vertex in g:
        graph_colornums.append(vertex.colornum)
    graph_colornums.append(graph_colornums)
    return graph_colornums


def is_omorph(g: "Graph", h: "Graph") -> bool:
    return False  # TODO check for isomorphism


def refine(g: "Graph", h: "Graph") -> Tuple["Graph", "Graph"]:
    if not is_omorph(g, h):
        return g, h


def deepcopy_graph(g: "Graph") -> "Graph":
    deepcopy = []
    for element in g.vertices:
        deepcopy.append(element)
    return deepcopy
