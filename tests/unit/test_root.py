import unittest
from color_refinement import set_weight, shift, choose_a_root, assign_levels
from tests import *

class ChooseRootCase(unittest.TestCase):

    def test_get_weight(self):
        g = create_graph_helper([(0, 1), (1, 2), (2, 3), (2, 4)])
        arb_root = g.find_vertex(0)
        for v in g.vertices:
            v.weight = 0
        set_weight(arb_root)
        self.assertEqual(5, g.find_vertex(0).weight)
        self.assertEqual(4, g.find_vertex(1).weight)
        self.assertEqual(3, g.find_vertex(2).weight)
        self.assertEqual(1, g.find_vertex(3).weight)
        self.assertEqual(1, g.find_vertex(4).weight)
        for v in g.vertices:
            v.weight = 0
        arb_root = g.find_vertex(2)
        set_weight(arb_root)
        self.assertEqual(5, g.find_vertex(2).weight)
        self.assertEqual(2, g.find_vertex(1).weight)
        self.assertEqual(1, g.find_vertex(0).weight)
        self.assertEqual(1, g.find_vertex(3).weight)
        self.assertEqual(1, g.find_vertex(4).weight)

    def test_shift(self):
        g = create_graph_helper([(0, 1), (0, 2), (2, 3), (0, 4), (4, 5),  (5, 6),  (6, 7),  (7, 8),  (8, 9), (8, 10)])
        arb_root = g.find_vertex(0)
        for v in g.vertices:
            v.weight = 0
        set_weight(arb_root)
        self.assertEqual(11, g.find_vertex(0).weight)
        root = shift(arb_root, g.order)
        self.assertEqual(g.find_vertex(5), root)

    def test_get_root(self):
        g = create_graph_helper([(0, 1), (0, 2), (2, 3), (0, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (8, 10)])
        for v in g.vertices:
            v.weight = 0
        root = choose_a_root(g)
        self.assertEqual(g.find_vertex(5), root)

    def test_levels(self):
        g = create_graph_helper([(0, 1), (0, 2), (0, 3), (1, 4), (1, 5), (2, 6), (6, 8), (3, 7)])
        for v in g.vertices:
            v.weight = 0
            v.level = None
        root = choose_a_root(g)
        self.assertEqual(g.find_vertex(0), root)
        assign_levels(root)
        self.assertEqual(0, g.find_vertex(0).level)
        self.assertEqual(1, g.find_vertex(1).level)
        self.assertEqual(1, g.find_vertex(2).level)
        self.assertEqual(1, g.find_vertex(3).level)
        self.assertEqual(2, g.find_vertex(4).level)
        self.assertEqual(2, g.find_vertex(5).level)
        self.assertEqual(2, g.find_vertex(6).level)
        self.assertEqual(2, g.find_vertex(7).level)
        self.assertEqual(3, g.find_vertex(8).level)




if __name__ == '__main__':
    unittest.main()