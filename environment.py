import os

import time

from color_refinement import get_number_automorphisms, is_isomorphisms
from graph_io import load_graph

PATH_BRANCHING = 'graphs/branching'
PATH_COLORREF = 'graphs/colorref'
PATH_TREEPATHS = 'graphs/treepaths'
OUTPUT_FORMAT = '{:10} {:>15} {:>25} {:>15} {:>25} {:>25}'
OUTPUT_PATH = 'export/result'


def main():
    file_graphs = find_graphs()
    process_data(file_graphs)


def find_graphs():
    branching_graphs = [PATH_BRANCHING + '/' + file for file in os.listdir(PATH_BRANCHING)]
    colorref_graphs = [PATH_COLORREF + '/' + file for file in os.listdir(PATH_COLORREF)]
    treepath_graphs = [PATH_TREEPATHS + '/' + file for file in os.listdir(PATH_TREEPATHS)]
    return branching_graphs + colorref_graphs + treepath_graphs


def process_data(file_graphs):
    for file in file_graphs:
        graphs = get_graphs_from_file(file)
        process_graphs(graphs)


def get_graphs_from_file(file):
    with open(file) as f:
        L = load_graph(f, read_list=True)
    return L[0]


def process_graphs(graphs):
    groups = [[]]
    groups[0] = [graphs.pop(0)]
    iso_start = time.time()
    for i in range(len(graphs)):
        added = False
        for j in range(len(groups)):
            if is_isomorphisms(groups[j][0], graphs[i]):
                groups[j].append(graphs[i])
                added = True
                break
        if not added:
            groups.append([graphs[i]])
    iso_time = time.time() - iso_start

    automorphs = []
    auto_start = time.time()
    for k in range(len(groups)):
        automorphs.append(get_number_automorphisms(groups[k][0]))
    auto_time = time.time() - auto_start

    for m in range(len(groups)):
        string1 = "Group " + str(m) + " has " + str(len(groups[m])) + " isomorph(s) ("
        for n in range(len(groups[m])):
            string1 += groups[m][n].name
            if n + 1 < len(groups[m]):
                string1 += ", "
        string1 += ") and " + str(automorphs[m]) + " automorph(s)"
        print(string1)

    total_time = auto_time + iso_time
    string2 = "Calculation time: " + str(total_time)
    print(string2)

    # subresult = OUTPUT_FORMAT.format(graphs[i].name, isomorphs, iso_time, automorphs, auto_time, total_time)
    # result += result + '\n' + subresult
    # print(subresult)
    # export_result(result)


def create_titles(file):
    title = '====================================\n' \
            + file.rsplit('/', 1)[1] \
            + '\n' + '====================================\n' \
            + OUTPUT_FORMAT.format('graph', 'isomorphs', 'isotime', 'automorphs', 'autotime', 'totaltime') + '\n' \
            + '--------------------------------------------------------------------\n'
    return title


def export_result(result):
    output_file = open('result_' + str(round(time.time())), 'w')
    output_file.write(result)
    output_file.close()


if __name__ == "__main__":
    main()
