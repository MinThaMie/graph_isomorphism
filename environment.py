import os

import time

from color_refinement import get_number_automorphisms, is_isomorphisms
from graph_io import load_graph

PATH_BRANCHING = 'graphs/branching'
PATH_COLORREF = 'graphs/colorref'
PATH_TREEPATHS = 'graphs/treepaths'
OUTPUT_FORMAT = '{:25} {:>15} {:>15} {:>15}'
OUTPUT_PATH = 'export/result'
TIME_ROUND = 5

FILE = 'graphs/colorref/colorref_smallexample_4_16.grl'


def main():
    if FILE == '':
        graph_files = find_graphs()
    else:
        graph_files = [FILE]
    process_graph_files(graph_files)


def find_graphs():
    branching_graphs = [PATH_BRANCHING + '/' + file for file in os.listdir(PATH_BRANCHING)]
    colorref_graphs = [PATH_COLORREF + '/' + file for file in os.listdir(PATH_COLORREF)]
    treepath_graphs = [PATH_TREEPATHS + '/' + file for file in os.listdir(PATH_TREEPATHS)]
    return branching_graphs + colorref_graphs + treepath_graphs


def process_graph_files(graph_files):
    for file in graph_files:
        graphs = get_graphs_from_file(file)
        process_graphs(file, graphs)


def get_graphs_from_file(file):
    with open(file) as f:
        L = load_graph(f, read_list=True)
    return L[0]


def process_graphs(file, graphs):
    iso_start = time.time()
    isomorphs = calculate_isomorphs(graphs)
    iso_time = time.time() - iso_start
    auto_start = time.time()
    automorphs = calculate_automorphs(isomorphs)
    auto_time = time.time() - auto_start
    result_string = stringify_result(file, isomorphs, iso_time, automorphs, auto_time)
    print_result(result_string)


def calculate_isomorphs(graphs):
    isomorphs = [[]]
    isomorphs[0] = [graphs.pop(0)]
    for i in range(len(graphs)):
        added = False
        for j in range(len(isomorphs)):
            if is_isomorphisms(isomorphs[j][0], graphs[i]):
                isomorphs[j].append(graphs[i])
                added = True
                break
        if not added:
            isomorphs.append([graphs[i]])
    return isomorphs


def calculate_automorphs(isomorphs):
    automorphs = []
    for k in range(len(isomorphs)):
        automorphs.append(get_number_automorphisms(isomorphs[k][0]))
    return automorphs


def create_titles(file, total_time):
    title = '=========================================================================\n' \
            + file.rsplit('/', 1)[1] + "                        TOTAL TIME: " + str(total_time) \
            + '\n\n' \
            + OUTPUT_FORMAT.format('isomorphs', 'isotime', 'automorphs', 'autotime') + '\n' \
            + '-------------------------------------------------------------------------'
    return title


def stringify_result(file, isomorphs, iso_time, automorphs, auto_time):
    total_time = round(iso_time + auto_time, TIME_ROUND)
    result = create_titles(file, total_time)
    for m in range(len(isomorphs)):
        iso_string = str(len(isomorphs[m])) + ": ("
        for n in range(len(isomorphs[m])):
            iso_string += isomorphs[m][n].name
            if n + 1 < len(isomorphs[m]):
                iso_string += ", "
        iso_string += ")"
        iso_time_string = str(round(iso_time, TIME_ROUND))
        auto_string = str(automorphs[m])
        auto_time_string = str(round(auto_time, TIME_ROUND))
        subresult = OUTPUT_FORMAT.format(iso_string, iso_time_string, auto_string, auto_time_string)
        result += "\n" + subresult
    return result + "\n"


def print_result(result):
    print(result)


def export_result(result):
    output_file = open('result_' + str(round(time.time())), 'w')
    output_file.write(result)
    output_file.close()


if __name__ == "__main__":
    main()
