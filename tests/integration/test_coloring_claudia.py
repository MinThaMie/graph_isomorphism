import unittest

from color_refinement import *


class TestPr2(unittest.TestCase):

    def test_count_isomorphism_unbalanced(self):
        g = Graph(False, 3)
        h = Graph(False)
        v_h1 = Vertex(h)
        v_h2 = Vertex(h)
        v_h3 = Vertex(h)
        e_h1 = Edge(v_h1, v_h2)
        e_h2 = Edge(v_h2, v_h3)
        h.add_edge(e_h1)
        h.add_edge(e_h2)
        G = g + h
        coloring = initialize_coloring(G)
        coloring = color_refine(coloring)
        self.assertEqual(0, count_isomorphism(g, h, coloring))

    def test_count_isomorphism_bijection(self):
        g = Graph(False, 1)
        h = Graph(False, 1)
        G = g + h
        coloring = initialize_coloring(G)
        coloring = color_refine(coloring)
        self.assertEqual(1, count_isomorphism(g, h, coloring))

    def test_count_isomorphism_recursive(self):
        # g: 1 - 2 - 3
        #         \ /
        #          4
        g = Graph(False)
        v_g1 = Vertex(g)
        v_g2 = Vertex(g)
        v_g3 = Vertex(g)
        v_g4 = Vertex(g)
        e_g1 = Edge(v_g1, v_g2)
        e_g2 = Edge(v_g2, v_g3)
        e_g3 = Edge(v_g2, v_g4)
        e_g4 = Edge(v_g3, v_g4)
        g.add_edge(e_g1)
        g.add_edge(e_g2)
        g.add_edge(e_g3)
        g.add_edge(e_g4)
        # h: 1 - 2 - 3
        #         \ /
        #          4
        h = Graph(False)
        v_h1 = Vertex(h)
        v_h2 = Vertex(h)
        v_h3 = Vertex(h)
        v_h4 = Vertex(h)
        e_h1 = Edge(v_h1, v_h2)
        e_h2 = Edge(v_h2, v_h3)
        e_h3 = Edge(v_h2, v_h4)
        e_h4 = Edge(v_h3, v_h4)
        h.add_edge(e_h1)
        h.add_edge(e_h2)
        h.add_edge(e_h3)
        h.add_edge(e_h4)
        G = g + h
        coloring = initialize_coloring(G)
        self.assertEqual(2, count_isomorphism(g, h, coloring))

    def test_color_refinement_small(self):
        # g: 1 - 2 - 3
        g = Graph(False, name='G')
        v_g1 = Vertex(g)
        v_g2 = Vertex(g)
        v_g3 = Vertex(g)
        e_g1 = Edge(v_g1, v_g2)
        e_g2 = Edge(v_g2, v_g3)
        g.add_edge(e_g1)
        g.add_edge(e_g2)
        # h: 4 - 5 - 6
        h = Graph(False, name='H')
        v_h1 = Vertex(h)
        v_h2 = Vertex(h)
        v_h3 = Vertex(h)
        e_h1 = Edge(v_h1, v_h2)
        e_h2 = Edge(v_h2, v_h3)
        h.add_edge(e_h1)
        h.add_edge(e_h2)
        coloring = color_refine(initialize_coloring(g + h))
        self.assertEqual(2, coloring.num_colors)
        self.assertListEqual([v_h3, v_g1, v_g3, v_h1], coloring.get(0))
        self.assertListEqual([v_h2, v_g2], coloring.get(1))

    def test_color_refinement_large(self):
        # g: 1 - 2 - 3 - 4 - 6
        #             \ /
        #              5
        g = Graph(False)
        v_g1 = Vertex(g)
        v_g2 = Vertex(g)
        v_g3 = Vertex(g)
        v_g4 = Vertex(g)
        v_g5 = Vertex(g)
        v_g6 = Vertex(g)
        e_g1 = Edge(v_g1, v_g2)
        e_g2 = Edge(v_g2, v_g3)
        e_g3 = Edge(v_g3, v_g4)
        e_g4 = Edge(v_g4, v_g6)
        e_g5 = Edge(v_g3, v_g5)
        e_g6 = Edge(v_g4, v_g5)
        g.add_edge(e_g1)
        g.add_edge(e_g2)
        g.add_edge(e_g3)
        g.add_edge(e_g4)
        g.add_edge(e_g5)
        g.add_edge(e_g6)
        # h: 1 - 2 - 3 - 4
        #             \ /
        #              5 - 6
        h = Graph(False)
        v_h1 = Vertex(h)
        v_h2 = Vertex(h)
        v_h3 = Vertex(h)
        v_h4 = Vertex(h)
        v_h5 = Vertex(h)
        v_h6 = Vertex(h)
        e_h1 = Edge(v_h1, v_h2)
        e_h2 = Edge(v_h2, v_h3)
        e_h3 = Edge(v_h3, v_h4)
        e_h4 = Edge(v_h3, v_h5)
        e_h5 = Edge(v_h4, v_h5)
        e_h6 = Edge(v_h5, v_h6)
        h.add_edge(e_h1)
        h.add_edge(e_h2)
        h.add_edge(e_h3)
        h.add_edge(e_h4)
        h.add_edge(e_h5)
        h.add_edge(e_h6)
        coloring = color_refine(initialize_coloring(g + h))
        self.assertEqual(6, coloring.num_colors)
        self.assertListEqual([v_g1, v_h1], coloring.get(1))
        self.assertListEqual([v_g6, v_h6], coloring.get(0))

    def test_get_number_isomorphisms_unbalanced(self):
        g = Graph(False, 3)
        h = Graph(False)
        v_h1 = Vertex(h)
        v_h2 = Vertex(h)
        v_h3 = Vertex(h)
        e_h1 = Edge(v_h1, v_h2)
        e_h2 = Edge(v_h2, v_h3)
        h.add_edge(e_h1)
        h.add_edge(e_h2)
        self.assertEqual(0, get_number_isomorphisms(g, h, True))

    def test_get_number_isomorphisms_bijection(self):
        g = Graph(False, 1)
        h = Graph(False, 1)
        self.assertEqual(1, get_number_isomorphisms(g, h, True))

    def test_get_number_isomorphisms_recursive(self):
        # g: 1 - 2 - 3
        #         \ /
        #          4
        g = Graph(False)
        v_g1 = Vertex(g)
        v_g2 = Vertex(g)
        v_g3 = Vertex(g)
        v_g4 = Vertex(g)
        e_g1 = Edge(v_g1, v_g2)
        e_g2 = Edge(v_g2, v_g3)
        e_g3 = Edge(v_g2, v_g4)
        e_g4 = Edge(v_g3, v_g4)
        g.add_edge(e_g1)
        g.add_edge(e_g2)
        g.add_edge(e_g3)
        g.add_edge(e_g4)
        # h: 1 - 2 - 3
        #         \ /
        #          4
        h = Graph(False)
        v_h1 = Vertex(h)
        v_h2 = Vertex(h)
        v_h3 = Vertex(h)
        v_h4 = Vertex(h)
        e_h1 = Edge(v_h1, v_h2)
        e_h2 = Edge(v_h2, v_h3)
        e_h3 = Edge(v_h2, v_h4)
        e_h4 = Edge(v_h3, v_h4)
        h.add_edge(e_h1)
        h.add_edge(e_h2)
        h.add_edge(e_h3)
        h.add_edge(e_h4)
        self.assertEqual(2, get_number_isomorphisms(g, h, True))

    def test_get_number_isomorphisms_unequal_number_vertices(self):
        g = Graph(False, 2)
        h = Graph(False, 3)
        self.assertEqual(0, get_number_isomorphisms(g, h, True))

    def test_get_number_automorphisms(self):
        # g: 1 - 2
        g = Graph(False)
        v_g1 = Vertex(g)
        v_g2 = Vertex(g)
        e_g = Edge(v_g1, v_g2)
        g.add_edge(e_g)
        self.assertEqual(2, get_number_automorphisms(g))
        # h: 1 - 2 - 3 - 4
        #            |
        #            5
        h = Graph(False)
        v_h1 = Vertex(h)
        v_h2 = Vertex(h)
        v_h3 = Vertex(h)
        v_h4 = Vertex(h)
        v_h5 = Vertex(h)
        e_h1 = Edge(v_h1, v_h2)
        e_h2 = Edge(v_h2, v_h3)
        e_h3 = Edge(v_h3, v_h4)
        e_h4 = Edge(v_h3, v_h5)
        # print(h)
        h.add_edge(e_h1)
        h.add_edge(e_h2)
        h.add_edge(e_h3)
        h.add_edge(e_h4)
        # print(h)
        self.assertEqual(2, get_number_automorphisms(h))

    # def test_is_isomorphic(self):
    #     TODO


if __name__ == '__main__':
    unittest.main()
