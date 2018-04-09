import unittest
from color_refinement import get_number_automorphisms
from graph import Graph, Edge


class TestCountAutomorphismsSmall(unittest.TestCase):

    def small_graph(self):
        # 0 - 1
        g = Graph(directed=False, n=2)
        vg_0, vg_1 = g.vertices
        g.add_edge(Edge(vg_0, vg_1))
        self.assertEqual(2, get_number_automorphisms(g))
        # 0 - 1 - 2
        g = Graph(directed=False, n=3)
        vg_0, vg_1, vg_2 = g.vertices
        g.add_edge(Edge(vg_0, vg_1))
        g.add_edge(Edge(vg_1, vg_2))
        self.assertEqual(2, get_number_automorphisms(g))

    def test_example(self):
        # 1       4
        # | \   / |
        # 3 - 0 - 6
        # | /   \ |
        # 2       5
        g = Graph(directed=False, n=7)
        vg_0, vg_1, vg_2, vg_3, vg_4, vg_5, vg_6 = g.vertices
        g.add_edge(Edge(vg_0, vg_1))
        g.add_edge(Edge(vg_0, vg_2))
        g.add_edge(Edge(vg_0, vg_3))
        g.add_edge(Edge(vg_0, vg_4))
        g.add_edge(Edge(vg_0, vg_5))
        g.add_edge(Edge(vg_0, vg_6))
        g.add_edge(Edge(vg_3, vg_1))
        g.add_edge(Edge(vg_3, vg_2))
        g.add_edge(Edge(vg_6, vg_4))
        g.add_edge(Edge(vg_6, vg_5))
        self.assertEqual(8, get_number_automorphisms(g))

    def test2(self):
        # 1       4
        #   \   /
        # 3 - 0 - 6
        #   /   \
        # 2       5
        g = Graph(directed=False, n=7)
        vg_0, vg_1, vg_2, vg_3, vg_4, vg_5, vg_6 = g.vertices
        g.add_edge(Edge(vg_0, vg_1))
        g.add_edge(Edge(vg_0, vg_2))
        g.add_edge(Edge(vg_0, vg_3))
        g.add_edge(Edge(vg_0, vg_4))
        g.add_edge(Edge(vg_0, vg_5))
        g.add_edge(Edge(vg_0, vg_6))
        self.assertEqual(720, get_number_automorphisms(g))


if __name__ == '__main__':
    unittest.main()