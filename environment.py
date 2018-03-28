import os

import time

import datetime

from color_refinement import get_number_automorphisms, is_isomorphisms, count_isomorphism
from graph_io import load_graph

PATH_BRANCHING = 'graphs/branching'
PATH_COLORREF = 'graphs/colorref'
PATH_TREEPATHS = 'graphs/treepaths'
OUTPUT_FORMAT = '{:10} {:>15} {:>25} {:>15} {:>25} {:>25}'
OUTPUT_PATH = 'export/result'


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
    result = create_titles(file)
    for i in range(len(graphs)):
        iso_start = time.time()
        isomorphs = get_isomorphs(graphs)
        iso_time = time.time() - iso_start
        auto_start = time.time()
        automorphs = get_number_automorphisms(graphs[i])
        auto_time = time.time() - auto_start
        total_time = auto_time + iso_time
        subresult = OUTPUT_FORMAT.format(graphs[i].name, isomorphs, iso_time, automorphs, auto_time, total_time)
        result += result + '\n' + subresult
        print(subresult)
    export_result(result)


def create_titles(file):
    title = '====================================\n' \
            + file.rsplit('/', 1)[1]\
            + '\n' + '====================================\n' \
            + OUTPUT_FORMAT.format('graph', 'automorphs', 'autotime', 'isomorphs', 'isotime', 'totaltime') + '\n'\
            + '--------------------------------------------------------------------\n'
    return title


def export_result(result):
    output_file = open('result_' + str(round(time.time())), 'w')
    output_file.write(result)
    output_file.close()


if __name__ == "__main__":
    main()
