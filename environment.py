import os

import time
from typing import List, Tuple

from color_refinement import get_number_automorphisms, is_isomorphisms
from graph import Graph
from graph_io import load_graph

PATH_BRANCHING = 'graphs/branching'
PATH_COLORREF = 'graphs/colorref'
PATH_TREEPATHS = 'graphs/treepaths'
OUTPUT_PATH = 'export/result'

FILE = 'graphs/branching/wheeljoin14.grl'


def main():
    if FILE == '':
        graph_files = find_graphs()
    else:
        graph_files = [FILE]
    process_graph_files(graph_files)


def find_graphs() -> List[str]:
    branching_graphs = [PATH_BRANCHING + '/' + file for file in os.listdir(PATH_BRANCHING)]
    colorref_graphs = [PATH_COLORREF + '/' + file for file in os.listdir(PATH_COLORREF)]
    treepath_graphs = [PATH_TREEPATHS + '/' + file for file in os.listdir(PATH_TREEPATHS)]
    return branching_graphs + colorref_graphs + treepath_graphs


def process_graph_files(graph_files: List[str]):
    for file in graph_files:
        graphs = get_graphs_from_file(file)
        isomorphs, iso_time, automorphs, auto_time = process_graphs(graphs)
        result_string = stringify_result(file, isomorphs, iso_time, automorphs, auto_time)
        print_result(result_string)


def get_graphs_from_file(file: str) -> List[Graph]:
    with open(file) as f:
        L = load_graph(f, read_list=True)
    return L[0]


def process_graphs(graphs: List[Graph]) -> Tuple[List[List[Graph]], float, List[int], float]:
    iso_start = time.time()
    isomorphs = calculate_isomorphs(graphs)
    iso_time = time.time() - iso_start
    auto_start = time.time()
    automorphs = calculate_automorphs(isomorphs)
    auto_time = time.time() - auto_start
    return isomorphs, iso_time, automorphs, auto_time


def calculate_isomorphs(graphs: List[Graph]) -> List[List[Graph]]:
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


def calculate_automorphs(isomorphs: List[List[Graph]]) -> List[int]:
    automorphs = []
    for k in range(len(isomorphs)):
        automorphs.append(get_number_automorphisms(isomorphs[k][0]))
    return automorphs


def stringify_result(file: str, isomorphs: List[List[Graph]], iso_time: float, automorphs: List[int], auto_time: float) -> str:
    title_string = create_title_string(file)
    data_string = create_data_string(isomorphs, automorphs)
    footer_string = create_footer_string(iso_time, auto_time)
    return title_string + '\n' + data_string + '\n' + footer_string + '\n'


def create_title_string(file: str) -> str:
    title = '{:_<41}'.format('') + '\n' \
            + file.rsplit('/', 1)[1] + '\n'
    return title


def create_data_string(isomorphs: List[List[Graph]], automorphs: List[int]) -> str:
    output_format = '{:<20} {:>20}'
    data_string = output_format.format('ISOMORPHS', 'AUTOMORPHS')
    for m in range(len(isomorphs)):
        iso_string = str(len(isomorphs[m])) + ' ('
        for n in range(len(isomorphs[m])):
            iso_string += isomorphs[m][n].name
            if n + 1 < len(isomorphs[m]):
                iso_string += ', '
        iso_string += ')'
        auto_string = str(automorphs[m])
        subresult = output_format.format(iso_string, auto_string)
        data_string += '\n' + subresult
    return data_string + '\n'


def create_footer_string(iso_time: float, auto_time: float) -> str:
    output_format = '{:<20} {:>20.10f}'
    total_time = iso_time + auto_time
    footer = output_format.format('isomorphs time', iso_time) + '\n' \
             + output_format.format('automorphs time', auto_time) + '\n' \
             + '{:25} {:-<15}'.format('', '') + '\n' \
             + output_format.format('total time (s)', total_time)
    return footer


def print_result(result):
    print(result)


def export_result(result):
    output_file = open('result_' + str(round(time.time())), 'w')
    output_file.write(result)
    output_file.close()


if __name__ == "__main__":
    main()
