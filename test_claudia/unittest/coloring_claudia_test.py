import unittest
from practicum2 import *


class TestPr2(unittest.TestCase):

    def test_create_partition(self):
        g = Graph(False)
        v_g1 = Vertex(g)
        v_g2 = Vertex(g)
        v_g3 = Vertex(g)
        coloring = {0: [v_g1, v_g2, v_g3]}
        new_coloring = create_partition(coloring, v_g1, v_g2)
        self.assertEqual(2, new_coloring.__len__())
        self.assertListEqual([v_g1, v_g2], new_coloring[0])
        self.assertListEqual([v_g3],       new_coloring[1])

    def test_initialize_coloring(self):
        # empty graph
        g = Graph(False)
        coloring = initialize_coloring(g)
        self.assertEqual(0, coloring.__len__())
        # 1 - 2 - 3
        v_g1 = Vertex(g)
        v_g2 = Vertex(g)
        v_g3 = Vertex(g)
        e_g1 = Edge(v_g1, v_g2)
        e_g2 = Edge(v_g2, v_g3)
        g.add_edge(e_g1)
        g.add_edge(e_g2)
        coloring = initialize_coloring(g)
        self.assertEqual(2, coloring.__len__())
        self.assertListEqual([v_g1, v_g3], coloring[1])
        self.assertListEqual([v_g2],       coloring[2])
        # 1 - 2 - 3
        #     |
        #     4 - 6 - 7
        #     |
        #     5
        v_g4 = Vertex(g)
        v_g5 = Vertex(g)
        v_g6 = Vertex(g)
        v_g7 = Vertex(g)
        e_g3 = Edge(v_g2, v_g4)
        e_g4 = Edge(v_g4, v_g5)
        e_g5 = Edge(v_g4, v_g6)
        e_g6 = Edge(v_g6, v_g7)
        g.add_edge(e_g3)
        g.add_edge(e_g4)
        g.add_edge(e_g5)
        g.add_edge(e_g6)
        coloring = initialize_coloring(g)
        self.assertListEqual([v_g1, v_g3, v_g5, v_g7], coloring[1])
        self.assertListEqual([v_g6],                   coloring[2])
        self.assertListEqual([v_g2, v_g4],             coloring[3])
        # 1 - 2 - 3
        #     |
        #     4 - 6 - 7
        #     |
        #     5       8
        v_g8 = Vertex(g)
        g.add_vertex(v_g8)
        coloring = initialize_coloring(g)
        self.assertListEqual([v_g8],                   coloring[0])
        self.assertListEqual([v_g1, v_g3, v_g5, v_g7], coloring[1])
        self.assertListEqual([v_g6],                   coloring[2])
        self.assertListEqual([v_g2, v_g4],             coloring[3])

    def test_has_same_color_neighbours(self):
        g = Graph(False)
        v_g1 = Vertex(g)
        v_g2 = Vertex(g)
        v_g3 = Vertex(g)
        v_g4 = Vertex(g)
        v_g5 = Vertex(g)
        e_g1 = Edge(v_g1, v_g2)
        e_g2 = Edge(v_g2, v_g3)
        e_g3 = Edge(v_g3, v_g4)
        e_g4 = Edge(v_g3, v_g5)
        g.add_edge(e_g1)
        g.add_edge(e_g2)
        g.add_edge(e_g3)
        g.add_edge(e_g4)
        coloring = {0: [v_g1],
                    1: [v_g4, v_g5],
                    2: [v_g2],
                    3: [v_g3]}
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
        self.assertFalse(is_unbalanced(balanced))
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
        coloring = {0: [1, 2, 3, 4]}
        coloring1 = {0: [1, 2],
                     1: [1, 2, 3, 4],
                     2: [1, 2, 3, 4, 5, 6]}
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
        twins = get_twins(g)
        print(twins)
        self.assertListEqual([(v1, v2), (v1, v3), (v2, v3)], twins)
        v4 = Vertex(g)
        e4 = Edge(v3, v4)
        g.add_edge(e4)
        self.assertListEqual([(v1, v2)], get_twins(g))

if __name__ == '__main__':
    unittest.main()
