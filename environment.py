import os
import time
from typing import List, Tuple

from color_refinement import get_number_automorphisms, is_isomorphisms
from disconnected_refinement import graph_component_isomorphic
from graph import Graph
from graph_io import load_graph
from preprocessing import checks, check_complement, find_components, construct_graph_from_components

GRAPHS = 'graphs'
BRANCHING = os.path.join(GRAPHS, 'branching')
COLORREF = os.path.join(GRAPHS, 'colorref')
TREEPATHS = os.path.join(GRAPHS, 'treepaths')
D_DAY = os.path.join(GRAPHS, 'd_day')
BASIC = os.path.join(D_DAY, 'basic/')

FILE = os.path.join(D_DAY, 'comp1.gr')


def main():
    if FILE == '':
        graph_files = find_graphs()
    else:
        graph_files = [FILE]
    process_graph_files(graph_files)


def find_graphs() -> List[str]:
    """
    Find all graph files on a given path
    :return: List of strings representing the paths to graph files
    """
    # branching_graphs = [BRANCHING + file for file in os.listdir(BRANCHING)]
    # colorref_graphs = [COLORREF + file for file in os.listdir(COLORREF)]
    # treepath_graphs = [TREEPATHS + file for file in os.listdir(TREEPATHS)]
    # return branching_graphs + colorref_graphs + treepath_graphs
    basic_graphs = [BASIC + file for file in os.listdir(BASIC)]
    return basic_graphs


def process_graph_files(graph_files: List[str]):
    """
    Run graph processing for every file in the input list
    :param graph_files: list of strings representing the paths to graph files
    """

    for file in graph_files:
        print(file)
        graphs = get_graphs_from_file(file)
        isomorphs, iso_time, automorphs, auto_time = process_graphs(graphs)
        result_string = stringify_results(file, isomorphs, iso_time, automorphs, auto_time)
        output_result(result_string)


def get_graphs_from_file(file: str) -> List[Graph]:
    with open(file) as f:
        graphs = load_graph(f, read_list=True)
    return graphs[0]


def process_graphs(graphs: List[Graph]) -> Tuple[List[List[Graph]], float, List[int], float]:
    """
    First preprocesses the given graphs, then runs calculations for isomorphisms and automorphisms. :param graphs:
    raw graphs to be processed

    :return: result tuple containing a list with: a list of isomorphic graphs, isomorphisms calculation time,
             automorphisms per graph and automorphisms calculation time
    """

    output_result(create_title_string("ISOMORPHISMS"))
    iso_start = time.time()
    isomorphs = calculate_isomorphisms(graphs)
    iso_time = time.time() - iso_start

    output_result(create_title_string("AUTOMORPHISMS"))
    graphs = [graphs[0] for graphs in isomorphs]
    auto_start = time.time()
    automorphs = calculate_automorphisms(graphs)
    auto_time = time.time() - auto_start

    return isomorphs, iso_time, automorphs, auto_time


def calculate_isomorphisms(graphs: List[Graph]) -> List[List[Graph]]:
    """
    Run isomorphism calculation for every graph in the input list
    :param graphs: list of graphs to be calculated
    :return: list with list of isomorphic graphs
    """

    isomorphs = [[]]
    isomorphs[0] = [graphs.pop(0)]
    for i in range(len(graphs)):
        added = False
        start_time = time.time()
        for j in range(len(isomorphs)):
            is_potential_isomorph, g, h = preprocess(isomorphs[j][0], graphs[i])
            if is_potential_isomorph:
                is_connected_g, components_g = find_components(g)
                is_connected_h, components_h = find_components(h)
                if not is_connected_g and not is_connected_h:
                    if graph_component_isomorphic(construct_graph_from_components(components_g),
                                                  construct_graph_from_components(components_h)):
                        end_time = time.time()
                        isomorphs[j].append(graphs[i])
                        added = True
                        output_result(graphs[i].name + " and " + isomorphs[j][0].name + " are isomorphisms (" + str(
                            end_time - start_time) + ")")
                        break
                if is_connected_g and is_connected_h:
                    if is_isomorphisms(g, h):
                        end_time = time.time()
                        isomorphs[j].append(graphs[i])
                        added = True
                        output_result(graphs[i].name + " and " + isomorphs[j][0].name + " are isomorphisms (" + str(
                            end_time - start_time) + ")")
                        break
        if not added:
            isomorphs.append([graphs[i]])
            end_time = time.time()
            output_result(f"{graphs[i].name} has no isomorphisms yet ({str(end_time - start_time)})")
    return isomorphs


def preprocess(g: Graph, h: Graph) -> Tuple[bool, Graph, Graph]:
    """
    Preprocess graphs for isomorphism calculation
    :param Graph h: One graph.
    :param Graph g: Another graph.
    :return: graphs prepared for isomorphism calculation
    """

    is_isomorph = checks(g, h)
    if is_isomorph:
        g, h = check_complement(g, h)
    return is_isomorph, g, h


def calculate_automorphisms(graphs: List[Graph]) -> List[int]:
    """
    Run automorphism calculation for every graph in the input list
    :param graphs: list of graphs to be calculated
    :return: list with number of automorphisms per graph
    """

    automorphisms = []
    for graph in graphs:
        start_time = time.time()
        num_automorphisms = get_number_automorphisms(graph)
        end_time = time.time()
        output_result(
            f"{graph.name}\'s group has {str(num_automorphisms)} automorphisms ({str(end_time - start_time)})")
        automorphisms.append(num_automorphisms)
    return automorphisms


def stringify_results(file: str, isomorphs: List[List[Graph]], iso_time: float, automorphs: List[int],
                      auto_time: float) -> str:
    title_string = create_title_string(get_file_title(file))
    data_string = create_data_string(isomorphs, automorphs)
    footer_string = create_footer_string(iso_time, auto_time)
    return title_string + '\n' + data_string + '\n' + footer_string + '\n'


def create_title_string(title: str) -> str:
    return '\n' + title + '\n' + '{:_<41}'.format('') + '\n'


def get_file_title(file: str) -> str:
    return file.rsplit(os.path.sep, 1)[1]


def create_data_string(isomorphs: List[List[Graph]], automorphs: List[int]) -> str:
    output_format = '{:<20} {:>20}'
    data_string = output_format.format('ISOMORPHISMS', 'AUTOMORPHISMS')

    for m in range(len(isomorphs)):
        iso_string = '[' + ', '.join(graph.name for graph in isomorphs[m]) + ']'
        auto_string = str(automorphs[m])
        subresult = output_format.format(iso_string, auto_string)
        data_string += '\n' + subresult

    return data_string + '\n'


def create_footer_string(iso_time: float, auto_time: float) -> str:
    output_format = '{:<20} {:>20.10f}'
    return '{0}\n{1}\n{2}\n{3}'.format(output_format.format('Isomorphisms time', iso_time),
                                       output_format.format('Automorphisms time', auto_time),
                                       f'{"":25} {"":-<15}',
                                       output_format.format('Total time (s)', iso_time + auto_time))


def output_result(result: str):
    print(result)


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print('Total time:', end - start)
