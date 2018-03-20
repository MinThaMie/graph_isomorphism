import unittest
from coloring_claudia import *


class TestPr2(unittest.TestCase):
    def helper(self, n_colors):
        g = Graph(False)
        vertices = [Vertex(g, i) for i in range(n_colors)]
        coloring = Coloring()
        color = coloring.next_color()
        for v in vertices:
            coloring.set(color, v)
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
            g.add_edge(Edge(vertices[head],vertices[tail]))
        return g


    def create_coloring_helper(self, graph: "Graph", map: "dict"):
        coloring = Coloring()
        for key in map:
            for value in map[key]:
                vertex = graph.find_vertex(value)
                coloring.set(key, vertex)
        return coloring


    def test_create_partition(self):
        g, vertices, coloring = self.helper(3)
        v_g1, v_g2, v_g3 = vertices
        # v_g1 = Vertex(g)
        # v_g2 = Vertex(g)
        # v_g3 = Vertex(g)
        # coloring = {0: [v_g1, v_g2, v_g3]}
        new_coloring = create_partition(coloring, v_g1, v_g2)
        self.assertEqual(2, new_coloring.num_colors) #__len__())
        self.assertListEqual([v_g1, v_g2], new_coloring.get(1))
        self.assertListEqual([v_g3],       new_coloring.get(0))

    def test_initialize_coloring(self):
        # empty graph
        g, v, coloring = self.helper(0)
        self.assertEqual(0, coloring.num_colors)

        # 1 - 2 - 3
        g = self.create_graph_helper([[1,2],[2,3]])
        v_g1, v_g2, v_g3 = g.vertices
        coloring = initialize_coloring(g)
        self.assertEqual(2, coloring.num_colors)
        self.assertListEqual([v_g1, v_g3], coloring.get(1))
        self.assertListEqual([v_g2],       coloring.get(2))
        # 1 - 2 - 3
        #     |
        #     4 - 6 - 7
        #     |
        #     5
        g = self.create_graph_helper([[1,2],[2,3],[2,4],[4,5],[4,6],[6,7]])
        v_g1, v_g2, v_g3, v_g4, v_g5, v_g6, v_g7 = g.vertices
        coloring = initialize_coloring(g)
        self.assertListEqual([v_g1, v_g3, v_g5, v_g7], coloring.get(1))
        self.assertListEqual([v_g6],                   coloring.get(2))
        self.assertListEqual([v_g2, v_g4],             coloring.get(3))
        # 1 - 2 - 3
        #     |
        #     4 - 6 - 7
        #     |
        #     5       8
        v_g8 = Vertex(g)
        g.add_vertex(v_g8)
        coloring = initialize_coloring(g)
        self.assertListEqual([v_g8],                   coloring.get(0))
        self.assertListEqual([v_g1, v_g3, v_g5, v_g7], coloring.get(1))
        self.assertListEqual([v_g6],                   coloring.get(2))
        self.assertListEqual([v_g2, v_g4],             coloring.get(3))

    def test_has_same_color_neighbours(self):
        g = self.create_graph_helper([[1,2],[2,3],[3,4],[3,5]])
        v_g1, v_g2, v_g3, v_g4, v_g5 = g.vertices
        coloring = self.create_coloring_helper(g, {0: [1], 1: [4,5], 2: [2], 3:[3]})

        self.assertTrue(has_same_color_neignhours(v_g4, v_g5, coloring))
        self.assertFalse(has_same_color_neignhours(v_g1, v_g4, coloring))

    def test_find_key(self):
        dictionary = {0: [0, 1, 2],
                      1: [1, 2, 3],
                      2: [4]}
        self.assertEqual(0, find_key(0, dictionary))
        self.assertEqual(0, find_key(1, dictionary))
        self.assertEqual(1, find_key(3, dictionary))
        self.assertEqual(2, find_key(4, dictionary))
        self.assertIsNone(find_key(5, dictionary))

    def test_is_unbalanced(self):
        balanced = {0: [1, 2],
                    1: [1, 2, 3, 4, 5, 6],
                    2: [1, 2, 3, 4]}
        unbalanced = {0: [1]}
        unbalanced2 = {0: [1, 2],
                       1: [1, 2, 3, 4, 5, 6],
                       2: [1, 2, 3]}
        self.assertFalse(is_unbalanced(balanced)) #TODO How to fix? My balanced method also checks if half of the vertex are from 1 graph and half from the other
        self.assertTrue(unbalanced)
        self.assertTrue(unbalanced2)

    def test_is_bijection(self):
        bijection = {0: [1, 2],
                     1: [1, 2],
                     2: [1, 2]}
        no_bijection = {0: [1, 2],
                        1: [1, 2, 3, 4],
                        2: [1, 2]}
        no_bijection2 = {0: [1, 2],
                         1: [1, 2],
                         2: [1, 2, 3, 4]}
        self.assertTrue(is_bijection(bijection))
        self.assertFalse(is_bijection(no_bijection))
        self.assertFalse(is_bijection(no_bijection2))

    def test_choose_partition(self):
        graph = Graph(directed=False, n=7)
        coloring = self.create_coloring_helper(graph, {0: [1, 2, 3, 4]})

        # coloring = {0: [1, 2, 3, 4]}
        coloring1 = {0: [1, 2],
                     1: [1, 2, 3, 4],
                     2: [1, 2, 3, 4, 5, 6]} #TODO: Cant have a vertex with more than one color
        coloring2 = {0: [1, 2],
                     1: [1, 2, 3, 4, 5]}
        self.assertListEqual([1, 2, 3, 4], choose_partition(coloring))
        self.assertListEqual([1, 2, 3, 4], choose_partition(coloring1))
        self.assertListEqual([],           choose_partition(coloring2))

    def test_choose_vertex(self):
        g = Graph(False)
        h = Graph(False)
        v_g = Vertex(g)
        v_g2 = Vertex(g)
        v_h = Vertex(h)
        self.assertEqual(v_g, choose_vertex([v_g, v_g2, v_h], g))
        self.assertEqual(v_h, choose_vertex([v_g, v_g2, v_h], h))
        self.assertEqual(v_g, choose_vertex([v_h, v_g],       g))
        self.assertIsNone(choose_vertex([v_g, v_g2], h))
        self.assertIsNone(choose_vertex([],          g))

    def test_get_vertices_of_graph(self):
        g = Graph(False)
        h = Graph(False)
        v_g = Vertex(g)
        v_g2 = Vertex(g)
        v_h = Vertex(h)
        self.assertListEqual([v_g, v_g2], get_vertices_of_graph([v_g, v_g2, v_h], g))
        self.assertListEqual([v_h],       get_vertices_of_graph([v_g, v_g2, v_h], h))
        self.assertListEqual([],          get_vertices_of_graph([v_h],       g))
        self.assertListEqual([],          get_vertices_of_graph([v_g, v_g2], h))
        self.assertListEqual([],          get_vertices_of_graph([],          g))

    def test_is_twins(self):
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
        self.assertTrue(is_twins(v1, v2))
        self.assertTrue(is_twins(v1, v3))
        self.assertTrue(is_twins(v2, v3))
        v4 = Vertex(g)
        e4 = Edge(v3, v4)
        g.add_edge(e4)
        self.assertFalse(is_twins(v3, v4))

    def test_get_twins(self):
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
        twins = get_twins(g) #TODO: returns a tuple of lists, but a list is expected below in the test
        print(twins)
        self.assertListEqual([(v1, v2), (v1, v3), (v2, v3)], twins)
        v4 = Vertex(g)
        e4 = Edge(v3, v4)
        g.add_edge(e4)
        self.assertListEqual([(v1, v2)], get_twins(g))

if __name__ == '__main__':
    unittest.main()
