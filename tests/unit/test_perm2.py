import unittest
from basicpermutationgroup import *
from basicpermutationgroup import order_computation
from color_refinement_helper import compare
from graph import Graph
from coloring import Coloring
from permv2 import Permutation


class TestPermv2(unittest.TestCase):
    """
    Test for permv2.py (only for code we have written)
    """
    def test_coloring_to_permutation(self):
        g = Graph(directed=False, n=5, name='g')
        h = Graph(directed=False, n=5, name='h')
        vg_0, vg_1, vg_2, vg_3, vg_4 = g.vertices
        vh_0, vh_1, vh_2, vh_3, vh_4 = h.vertices

        coloring_p = Coloring()
        # p = Permutation(0, coloring=coloring_p, g=g)
        # self.assertEqual(0, len(p))

        coloring_p.add([vg_0, vh_0])
        coloring_p.add([vg_1, vh_1])
        p = Permutation(2, coloring=coloring_p, g=g)
        self.assertEqual(0, p.P[0])
        self.assertEqual(1, p.P[1])

        coloring_p = Coloring()
        coloring_p.add([vg_0, vh_1])
        coloring_p.add([vh_0, vg_1])
        p = Permutation(2, coloring=coloring_p, g=g)
        self.assertEqual(1, p.P[0])
        self.assertEqual(0, p.P[1])

        # TODO: deze test gaat nog mis...
        coloring_p = Coloring()
        coloring_p.add([vg_0, vh_1])
        coloring_p.add([vg_1, vh_2])
        coloring_p.add([vg_2, vh_3])
        coloring_p.add([vg_3, vh_4])
        coloring_p.add([vg_4, vh_0])
        p = Permutation(5, coloring=coloring_p, g=g)
        self.assertEqual(1, p.P[0])
        self.assertEqual(2, p.P[1])
        self.assertEqual(3, p.P[2])
        self.assertEqual(4, p.P[3])
        self.assertEqual(0, p.P[4])

if __name__ == '__main__':
    unittest.main()