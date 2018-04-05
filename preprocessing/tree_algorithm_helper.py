from graph import *


def has_cycle(g: Graph, vertex: Vertex, predecessor: Vertex, visited):
    """
    Recursive function to detect cycles in a graph

    :param g: input graph
    :param vertex: vertex to start from
    :param predecessor: predecessor vertex of vertex
    :param visited: List with visited vertices
    :param result: list containing the "Truth Of The Tree"
    :return: result: [True] if has_cycle
    """
    visited.append(vertex)

    for v in vertex.neighbours:
        if v in visited and v is not predecessor:
            return True
        elif v not in visited:
            return has_cycle(g, v, vertex, visited)
