import unittest
from color_refinement import get_weight, shift
from tests import *

class ChooseRootCase(unittest.TestCase):

    def test_get_weight(self):
        g = create_graph_helper([(0, 1), (1, 2), (2, 3), (2, 4)])
        arb_root = g.find_vertex(0)
        for v in g.vertices:
            v.weight = 0
        get_weight(arb_root, None)
        self.assertEqual(5, g.find_vertex(0).weight)
        self.assertEqual(4, g.find_vertex(1).weight)
        self.assertEqual(3, g.find_vertex(2).weight)
        self.assertEqual(1, g.find_vertex(3).weight)
        self.assertEqual(1, g.find_vertex(4).weight)
        for v in g.vertices:
            v.weight = 0
        arb_root = g.find_vertex(2)
        get_weight(arb_root, None)
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
        get_weight(arb_root, None)
        self.assertEqual(11, g.find_vertex(0).weight)
        root = shift(arb_root, g.order)
        self.assertEqual(g.find_vertex(5), root)


if __name__ == '__main__':
    unittest.main()