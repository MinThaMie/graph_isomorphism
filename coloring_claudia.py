from graph_io import *
from collections import Counter
from graph import *


def count_isomorphism(g: "Graph", h: "Graph", coloring: "dict") -> int:
    """
    Returns the number of isomorphisms of graph g and h for a given stable coloring.

    If the coloring is unbalanced, it will return 0.
    If the coloring defines a bijection, it will return 1.
    If neither applies, a partition is chosen from which a vertex of graph g is mapped to all possible vertices of graph
    h in the same partition. For each mapping, the number of isomorphisms is calculated and summed.
    :param g: first graph to compare
    :param h: second graph to compare
    :param coloring: stable coloring of graph g and h
    :return: the number of isomorphisms of graph g and h for a given coloring
    """
    new_coloring = color_refinement(coloring)
    if is_unbalanced(new_coloring):
        return 0
    if is_bijection(new_coloring):
        return 1
    partition = choose_partition(new_coloring)
    first_vertex = choose_vertex(partition, g)
    number_isomorphisms = 0
    for second_vertex in get_vertices_of_graph(partition, h):
        adapted_coloring = create_partition(new_coloring, first_vertex, second_vertex)
        number_isomorphisms = number_isomorphisms + count_isomorphism(g, h, adapted_coloring)
    return number_isomorphisms


def create_partition(old_coloring: "dict", vertex1: "Vertex", vertex2: "Vertex") -> "dict":
    """
    Returns a new coloring where both vertices are in a new partition and removed from the one they belonged to.

    :param old_coloring: current coloring
    :param vertex1: vertex to be in the separate partition
    :param vertex2: vertex to be in the separate partition
    :return: a new coloring with vertex1 and vertex2 as a seperate partition
    """
    new_coloring = {}
    new_partition = list()
    new_partition.append(vertex1)
    new_partition.append(vertex2)
    new_coloring[0] = new_partition
    for key in old_coloring.keys():
        vertices = list(old_coloring[key])
        if vertex1 in vertices:
            vertices.remove(vertex1)
            vertices.remove(vertex2)
        new_coloring[key + 1] = list(vertices)
    return new_coloring


def initialize_coloring(g: "Graph") -> dict:
    """
    Creates an initial coloring where the vertices with the same degree are in the same partition.

    :param g: graph on which the coloring needs to be applied
    :return: an initial coloring of graph g
    """
    coloring = {}
    for vertex in g.vertices:
        if vertex.degree not in coloring.keys():
            coloring[vertex.degree] = []
        coloring[vertex.degree].append(vertex)
    return coloring


def color_refinement(old_coloring: "dict") -> "dict":
    """
    Returns a stable coloring based on the input coloring.

    For each partition, the vertices in that partition are compared. If their neighbours are in the same partition, the
    vertices stay in the same partition. If not, the vertices will be put in separate partitions.
    When there is no change in the coloring, the coloring is considered stable. When the coloring is unstable, the
    color-refinement algorithm is applied again.
    :param old_coloring:
    :return: a stable coloring
    """
    new_coloring = {}
    colornr = 0
    for key in old_coloring.keys():
        vertices = list(old_coloring[key])
        while len(vertices) > 0:
            u = vertices.pop(0)
            if colornr not in new_coloring.keys():
                new_coloring[colornr] = []
            new_coloring[colornr].append(u)
            for v in list(vertices):
                if has_same_color_neignhours(u, v, old_coloring):
                    new_coloring[colornr].append(v)
                    vertices.remove(v)
            colornr = colornr + 1
    changed = len(old_coloring.keys()) != len(new_coloring.keys())
    if changed:
        if is_unbalanced(new_coloring):
            return new_coloring
        return color_refinement(new_coloring)
    else:
        return new_coloring


def has_same_color_neignhours(u: "Vertex", v: "Vertex", coloring: "dict") -> bool:
    """
    Returns whether the vertices u and v have the same colored neighbourhood for the given coloring.

    :param u: vertex of which the neighbourhood must be compared
    :param v: vertex of which the neighbourhood must be compared
    :param coloring: coloring
    :return: `True` if the vertices have the same colored neighbourhood, `False` otherwise
    """
    color_u = [find_key(w, coloring) for w in u.neighbours]
    color_v = [find_key(w, coloring) for w in v.neighbours]
    return Counter(color_u) == Counter(color_v)


def find_key(value, dictionary: "dict"):
    """
    Returns the key of the value for the given dictionary.

    :param value: value to find the key of
    :param dictionary: dictionary with key,value-pairs in which to search
    :return: Returns the key of the given value, returns `None` if no key can be found
    """
    for key in dictionary.keys():
        if value in dictionary[key]:
            return key
    return None


def is_unbalanced(coloring: "dict") -> bool:
    """
    Returns whether the coloring is balanced.

    The coloring is balanced if all partitions have a even number of vertices.
    :param coloring:
    :return: `True` if the coloring is unbalanced, `False` if the coloring is balanced
    """
    for k in coloring.keys():
        values = coloring[k]
        if (len(values) % 2) == 1:
            return True
    return False


def is_bijection(coloring: "dict") -> bool:
    """
    Returns whether the coloring defines a bijection.

    A coloring defines a bijection if all colors are appear only one time in one graph, and one time in the other. So,
    if all partitions contain two vertices. By definition of the color-refinement algorithm, it is not possible that a
    partition with two vertices are both in the same graph.
    :param coloring:
    :return: `True` if the coloring defines a bijection, `False` otherwise
    """
    for key in coloring.keys():
        values = coloring[key]
        if len(values) != 2:
            return False
    return True


def choose_partition(coloring: "dict") -> List["Vertex"]:
    """
    Selects a partition with at least four vertices.

    Returns the first partition with at least four vertices that is found.
    :param coloring:
    :return: a partition with at least four vertices, `None` if no partition could be found
    """
    for key in coloring.keys():
        values = list(coloring[key])
        if len(values) >= 4 and len(values) % 2 == 0:
            return values
    return []


def choose_vertex(partition: List["Vertex"], g: "Graph") -> "Vertex":
    """
    Selects a vertex of graph g which is in the given partition.

    Returns the first vertex of graph g in the partition.
    :param partition:
    :param g: graph of which the vertex must be a part
    :return: a vertex of graph g in the partition, `None` if no vertex of graph g could be found
    """
    for vertex in partition:
        if g in vertex.graph:
            return vertex
    return None


def get_vertices_of_graph(partition: List["Vertex"], g: "Graph") -> List["Vertex"]:
    """
    Returns the vertices of graph g in the given partition.

    :param partition:
    :param g:
    :return: a list of vertices belonging to graph g in the given partition. The list is empty if no vertices of graph g
    are found in the given partition
    """
    vertices = list()
    for v in partition:
        if g in v.graph:
            vertices.append(v)
    return vertices


# def is_isomorphic(g: "Graph", h: "Graph"):
#     """
#     Returns whether graph g and h are isomorphic.
#
#     :param g: graph to check for isomorphism
#     :param h: graph to check for isomorphism
#     :return: `True` if graph g and h are isomorphic, `False` otherwise
#     """
#     added_graph = g + h
#     coloring = color_refinement(initialize_coloring(added_graph))
#
#     could_be_isomorphic = True
#     for k in coloring.keys():
#         values = coloring[k]
#         # test if there are an odd number of vertices in the partition
#         if (len(values) % 2) == 1:
#             return False
#         # check if there are the same number of vertices of g as h in the partition
#         count = 0
#         for v in values:
#             if v in h.vertices:
#                 count = count + 1
#         # check if the
#         if count != (len(values) - count):
#             return False
#         if len(values) == 2:
#             could_be_isomorphic = could_be_isomorphic and True
#         else:
#             could_be_isomorphic = False
#     if could_be_isomorphic:
#         return could_be_isomorphic
#     else:
#         return None


def get_number_isomorphisms(g: "Graph", h: "Graph") -> int:
    """
    Returns the number of isomorphisms for graph g and h.

    First, the coloring is initialized by degree of the vertices. Next, the number of isomorphisms is counted by
    applying the color-refinement algorithm and branching the
    :param g: graph for which to determine the number of isomorphisms
    :param h: graph for which to determine the number of isomorphisms
    :return: The number of isomorphisms for graph g and h
    """
    if len(g) != len(h):
        return 0
    if len(g.edges) != len(h.edges):
        return 0
    added_graph = g + h
    coloring = initialize_coloring(added_graph)
    return count_isomorphism(g, h, coloring)


def get_number_automorphisms(g: "Graph") -> int:
    """
    Returns the number of automorphisms of graph g.

    Applies the GI-problem to itself.
    :param g: graphs for which to determine the number of isomorphisms
    :return: The number of automorphisms for graph g
    """
    return get_number_isomorphisms(g, g.deepcopy())


def is_twins(u: "Vertex", v: "Vertex") -> bool:
    N_u = u.neighbours
    N_u.remove(v)
    N_v = v.neighbours
    N_v.remove(u)
    return Counter(N_u) == Counter(N_v)


def get_twins(g: "Graph"):  # -> List[("Vertex", "Vertex")]:
    twins = list()
    false_twins = list()
    for u in g.vertices:
        for v in g.vertices:
            if v.label > u.label:
                if u.is_adjacent(v) and is_twins(u, v):
                    twins.append((u, v))
                if Counter(u.neighbours) == Counter(v.neighbours):
                    false_twins.append((u, v))
    return twins, false_twins

# with open('trees36.grl') as f:
#     L = load_graph(f, read_list=True)
#
# g0 = L[0][1]
#
# twins, false_twins = get_twins(g0)
# print('true twins: ', twins)
# print('false twins: ', false_twins)
# print('#vertices    = ', len(g0.vertices))
# print('#false twins = ', len(false_twins))
# print('#automorphisms:', get_number_automorphisms(g0))

