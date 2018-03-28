import os

import time

from color_refinement import get_number_automorphisms, is_isomorphisms, count_isomorphism
from graph_io import load_graph

PATH_BRANCHING = 'graphs/branching'
PATH_COLORREF = 'graphs/colorref'
PATH_TREEPATHS = 'graphs/treepaths'
OUTPUT_FORMAT = '{:10} {:>15} {:>25} {:>15} {:>25} {:>25}'


def main():
    graphs = find_graphs()
    process_data(graphs)


def find_graphs():
    branching_graphs = [PATH_BRANCHING + '/' + file for file in os.listdir(PATH_BRANCHING)]
    colorref_graphs = [PATH_COLORREF + '/' + file for file in os.listdir(PATH_COLORREF)]
    treepath_graphs = [PATH_TREEPATHS + '/' + file for file in os.listdir(PATH_TREEPATHS)]
    # return branching_graphs + colorref_graphs + treepath_graphs
    return colorref_graphs


def process_data(graphs):
    for file in graphs:
        graphs = get_graphs_from_file(file)
        process_graphs(file, graphs)


def get_graphs_from_file(file):
    with open(file) as f:
        L = load_graph(f, read_list=True)
    return L[0]


def process_graphs(file, graphs):
    export(create_titles(file))
    for i in range(len(graphs)):
        auto_start = time.time()
        automorphs = get_number_automorphisms(graphs[i])
        auto_time = time.time() - auto_start
        isomorphs = []
        iso_start = time.time()
        for j in range(len(graphs)):
            if j > i:
                isomorph = is_isomorphisms(graphs[i], graphs[j])
                num = count_isomorphism(graphs[i], graphs[j])
                #TODO gaat het om de totale serie vergelijken? Want dan kan er efficiënter gekozen worden: niet alle grafen vergelijken, maar alleen die nog niet vergeleken zijn. Als de rest al iso/auto (wat is wat?) is, zijn die dus sowieso al wel/niet gelijk aan elkaar
                print(graphs[i].name, 'and', graphs[j].name, 'isomorphic?', isomorph)
                print('There are', num, 'isomorphisms')

        iso_time = time.time() - iso_start
        total_time = auto_time + iso_time
        export(OUTPUT_FORMAT.format(graphs[i].name, automorphs, auto_time, isomorphs, iso_time, total_time))


def create_titles(file):
    title = '====================================\n' \
            + file.rsplit('/', 1)[1]\
            + '\n' + '====================================\n' \
            + OUTPUT_FORMAT.format('graph', 'automorphs', 'autotime', 'isomorphs', 'isotime', 'totaltime') + '\n'\
            + '--------------------------------------------------------------------\n'
    return title


def export(string):
    print(string)


if __name__ == "__main__":
    main()
