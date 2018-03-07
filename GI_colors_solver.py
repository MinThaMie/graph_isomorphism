from mygraph import *
from graph_io import *

WRITE_DOT_FILES = True


def load_file():
    with open('colorref_smallexample_2_49.grl') as f:
        L = load_graph(f, read_list=True)
    G = L[0][0]
    H = L[0][1]
    print(G)
    print(H)


for v in G.vertices:
    v.colornum = v.degree
