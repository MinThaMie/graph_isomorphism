import unittest

from color_refiment_helper import *


class TestPr2(unittest.TestCase):
    def helper(self, n_colors):
        g = Graph(False)
        vertices = [Vertex(g, i) for i in range(n_colors)]
        coloring = Coloring()
        color = coloring.next_color()
        for v in vertices:
            coloring.set(v, color)
        return g, vertices, coloring

    def create_graph_helper(self, edges: List[List["Integer"]]):
        g = Graph(False)
        vertices = {}
        for edge in edges:
            head, tail = edge
            if head not in vertices:
                vertices[head] = Vertex(g, label=head)
                g.add_vertex(vertices[head])
            if tail not in vertices:
                vertices[tail] = Vertex(g, label=tail)
                g.add_vertex(vertices[tail])
            g.add_edge(Edge(vertices[head], vertices[tail]))
        return g

    def create_coloring_helper(self, graph: "Graph", map: "dict"):
        coloring = Coloring()
        for color in map:
            for value in map[color]:
                vertex = graph.find_vertex(value)
                coloring.set(vertex, color)
        return coloring

    def test_create_partition(self):
        g, vertices, coloring = self.helper(3)
        v_g1, v_g2, v_g3 = vertices
        # v_g1 = Vertex(g)
        # v_g2 = Vertex(g)
        # v_g3 = Vertex(g)
        # coloring = {0: [v_g1, v_g2, v_g3]}
        new_coloring = create_new_color_class(coloring, v_g1, v_g2)
        self.assertEqual(2, len(new_coloring))  # __len__())
        self.assertListEqual([v_g1, v_g2], new_coloring.get(1))
        self.assertListEqual([v_g3], new_coloring.get(0))

    def test_initialize_coloring(self):
        # empty graph
        g, v, coloring = self.helper(0)
        self.assertEqual(0, len(coloring))

        # 1 - 2 - 3
        g = self.create_graph_helper([[1, 2], [2, 3]])
        v_g1, v_g2, v_g3 = g.vertices
        coloring = initialize_coloring(g)
        self.assertEqual(2, len(coloring))
        self.assertListEqual([v_g1, v_g3], coloring.get(1))
        self.assertListEqual([v_g2], coloring.get(2))
        # 1 - 2 - 3
        #     |
        #     4 - 6 - 7
        #     |
        #     5
        g = self.create_graph_helper([[1, 2], [2, 3], [2, 4], [4, 5], [4, 6], [6, 7]])
        v_g1, v_g2, v_g3, v_g4, v_g5, v_g6, v_g7 = g.vertices
        coloring = initialize_coloring(g)
        self.assertListEqual([v_g1, v_g3, v_g5, v_g7], coloring.get(1))
        self.assertListEqual([v_g6], coloring.get(2))
        self.assertListEqual([v_g2, v_g4], coloring.get(3))
        # 1 - 2 - 3
        #     |
        #     4 - 6 - 7
        #     |
        #     5       8
        v_g8 = Vertex(g)
        g.add_vertex(v_g8)
        coloring = initialize_coloring(g)
        self.assertListEqual([v_g8], coloring.get(0))
        self.assertListEqual([v_g1, v_g3, v_g5, v_g7], coloring.get(1))
        self.assertListEqual([v_g6], coloring.get(2))
        self.assertListEqual([v_g2, v_g4], coloring.get(3))

    def test_has_same_color_neighbours(self):
        g = self.create_graph_helper([[1, 2], [2, 3], [3, 4], [3, 5]])
        v_g1, v_g2, v_g3, v_g4, v_g5 = g.vertices
        coloring = self.create_coloring_helper(g, {0: [1], 1: [4, 5], 2: [2], 3: [3]})

        self.assertTrue(has_same_color_neighbours(v_g4, v_g5, coloring))
        self.assertFalse(has_same_color_neighbours(v_g1, v_g4, coloring))

    # TODO: Rewrite
    # def test_is_unbalanced(self):
    #     graph = self.create_graph_helper([[1, 2], [3, 4],[5,6]])
    #     balanced = self.create_coloring_helper(graph,{0: [1, 2],
    #                 1: [1, 2, 3, 4, 5, 6],
    #                 2: [1, 2, 3, 4]})
    #     unbalanced = self.create_coloring_helper(graph,{0: [1]})
    #     unbalanced2 = self.create_coloring_helper(graph,{0: [1, 2],
    #                    1: [1, 2, 3, 4, 5, 6],
    #                    2: [1, 2, 3]})
    #     self.assertFalse(is_unbalanced(balanced))
    #     self.assertTrue(unbalanced)
    #     self.assertTrue(unbalanced2)

    # TODO: Rewrite
    # def test_is_bijection(self):
    #     graph = self.create_graph_helper([[1, 2], [3, 4]])
    #     bijection = self.create_coloring_helper(graph, {0: [1, 2],
    #                  2: [3, 4]})
    #     no_bijection = self.create_coloring_helper(graph, {0: [1, 2],
    #                     1: [1, 2, 3, 4],
    #                     2: [1, 2]})
    #     no_bijection2 = self.create_coloring_helper(graph,{0: [1, 2],
    #                      1: [1, 2],
    #                      2: [1, 2, 3, 4]})
    #     self.assertTrue(bijection.status(graph,graph) == "Bijection")
    #     self.assertFalse(no_bijection.status != "Bijection")
    #     self.assertFalse(no_bijection2.status == "Bijection")

    def test_choose_color(self):
        graph = self.create_graph_helper([[1, 2], [3, 4], [5, 6], [7, 8]])
        vertices = sorted(graph.vertices, key=Vertex.__str__)

        coloring = self.create_coloring_helper(graph, {0: [1, 2, 3, 4]})
        self.assertListEqual(vertices[:4], choose_color(coloring))

        # TODO: replace this with new tests from Claudia's PR
        # coloring1 = self.create_coloring_helper(graph, {0: [1, 2],
        #                                                 1: [1, 2, 3, 4],
        #                                                 2: [1, 2, 3, 4, 5, 6]})
        # self.assertListEqual(vertices[:4], sorted(choose_color(coloring1), key=Vertex.__str__))
        #
        # coloring2 = self.create_coloring_helper(graph, {0: [1, 2],
        #                                                 1: [1, 2, 3, 4, 5]})
        # self.assertListEqual([], choose_color(coloring2))

    def test_choose_vertex(self):
        g = Graph(False)
        h = Graph(False)
        v_g = Vertex(g)
        v_g2 = Vertex(g)
        v_h = Vertex(h)
        self.assertEqual(v_g, choose_vertex([v_g, v_g2, v_h], g))
        self.assertEqual(v_h, choose_vertex([v_g, v_g2, v_h], h))
        self.assertEqual(v_g, choose_vertex([v_h, v_g], g))
        self.assertIsNone(choose_vertex([v_g, v_g2], h))
        self.assertIsNone(choose_vertex([], g))

    def test_get_vertices_of_graph(self):
        g = Graph(False)
        h = Graph(False)
        v_g = Vertex(g)
        v_g2 = Vertex(g)
        v_h = Vertex(h)
        self.assertListEqual([v_g, v_g2], get_vertices_of_graph([v_g, v_g2, v_h], g))
        self.assertListEqual([v_h], get_vertices_of_graph([v_g, v_g2, v_h], h))
        self.assertListEqual([], get_vertices_of_graph([v_h], g))
        self.assertListEqual([], get_vertices_of_graph([v_g, v_g2], h))
        self.assertListEqual([], get_vertices_of_graph([], g))

    def test_are_twins(self):
        g = Graph(False)
        v1 = Vertex(g)
        v2 = Vertex(g)
        v3 = Vertex(g)
        e1 = Edge(v1, v2)
        e2 = Edge(v1, v3)
        e3 = Edge(v2, v3)
        g.add_edge(e1)
        g.add_edge(e2)
        g.add_edge(e3)
        self.assertTrue(are_twins(v1, v2))
        self.assertTrue(are_twins(v1, v3))
        self.assertTrue(are_twins(v2, v3))
        v4 = Vertex(g)
        e4 = Edge(v3, v4)
        g.add_edge(e4)
        self.assertFalse(are_twins(v3, v4))

    def test_get_twins(self):
        g = Graph(False)
        v1 = Vertex(g)
        v2 = Vertex(g)
        v3 = Vertex(g)
        e1 = Edge(v1, v2)
        e2 = Edge(v1, v3)
        g.add_edge(e1)
        g.add_edge(e2)
        twins, false_twins = get_twins(g)
        self.assertListEqual([], twins)
        self.assertListEqual([(v2, v3)], false_twins)
        e3 = Edge(v2, v3)
        g.add_edge(e3)
        twins, false_twins = get_twins(g)
        self.assertListEqual([(v1, v2), (v1, v3), (v2, v3)], twins)
        self.assertListEqual([], false_twins)
        v4 = Vertex(g)
        e4 = Edge(v3, v4)
        g.add_edge(e4)
        twins, false_twins = get_twins(g)
        self.assertListEqual([(v1, v2)], twins)
        self.assertListEqual([], false_twins)

    def test_get_twins_module(self):
        g = Graph(False)
        v0 = Vertex(g)
        v1 = Vertex(g)
        v2 = Vertex(g)
        v3 = Vertex(g)
        v4 = Vertex(g)
        v5 = Vertex(g)
        v6 = Vertex(g)
        v7 = Vertex(g)
        e1 = Edge(v0, v1)
        e2 = Edge(v0, v2)
        e3 = Edge(v0, v3)
        e4 = Edge(v1, v2)
        e5 = Edge(v1, v3)
        e6 = Edge(v1, v4)
        e7 = Edge(v2, v3)
        e8 = Edge(v4, v5)
        e9 = Edge(v5, v6)
        e10 = Edge(v5, v7)
        e11 = Edge(v6, v7)
        g.add_edge(e1)
        g.add_edge(e2)
        g.add_edge(e3)
        g.add_edge(e4)
        g.add_edge(e5)
        g.add_edge(e6)
        g.add_edge(e7)
        g.add_edge(e8)
        g.add_edge(e9)
        g.add_edge(e10)
        g.add_edge(e11)
        twins, false_twins = get_twins(g)
        self.assertListEqual([(v0, v2), (v0, v3), (v2, v3), (v6, v7)], twins)
        self.assertListEqual([], false_twins)


if __name__ == '__main__':
    unittest.main()
