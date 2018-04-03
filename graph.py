"""
This is a module for working with directed and undirected multigraphs.
"""
# version: 29-01-2015, Paul Bonsma
# version: 01-02-2017, Pieter Bos, Tariq Bontekoe
# version: 13-37-1337, NU2 🎓

from typing import List, Union, Set


class GraphError(Exception):
    """An error that occurs while manipulating a `Graph`."""

    def __init__(self, message: str):
        """Instantiate a graph error.

        :param str message: The error message.
        """

        super(GraphError, self).__init__(message)


class Vertex(object):
    """`Vertex` objects belong to graph objects. They have an attribute `label` which can be anything."""

    def __init__(self, graph: "Graph", label=None):
        """Instantiate a vertex, part of the specified graph.

        :param Graph graph: The graph that this vertex is a part of.
        :param label: Optional parameter to specify a label for this vertex
        """

        if label is None:
            label = graph._next_label()

        self._graphs = [graph]
        self._incidence = {}
        self._label = label

    def __repr__(self):
        """A programmer-friendly representation of this vertex.

        :return: The string to approximate the constructor arguments of the `Vertex'
        """

        return 'Vertex(label={}, #incident={})'.format(self.label, len(self._incidence))

    def __str__(self) -> str:
        """A user-friendly representation of the vertex, that is, its label.

        :return: The string representation of the label.
        """

        return str(self._label)

    def is_adjacent(self, other: "Vertex") -> bool:
        """Returns True iff this vertex is adjacent to the specified other vertex.

        :param Vertex other: The other vertex
        """

        return other in self._incidence

    def _add_incidence(self, edge: "Edge"):
        """Add an edge to the incidence map of this vertex.

        :param Edge edge: The edge to add.
        """

        other = edge.other_end(self)

        if other not in self._incidence:
            self._incidence[other] = set()

        self._incidence[other].add(edge)

    def remove_incidence(self, edge):
        other = edge.other_end(self)

        if other in self._incidence:
            self._incidence[other].remove(edge)
            if len(self._incidence[other]) == 0:
                self._incidence.pop(other)

    def add_graph(self, graph: "Graph"):
        if graph not in self._graphs:
            self._graphs.append(graph)

    def in_graph(self, graph: "Graph") -> bool:
        return graph in self._graphs

    @property
    def graphs(self) -> List["Graph"]:
        """The graphs this vertex belongs to.

        :return: List of graphs this vertex belongs to.
        """

        return self._graphs

    @property
    def incidence(self) -> List["Edge"]:
        """Get incidence, i.e. the list of edges incident with this vertex.

        :return: The list of edges incident with this vertex
        """

        result = set()

        for edge_set in self._incidence.values():
            result |= edge_set

        return list(result)

    @property
    def neighbours(self) -> ["Vertex"]:
        """Get the list of neighbours of the vertex."""

        return list(self._incidence.keys())

    @property
    def degree(self) -> int:
        """Get the degree of the vertex."""

        return sum(map(len, self._incidence.values()))

    @property
    def label(self) -> int:
        return self._label

    @label.setter
    def label(self, label):
        self._label = label


class Edge(object):
    """An edge has a tail and a head which point to the end vertices. The order of these matters if the graph is
    directed."""

    def __init__(self, tail: Vertex, head: Vertex, weight=None):
        """Create an edge between vertices `tail` and `head`.

        :param Vertex tail: In case the graph is directed, this is the tail of the arrow.
        :param Vertex head: In case the graph is directed, this is the head of the arrow.
        :param weight: Optional weight of the vertex, which can be any type, but usually is a number.
        """

        self._tail = tail
        self._head = head
        self._weight = weight

    def __repr__(self):
        """A programmer-friendly representation of this edge.

        :return: The string to approximate the constructor arguments of this edge.
        """

        return 'Edge(head={}, tail={}, weight={})'.format(self.head.label, self.tail.label, self.weight)

    def __str__(self) -> str:
        """A user friendly representation of this edge.

        :return: A user friendly representation of this edge.
        """

        return '({}, {})'.format(str(self.tail), str(self.head))

    @property
    def tail(self) -> "Vertex":
        """In case the graph is directed, this represents the tail of the arrow.

        :return: The tail of this edge.
        """

        return self._tail

    @property
    def head(self) -> "Vertex":
        """In case the graph is directed, this represents the head of the arrow.

        :return: The head of this edge.
        """

        return self._head

    @property
    def weight(self):
        """The weight of this edge, which can also just be used as a generic label.

        :return: The weight of this edge
        """

        return self._weight

    def other_end(self, vertex: Vertex) -> Vertex:
        """Given one end vertex of the edge, this returns the other end vertex.

        :param Vertex vertex: One end's vertex.
        :return: The other end's vertex.
        """

        if self.tail == vertex:
            return self.head
        elif self.head == vertex:
            return self.tail

        raise GraphError(
            'edge.other_end(vertex): vertex must be head or tail of edge')

    def incident(self, vertex: Vertex) -> bool:
        """Determine if this edge is incident with the specified vertex.

        :param Vertex vertex: The vertex.
        :return: Whether the vertex is incident with the edge.
        """

        return self.head == vertex or self.tail == vertex


class Graph(object):
    disjoint_union_operator = '⊎'

    def __init__(self, directed: bool, n: int = 0, simple: bool = False, name: str = 'G'):
        """Instantiate a graph.

        :param bool directed: Whether the graph should behave as a directed graph.
        :param bool simple: Whether the graph should be a simple graph, i.e., not have multi-edges or loops.
        :param int n: Optional, the number of default vertices the graph should instantiate and add immediately.
        :param str name: Optional name for the graph.
        """

        self._v = list()
        self._e = list()
        self._simple = simple
        self._directed = directed
        self._next_label_value = 0
        self._name = name

        for i in range(n):
            self.add_vertex(Vertex(self))

    def __repr__(self):
        """A programmer-friendly representation of this graph.

        :return: The string to approximate the constructor arguments of this graph.
        """

        return 'Graph(' \
               f'name={self.name}, ' \
               f'directed={self._directed}, ' \
               f'simple={self._simple}, ' \
               f'#edges={len(self._e)}, ' \
               f'#vertices={len(self._v)}' \
               ')'

    def __str__(self) -> str:
        """A user-friendly representation of this graph.

        :return: A textual representation of the vertices and edges of this graph.
        """

        return self._name + ':\n' \
                            'V=[' + ", ".join(map(str, self._v)) + ']\n' \
                                                                   'E=[' + ", ".join(map(str, self._e)) + ']'

    def _next_label(self) -> int:
        """Generate a unique label for vertices in the graph.

        :return: A unique label.
        """

        result = self._next_label_value
        self._next_label_value += 1
        return result

    @property
    def name(self) -> str:
        """Name of the graph.

        :return: Name of the graph
        """

        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def simple(self) -> bool:
        """Whether this graph is a simple graph, i.e., it does not have multi-edges or loops.

        :return: Whether this graph is simple.
        """

        return self._simple

    @property
    def directed(self) -> bool:
        """Whether this graph behaves as a directed graph.

        :return: Whether the graph is directed.
        """

        return self._directed

    @property
    def vertices(self) -> List["Vertex"]:
        """:return: The list of vertices of this graph."""

        return list(self._v)

    @property
    def edges(self) -> List["Edge"]:
        """:return: The list of edges of this graph."""

        return list(self._e)

    @property
    def order(self) -> int:
        """The number of vertices of this graph."""
        return len(self.vertices)

    @property
    def size(self) -> int:
        """The number of edges of this graph."""

        return len(self.edges)

    def __iter__(self):
        """:return: Returns an iterator for the vertices of the graph."""

        return iter(self._v)

    def add_vertex(self, vertex: "Vertex"):
        """Add a vertex to this graph.

        :param Vertex vertex: The vertex to be added.
        """

        vertex.graphs.append(self)
        self._v.append(vertex)

    def add_edge(self, edge: "Edge"):
        """Add an edge to this graph and, if necessary, also the vertices of the edge. This includes some checks
        whether or not the graph should stay simple.

        :param edge: The edge to be added.
        """

        if self._simple:
            if edge.tail == edge.head:
                raise GraphError('No loops allowed in simple graphs')

            if self.is_adjacent(edge.tail, edge.head):
                raise GraphError('No multiedges allowed in simple graphs')

        if edge.tail not in self._v:
            self.add_vertex(edge.tail)
        if edge.head not in self._v:
            self.add_vertex(edge.head)

        self._e.append(edge)

        edge.head._add_incidence(edge)
        edge.tail._add_incidence(edge)

    def deepcopy(self) -> "Graph":
        G = Graph(self.directed)
        for v in self.vertices:
            v_copy = Vertex(G)
            v_copy.label = v.label
            G.add_vertex(v_copy)
        for e in self.edges:
            tail = e.tail
            tail_copy = G.find_vertex(tail.label)
            head = e.head
            head_copy = G.find_vertex(head.label)
            e_copy = Edge(tail_copy, head_copy)
            G.add_edge(e_copy)
        return G

    def find_vertex(self, label: int) -> "Vertex":
        for v in self._v:
            if v.label == label:
                return v

    def __add__(self, other: "Graph") -> "Graph":
        """Make a disjoint union of two graphs.

        :param Graph other: The other graph to form a disjoint union with.
        :return: A new graph instance being the disjoint union of this graph and the other.
        """

        disjoint_union_name = ''
        if self.name and other.name:
            disjoint_union_name = f'{self.name} {Graph.disjoint_union_operator} {other.name}'

        disjoint_union = Graph(
            directed=self.directed or other.directed,
            n=0,
            simple=self.simple and other.simple,
            name=disjoint_union_name
        )

        for vertex in self.vertices + other.vertices:
            disjoint_union.add_vertex(vertex)

        for edge in self.edges + other.edges:
            disjoint_union.add_edge(edge)

        return disjoint_union

    def __iadd__(self, other: Union['Graph', Vertex, Edge]) -> "Graph":
        """Add a graph, vertex or edge to this graph with the += syntax.

        :param other: The graph, vertex or edge to be added.
        :return: In case of a graph: this method returns a new graph instance being the disjoint union of the two
                 graphs. Otherwise this method modifies this graph object and returns it.
        """

        if isinstance(other, Graph):
            return self + other

        if isinstance(other, Vertex):
            self.add_vertex(other)

        if isinstance(other, Edge):
            self.add_edge(other)

        return self

    def edge_exists(self, u: "Vertex", v: "Vertex") -> bool:
        return len(self.find_edge(u, v)) == 0

    def find_edge(self, u: "Vertex", v: "Vertex") -> Set["Edge"]:
        """Find edges in this graph between the specified vertices.

        :param Vertex u: One vertex.
        :param Vertex v: Another vertex.
        :return: The set of edges incident with both `u` and `v`.
        """

        result = set(x for x in u.incidence if x == v)
        # result |= u.incidence.get(v, set())

        if not self._directed:
            result.union(set(x for x in v.incidence if x == u))
            # result |= v.incidence.get(u, set())

        return result

    def is_adjacent(self, u: "Vertex", v: "Vertex") -> bool:
        """Check if the specified vertices are adjacent. If the graph is directed, the direction of the edges is
        respected.

        :param Vertex u: One vertex.
        :param Vertex v: Another vertex.
        :return: Whether the vertices are adjacent.
        """

        return v in u.neighbours and (not self.directed or any(e.head == v for e in u.incidence))

    def del_edge(self, edge: "Edge"):
        """Delete the specified edge.

        :param Edge edge: the edge to delete.
        """

        edge.tail.remove_incidence(edge)
        edge.head.remove_incidence(edge)

        self._e.remove(edge)

    def del_vertex(self, v: "Vertex"):
        """Delete the specified vertex.

        :param Vertex v: The vertex to be removed.
        """

        for e in v.incidence:
            self.del_edge(e)

        v.graphs.remove(self)
        self._v.remove(v)

    def complement(self) -> 'Graph':
        """Instantiate this graph's complement.

        :return A new graph instance being this graph's complement. It has new vertex instances and, by definition, new
                edges.
        """

        complement = Graph(directed=self.directed, simple=self.simple, name='complement of ' + self.name)

        # Map current vertices to copies for complement
        current_complement_vertices = {vertex: Vertex(graph=complement, label=vertex.label) for vertex in list(self._v)}

        while len(current_complement_vertices) > 0:
            current_vertex, complement_vertex = current_complement_vertices.popitem()

            if complement_vertex not in complement.vertices:
                complement.add_vertex(complement_vertex)

            complement_neighbours = {
                complement_neighbour
                for current_neighbour, complement_neighbour in current_complement_vertices.items()
                if not current_vertex.is_adjacent(current_neighbour)
            }

            for complement_neighbour in complement_neighbours:
                complement.add_edge(Edge(tail=complement_vertex, head=complement_neighbour))

        return complement
