import os
from typing import List, Tuple, Any, Dict, Set

from graph import Graph, Vertex, Edge

_last_integer = 0
_generated_integers = set()

IsomorphismMapping = Dict[int, Set[int]]


def dot_to_pdf(dot_file_path: str, pdf_file_path: str, open_outfile: bool = False):
    """Read a Graphviz DOT file and write to PDF. `dot` must be on your system path.
    :param str dot_file_path: path to DOT file to read.
    :param str pdf_file_path: path to PDF file to write.
    :param bool open_outfile: open created PDF file if `True`; don't open it otherwise.
    """

    os.system(f'dot {dot_file_path} -Tpdf > {pdf_file_path}')

    if open_outfile:
        os.system(f'open {pdf_file_path}')


def unique_integer() -> int:
    """Generate a unique non-negative integer."""

    # Note: int is unbounded (no max, except for system limit) in Python 3
    # Source: https://stackoverflow.com/a/7604981/3169029

    global _last_integer, _generated_integers

    if _last_integer in _generated_integers:
        _last_integer += 1
        return unique_integer()

    _generated_integers.add(_last_integer)
    return _last_integer


def create_graph_helper(edges: List[Tuple[Any, Any]] = list()):
    """
    Create a graph from the specified edges.

    :param edges: A list of 2-tuples of vertex labels (of any type) between which to create edges.
    :return: The graph with labelled vertices and edges
    """

    graph = Graph(False)
    vertices = {}
    for head, tail in edges:
        if head not in vertices:
            vertices[head] = Vertex(graph=graph, label=head, id=head)
            graph.add_vertex(vertices[head])

        if tail not in vertices:
            vertices[tail] = Vertex(graph=graph, label=tail, id=tail)
            graph.add_vertex(vertices[tail])

        graph.add_edge(Edge(vertices[head], vertices[tail]))
    return graph


def update_known_isomorphisms(i: int, j: int, known_isomorphisms: IsomorphismMapping) -> IsomorphismMapping:
    """
    Store a known isomorphism between two indices in the specified mapping.

    :param int i: Index of one known isomorphism pair member.
    :param int j: Index of another known isomorphism pair member.
    :param dict known_isomorphisms: Dictionary in which to store the set of known isomorphisms.
    """

    isomorphisms = known_isomorphisms[i] | known_isomorphisms[j] | {i, j}

    for index in isomorphisms:
        known_isomorphisms[index] = isomorphisms - {index}

    return known_isomorphisms
