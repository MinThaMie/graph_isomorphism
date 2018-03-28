from graph import *


def graph_vertex2edge1() -> Graph:
    """
        Create a graph with structure:

        1 - 2

        :return: The created graph
        """
    v2e1 = Graph(False)
    v_g1 = Vertex(v2e1)
    v_g2 = Vertex(v2e1)
    e_g = Edge(v_g1, v_g2)
    v2e1.add_edge(e_g)
    return v2e1


def graph_vertex3edge2() -> Graph:
    """
        Create a graph with structure:

        1 - 2 - 3

        :return: The created graph
        """
    v3e2 = Graph(False, name='G')
    v_g1 = Vertex(v3e2)
    v_g2 = Vertex(v3e2)
    v_g3 = Vertex(v3e2)
    e_g1 = Edge(v_g1, v_g2)
    e_g2 = Edge(v_g2, v_g3)
    v3e2.add_edge(e_g1)
    v3e2.add_edge(e_g2)
    return v3e2


def graph_vertex4edge4() -> Graph:
    """
        Create a graph with structure:

        1 - 2 - 3
         \ /
          4

        :return: The created graph
        """
    v4e4 = Graph(False)
    v_g1 = Vertex(v4e4)
    v_g2 = Vertex(v4e4)
    v_g3 = Vertex(v4e4)
    v_g4 = Vertex(v4e4)
    e_g1 = Edge(v_g1, v_g2)
    e_g2 = Edge(v_g2, v_g3)
    e_g3 = Edge(v_g2, v_g4)
    e_g4 = Edge(v_g3, v_g4)
    v4e4.add_edge(e_g1)
    v4e4.add_edge(e_g2)
    v4e4.add_edge(e_g3)
    v4e4.add_edge(e_g4)
    return v4e4


def graph_vertex5edge4() -> Graph:
    """
        Create a graph with structure:

        1 - 2 - 3 - 4
                |
                5

    :return: The created graph
    """
    v4e4 = Graph(False)
    v_h1 = Vertex(v4e4)
    v_h2 = Vertex(v4e4)
    v_h3 = Vertex(v4e4)
    v_h4 = Vertex(v4e4)
    v_h5 = Vertex(v4e4)
    e_h1 = Edge(v_h1, v_h2)
    e_h2 = Edge(v_h2, v_h3)
    e_h3 = Edge(v_h3, v_h4)
    e_h4 = Edge(v_h3, v_h5)
    v4e4.add_edge(e_h1)
    v4e4.add_edge(e_h2)
    v4e4.add_edge(e_h3)
    v4e4.add_edge(e_h4)
    return v4e4


def graph_vertex5edge4loop() -> Graph:
    """
        Create a graph with structure:

        1 - 2 - 3   4
                |
                5

    :return: The created graph
    """
    v5e4loop = Graph(False)
    v_h1 = Vertex(v5e4loop)
    v_h2 = Vertex(v5e4loop)
    v_h3 = Vertex(v5e4loop)
    v_h4 = Vertex(v5e4loop)
    v_h5 = Vertex(v5e4loop)
    e_h1 = Edge(v_h1, v_h2)
    e_h2 = Edge(v_h2, v_h3)
    e_h3 = Edge(v_h4, v_h4)
    e_h4 = Edge(v_h3, v_h5)
    v5e4loop.add_edge(e_h1)
    v5e4loop.add_edge(e_h2)
    v5e4loop.add_edge(e_h3)
    v5e4loop.add_edge(e_h4)
    return v5e4loop
