"""
Module with helper methods for the Color Refinement Algorithm
"""
from typing import Iterable

from coloring import *
from graph import Graph
from tools import create_graph_helper

Module = [Vertex]
ModularDecomposition = [Module]

DEBUG = False


def debug(*args):
    """
    Prints debug statements when DEBUG is set to `True`

    :param args: argument to be printed
    """
    if DEBUG:
        print(*args)


def compare(s: Iterable, t: Iterable, key=None) -> bool:
    """Compare 2 iterables and will do so on the sorted list.

    :param Iterable s: One iterable to compare
    :param Iterable t: Another iterable to compare
    :param key: Key on which to compare the iterables' contents on, e.g. Vertex.label or a lambda function.
    :return: `True` if the iterables' contents are the same; `False` otherwise.
    """
    return sorted(s, key=key) == sorted(t, key=key)


def create_new_color_class(coloring: Coloring, vertex1: Vertex, vertex2: Vertex) -> Coloring:
    """
    Returns a new coloring where both vertices have the same new color class and are removed from the one they belonged
    to

    :param coloring: current coloring
    :param vertex1: vertex to be in the separate color
    :param vertex2: vertex to be in the separate color
    :return: a new coloring with vertex1 and vertex2 together as a new color class
    """
    new_coloring = coloring.copy()
    new_color = new_coloring.next_color()
    new_coloring.recolor(vertex1, new_color)
    new_coloring.recolor(vertex2, new_color)
    return new_coloring


def has_same_color_neighbours(u: Vertex, v: Vertex, coloring: Coloring) -> bool:
    """
    Returns whether the vertices u and v have the same colored neighbourhood for the given coloring

    :param u: vertex of which the neighbourhood must be compared
    :param v: vertex of which the neighbourhood must be compared
    :param coloring: current coloring
    :return: `True` if the vertices have the same colored neighbourhood, `False` otherwise
    """
    ncolors_u = (coloring.color(w) for w in u.neighbours)
    ncolors_v = (coloring.color(w) for w in v.neighbours)
    return compare(ncolors_u, ncolors_v)


def choose_color(coloring: Coloring) -> DoubleLinkedList:
    """
    Returns a partition cell (aka color class) with at least four vertices

    Returns the first color class with at least four vertices that is found.
    :param coloring: current coloring
    :return: a color class with at least four vertices, `None` if no color class could be found
    """
    for color in coloring.colors:
        vertices = coloring.get(color)
        if len(vertices) >= 4 and len(vertices) % 2 == 0:
            return vertices
    return DoubleLinkedList()


def choose_color_trivial(coloring: Coloring, g: Graph) -> (Vertex, [Vertex]):
    """
    Returns a partition cell (aka color class) with at least four vertices

    Returns the first color class with at least four vertices that is found.
    :param coloring: current coloring
    :return: a color class with at least four vertices, `None` if no color class could be found
    """
    for key in coloring.colors:
        vertices = list(coloring.get(key))
        if len(vertices) >= 4 and len(vertices) % 2 == 0:
            ordered = group_by(vertices, group_rule=lambda v: v.id)
            for key1 in ordered.keys():
                if len(ordered[key1]) == 2:
                    if ordered[key1][0].in_graph(g):
                        return ordered[key1][0], vertices
                    else:
                        return ordered[key1][1], vertices
    return None, []


def choose_vertex(color: Iterable[Vertex], g: Graph) -> Union[Vertex, None]:
    """
    Returns a vertex of graph g which is in the given color class

    Returns the first vertex of graph g in the color.
    :param color: color class from which the vertex must be chosen
    :param g: graph of which the vertex must be a part of
    :return: a vertex of graph g in the color class, `None` if no vertex of graph g could be found
    """
    for vertex in color:
        if vertex.in_graph(g):
            return vertex
    return None


def graph_to_modules(graph: Graph) -> ModularDecomposition:
    vertices = graph.vertices
    vertices_in_any_module = []
    modular_decomposition = []

    for vertex in vertices:
        if vertex in vertices_in_any_module:
            continue

        module = [vertex]
        vertices_in_any_module.append(vertex)

        neighbours = vertex.neighbours

        other_vertices = [vertex for vertex in vertices if vertex not in vertices_in_any_module]
        for other_vertex in other_vertices:
            other_neighbours = set(other_vertex.neighbours) - {vertex}
            if other_neighbours == (set(neighbours) - {other_vertex}):
                module.append(other_vertex)
                vertices_in_any_module.append(other_vertex)

        modular_decomposition.append(module)

    return modular_decomposition


def modules_to_graph(modules: ModularDecomposition) -> (Graph, {Vertex: Vertex}):
    """
    Returns a new Graph object with Modules compressed to a Vertex
    :param modules: list of modules
    :return: new Graph
    """

    label_mapping = {}

    edges_list = []
    for module in modules:
        for vertex in module:
            edges_list += get_edges_of_vertex(vertex)

    for module in modules:
        if len(module) > 1:
            new_label = create_new_label(module)
            for vertex in module:
                label_mapping[vertex] = new_label
            edges_list = relabel_edges(module, edges_list, new_label)

    edges = set()
    for edge in edges_list:
        if edge[0] != edge[1]:
            edges.add(tuple(sorted(edge)))

    if not edges:
        graph = Graph(False)
        if edges_list:
            vertex = Vertex(graph, edges_list[0][0])
        graph.add_vertex(vertex)
    else:
        graph = create_graph_helper(sorted(list(edges)))

    old_new_vertex_mapping = {}
    for vertex, label in label_mapping.items():
        old_new_vertex_mapping[vertex] = graph.find_vertex(label)

    return graph, old_new_vertex_mapping


def determine_module_connectivity(md: ModularDecomposition):
    connected_modules = []
    disconnected_modules = []
    for module in (module for module in md if len(module) > 1):
        if module[1] in module[0].neighbours:
            # Connected, i.e. serial
            connected_modules.append(module)
        else:
            # Disconnected, i.e. parallel
            disconnected_modules.append(module)

    return connected_modules, disconnected_modules


def modules_to_graph_with_module_isomorphism(md: ModularDecomposition) -> (Graph, [[Vertex]]):
    def _add_iso_groups(md_groups, groups, mapping):
        for modules in md_groups:
            iso = []
            for module in modules:
                iso.append(mapping[module[0]])
            groups.append(iso)

    def _sort_iso_groups(length_to_module_mapping):
        return [length_to_module_mapping[length] for length in sorted(length_to_module_mapping.keys())]

    graph, old_new_vertex_mapping = modules_to_graph(md)
    connected_md, disconnected_md = determine_module_connectivity(md)

    length_to_iso_connected_modules = group_by(connected_md, len)
    length_to_isomorphic_disconnected_modules = group_by(disconnected_md, len)

    connected_iso_groups = _sort_iso_groups(length_to_iso_connected_modules)
    disconnected_iso_groups = _sort_iso_groups(length_to_isomorphic_disconnected_modules)

    md_iso_groups = []
    _add_iso_groups(connected_iso_groups, md_iso_groups, old_new_vertex_mapping)
    _add_iso_groups(disconnected_iso_groups, md_iso_groups, old_new_vertex_mapping)

    return graph, md_iso_groups


def get_edges_of_vertex(vertex: Vertex) -> List[List[str]]:
    edges = []
    for edge in vertex.incidence:
        edges.append([str(edge.head.label), str(edge.tail.label)])
    return edges


def create_new_label(module: Module) -> str:
    new_label = str(module[0].label)
    itermodule = iter(module)
    next(itermodule)
    for vertex in itermodule:
        new_label = "+".join(sorted([new_label, str(vertex.label)]))
    return new_label


def relabel_edges(module: Module, edges_list: List[List[str]], new_label: str) -> List[List[str]]:
    for edge in edges_list:
        for vertex in module:
            label = str(vertex.label)
            edge[0] = new_label if edge[0] == label else edge[0]
            edge[1] = new_label if edge[1] == label else edge[1]
    return edges_list


def initialize_coloring(g: Graph) -> Coloring:
    """
    Creates an initial coloring for graph g where the vertices with the same degree are in the same color class

    :param g: graph on which the coloring needs to be applied
    :return: an initial coloring of graph g by degree
    """

    coloring = Coloring()
    for v in g.vertices:
        coloring.set(v, v.degree)
    debug('Init coloring ', coloring)
    return coloring


def generate_neighbour_count_with_color(coloring: Coloring, current_color: int) -> {}:
    """
    This methode creates a mapping from a vertex to the amount of neighbours with current_color.
    :param coloring: coloring used for the counting of the neighbours
    :param current_color: the color which is used to refine the graph
    :return: mapping of colors to a vertex-neighbour_count mapping, the vertex-neighbour_count mapping
                is a dictionary which maps vertices to the amount of neighbours with current_color
    """

    counter = {}
    for v in coloring.vertices:
        count = 0
        for x in v.neighbours:
            if coloring.color(x) is current_color:
                count += 1
        if coloring.color(v) not in counter.keys():
            counter[coloring.color(v)] = {}
        counter[coloring.color(v)].update({v: count})
    return counter


def group_by(obj, group_rule=None) -> dict:
    """
    Group the given object according to the given key.

    Eg. group_by(List[int]) groups by number
    Eg. group_by(List[Vertex], key=Vertex.degree) groups by vertex degree
    Eg. group_by(dict{List}, key=lambda x:len(x)) groups by length of the lists
    :param obj: Object over which one can iterate
    :param group_rule: Rule to use for grouping, if not set `lambda x:x` is used
    :return: A dict in which the elements of 'obj' are grouped by results of the 'group_rule'
    """

    d = {}
    if not group_rule:
        for elem in obj:
            d.setdefault(elem, []).append(elem)
    else:
        for elem in obj:
            key = group_rule(elem)
            d.setdefault(key, []).append(elem)
    return d


def get_mappings(v: Vertex, vertices: [Vertex]) -> (Vertex, [Vertex]):
    """
    Returns the trivial mapping of a Vertex and a list of non-trivial mappings

    Returns a 2-tuple with as first argument the trivial mapping of the Vertex. The second argument is a list of
    vertices which are not the trivial mapping. A mapping is called trivial if the labels of two vertices are equal.
    The list of vertices (mappings) must be from another graph compared to vertex.
    :param Vertex v: the vertex to be mapped
    :param [Vertex] vertices: list of vertices to map to. These vertices must belong to another graph than Vertex v
    :return (Vertex, [Vertex]): a trivial mapping from the vertex to the other graph, `None` if it doesn't exist. And a list of vertices
    which is not a trivial mapping.
    """
    trivial = None
    non_trivial = []
    for vertex in vertices:
        if vertex.id == v.id:
            trivial = vertex
        else:
            non_trivial.append(vertex)
    return trivial, non_trivial
