from coloring_dorien import *
from tools import *


def initialize_coloring(g: "Graph") -> "Coloring":
    """
    Creates an initial coloring where the vertices with the same degree are in the same partition.

    :param g: graph on which the coloring needs to be applied
    :return: an initial coloring of graph g
    """
    return get_degree_coloring(g)


def get_degree_coloring(graph: "Graph"):
    # Initialize colors to degrees
    coloring = Coloring()
    for v in graph.vertices:
        coloring.set(v.degree, v)
    debug('Init coloring ', coloring)
    return coloring


def get_unit_coloring(graph: "Graph"):
    coloring = Coloring()
    for v in graph.vertices:
        coloring.set(0, v)
    debug('Init coloring ', coloring)
    return coloring


def has_same_color_neignhours(u: "Vertex", v: "Vertex", coloring: "Coloring") -> bool:
    """
    Returns whether the vertices u and v have the same colored neighbourhood for the given coloring.

    :param u: vertex of which the neighbourhood must be compared
    :param v: vertex of which the neighbourhood must be compared
    :param coloring: coloring
    :return: `True` if the vertices have the same colored neighbourhood, `False` otherwise
    """
    ncolors_u = [coloring.color(w) for w in u.neighbours]
    ncolors_v = [coloring.color(w) for w in v.neighbours]
    return compare(ncolors_u, ncolors_v)


def get_vertices_of_graph(partition: List["Vertex"], g: "Graph") -> List["Vertex"]:
    """
    Returns the vertices of graph g in the given partition.

    :param partition:
    :param g:
    :return: a list of vertices belonging to graph g in the given partition. The list is empty if no vertices of graph g
    are found in the given partition
    """
    return [v for v in partition if g in v.graphs]


def count_isomorphism(g: "Graph", h: "Graph", coloring: "Coloring", count: bool=True) -> int:
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
    # TODO: make sure initial coloring is done
    new_coloring = color_refine(coloring)
    coloring_status = coloring.status(g, h)
    if coloring_status == "Unbalanced":
        return 0
    if coloring_status == "Bijection":
        return 1

    vertices = choose_color(new_coloring)
    first_vertex = choose_vertex(vertices, g)
    vertices_in_h = [v for v in vertices if v.in_graph(h)]
    number_isomorphisms = 0
    for second_vertex in vertices_in_h:
        adapted_coloring = create_partition(new_coloring, first_vertex, second_vertex)
        number_isomorphisms = number_isomorphisms + count_isomorphism(g, h, adapted_coloring)
        # for if you want to know if isomorphic and not number
        if not count and number_isomorphisms > 0:
            return number_isomorphisms
    return number_isomorphisms


def choose_color(coloring: "Coloring") -> List["Vertex"]:
    """
    Selects a partition with at least four vertices.

    Returns the first partition with at least four vertices that is found.
    :param coloring:
    :return: a partition with at least four vertices, `None` if no partition could be found
    """
    for key in coloring.colors:
        vertices = list(coloring.get(key))
        if len(vertices) >= 4 and len(vertices) % 2 == 0:
            return vertices
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
        if vertex.in_graph(g):
            return vertex
    return None


def create_partition(old_coloring: "Coloring", vertex1: "Vertex", vertex2: "Vertex") -> "Coloring":
    """
    Returns a new coloring where both vertices are in a new partition and removed from the one they belonged to.

    :param old_coloring: current coloring
    :param vertex1: vertex to be in the separate partition
    :param vertex2: vertex to be in the separate partition
    :return: a new coloring with vertex1 and vertex2 as a seperate partition
    """
    new_coloring = old_coloring.copy()
    new_color = new_coloring.next_color()
    new_coloring.recolor(vertex1, new_color)
    new_coloring.recolor(vertex2, new_color)
    return new_coloring


def color_refine(coloring: "Coloring") -> "Coloring":
    """
    Do the color refinement alg.
    :param graph: A graph G = (V,E)
    :param coloring: Initial coloring
    :return: The input Graph 'graph' and a stable coloring alpha_i of G
    """
    has_changed = True
    while has_changed:
        new_coloring = Coloring()
        for color in coloring.colors:
            vertices = coloring.get(color)
            while len(vertices) > 0:
                new_color = new_coloring.next_color()
                unbalanced = True
                u = vertices.pop()
                new_coloring.set(new_color, u)
                for v in list(vertices):
                    if has_same_color_neignhours(u, v, coloring):
                        new_coloring.set(new_color, v)
                        vertices.remove(v)
                        unbalanced = not unbalanced
            # Check if coloring is unbalanced, then we must stop
            if unbalanced: #len(new_coloring.get(new_color)) == 1: #TODO 1 or odd?
              debug('Coloring is unbalanced')
              return new_coloring

        debug('New coloring ', new_coloring)
        has_changed = (coloring.num_colors != new_coloring.num_colors)
        coloring = new_coloring

    debug('No changes found')

    return coloring


def get_number_isomorphisms(g: "Graph", h: "Graph", count: bool) -> int:
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
    return count_isomorphism(g, h, coloring, count)


def is_isomorphisms(g: "Graph", h: "Graph") -> bool:
    """
        Returns the number of isomorphisms for graph g and h.

        First, the coloring is initialized by degree of the vertices. Next, the number of isomorphisms is counted by
        applying the color-refinement algorithm and branching the
        :param g: graph for which to determine the number of isomorphisms
        :param h: graph for which to determine the number of isomorphisms
        :return: The number of isomorphisms for graph g and h
        """
    return get_number_isomorphisms(g, h, False) > 0


def get_number_automorphisms(g: "Graph") -> int:
    return get_number_isomorphisms(g, g.deepcopy(), True)


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