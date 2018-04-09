"""
Test file for Coloring class
"""
import unittest

from tests import *
from tools import create_graph_helper


class ColoringCase(unittest.TestCase):
    coloring = None
    graph = None
    v1 = None
    v2 = None

    def setUp(self):
        self.coloring = Coloring()
        self.graph = Graph(False, 5)
        self.v1, self.v2 = Vertex(self.graph), Vertex(self.graph)

    def test_init(self):
        # Has no colors or vertices
        self.assertEqual(0, len(self.coloring))
        self.assertEqual(0, len(self.coloring.vertices))

    def test_set(self):
        # Adds a new color if not existing
        self.coloring.set(self.v1, 4)
        self.assertEqual(1, len(self.coloring))
        self.assertEqual(4, list(self.coloring.colors)[0])

        # Adds no new color if already existing
        self.coloring.set(self.v2, 4)
        self.assertEqual(1, len(self.coloring))

        # Cannot set a vertex that is already in the coloring (have to recolor it)
        with self.assertRaises(KeyError) as e:
            self.coloring.set(self.v1, 0)
        self.assertEqual('\'Vertex {} already in coloring, color: 4. Use recolor instead\''.format(str(self.v1)),
                         str(e.exception))

    def test_get(self):
        self.coloring.set(self.v1, 4)
        self.coloring.set(self.v2, 4)
        vertices = self.coloring.get(4)
        self.assertEqual(2, len(vertices))
        self.assertTrue(self.v1 in vertices)
        self.assertTrue(self.v2 in vertices)

    def test_add(self):
        # Adds new vertices
        self.coloring.add([self.v1, self.v2], 4)
        vertices = self.coloring.get(4)
        self.assertEqual(2, len(vertices))
        self.assertTrue(self.v1 in vertices)
        self.assertTrue(self.v2 in vertices)

        # Recolors old vertices
        v3, v4 = Vertex(self.graph), Vertex(self.graph)
        self.coloring.set(v3, 4)
        self.coloring.add([self.v1, self.v2, v4], 0)
        vertices = self.coloring.get(0)
        self.assertEqual(3, len(vertices))
        self.assertTrue(self.v1 in vertices)
        self.assertTrue(self.v2 in vertices)
        self.assertTrue(v4 in vertices)
        self.assertFalse(v3 in vertices)
        self.assertEqual(1, len(self.coloring.get(4)))

    def test_color(self):
        self.coloring.set(self.v1, 3)
        self.coloring.set(self.v2, 4)
        self.assertEqual(3, self.coloring.color(self.v1))
        self.assertEqual(4, self.coloring.color(self.v2))

    def test_recolor(self):
        self.coloring.set(self.v1, 1)
        self.assertEqual(1, self.coloring.color(self.v1))

        self.coloring.recolor(self.v1, 2)
        self.assertEqual(2, len(self.coloring))
        self.assertFalse(self.v1 in self.coloring.get(1))
        self.assertTrue(self.v1 in self.coloring.get(2))

        # Cannot recolor vertex that is not in the coloring
        with self.assertRaises(KeyError) as e:
            self.coloring.recolor(self.v2, 2)

        self.assertEqual("\'Vertex {} not found in coloring, use set() instead\'".format(str(self.v2)),
                         str(e.exception))

    def test_colors(self):
        self.coloring.set(self.v1, 0)
        self.coloring.set(self.v2, 1)
        self.coloring.set(Vertex(self.graph), 2)

        self.assertEqual(3, len(self.coloring))
        self.assertIn(0, self.coloring.colors)
        self.assertIn(1, self.coloring.colors)
        self.assertIn(2, self.coloring.colors)

    def test_vertices(self):
        v3 = Vertex(self.graph)
        self.coloring.set(self.v1, 0)
        self.coloring.set(self.v2, 1)
        self.coloring.set(v3, 1)

        self.assertEqual(3, len(self.coloring.vertices))
        self.assertIn(self.v1, self.coloring.vertices)
        self.assertIn(self.v2, self.coloring.vertices)
        self.assertIn(v3, self.coloring.vertices)

    def test_next_color(self):
        for i in range(10):
            self.assertEqual(i, len(self.coloring))
            self.assertEqual(i, self.coloring.next_color())
            self.coloring.set(Vertex(self.graph), i)

    def test_items(self):
        self.coloring.set(self.v1, 0)
        self.coloring.set(self.v2, 1)
        self.coloring.set(Vertex(self.graph), 2)

        for c, v in self.coloring.items():
            self.assertIn(c, self.coloring.colors)
            self.assertEqual(self.coloring.get(c), list(v))

    def test_status(self):
        # For different graphs
        # G0: 0 -- 1 -- 2 -- 3
        #                \  /
        #                 4 -- 5 -- 6
        #
        # G1: 10 -- 12 -- 13
        #            |   /
        #             14 -- 11 -- 15 -- 16
        #
        # G2: 21 -- 23 -- 25 -- 20 -- 26 -- 22
        #                   \  /
        #                    24
        #
        # G3: 30 -- 32 -- 34 -- 35 -- 36
        #                         \  /
        #                          31 -- 33
        G0 = create_graph_helper(edges=[[0, 1], [1, 2], [2, 3], [3, 4], [2, 4], [4, 5], [5, 6]])
        G1 = create_graph_helper(edges=[[10, 12], [12, 13], [12, 14], [13, 14], [11, 14], [11, 15], [15, 16]])
        G2 = create_graph_helper(edges=[[21, 23], [23, 25], [20, 25], [20, 24], [24, 25], [20, 26], [22, 26]])
        G3 = create_graph_helper(edges=[[30, 32], [32, 34], [34, 35], [35, 36], [31, 35], [31, 36], [31, 33]])

        coloring13 = create_coloring_helper(G1.vertices + G3.vertices,
                                            {0: [10, 33], 1: [16, 30], 2: [11, 34], 3: [13, 36], 4: [15, 32],
                                             5: [12, 31], 6: [14, 35]})
        coloring02 = create_coloring_helper(G0.vertices + G2.vertices,
                                            {0: [0, 6, 21, 22], 1: [1, 5, 23, 26], 2: [3, 24], 3: [2, 4, 20, 25]})
        coloring01 = create_coloring_helper(G0.vertices + G1.vertices,
                                            {0: [0, 6], 1: [1, 5], 2: [2, 4], 3: [3], 4: [10], 5: [11], 6: [12],
                                             7: [13], 8: [14], 9: [15], 10: [16]})
        unbalanced_coloring = create_coloring_helper(G0.vertices + G1.vertices, {0: [0, 1], 1: [10, 11]})

        self.assertEqual("Bijection", coloring13.status(G1, G3))
        self.assertEqual(None, coloring02.status(G1, G3))
        self.assertEqual("Unbalanced", coloring01.status(G1, G3))
        self.assertEqual("Unbalanced", unbalanced_coloring.status(G0, G1))

        # Automorphism
        G0copy = G0.deepcopy()
        coloring0 = create_coloring_helper(G0.vertices, {0: [0, 6], 1: [1, 5], 2: [2, 4], 3: [3]})
        coloring0.add([G0copy.vertices[0], G0copy.vertices[6]], 0)
        coloring0.add([G0copy.vertices[1], G0copy.vertices[5]], 1)
        coloring0.add([G0copy.vertices[2], G0copy.vertices[4]], 2)
        coloring0.set(G0copy.vertices[3], 3)
        self.assertEqual(None, coloring0.status(G0, G0copy))

    def test_copy(self):
        g = Graph(False, n=10)
        self.coloring.add(g.vertices[0:2])
        self.coloring.add(g.vertices[2:3])
        self.coloring.add(g.vertices[3:7])
        self.coloring.add(g.vertices[7:])

        copy = self.coloring.copy()
        for c, v in self.coloring.items():
            self.assertEqual(list(v), list(copy.get(c)))

        # Test that changing the copy does not change to old coloring
        v0 = g.vertices[0]
        copy.recolor(v0, 2)  # recolor v0
        self.assertEqual(2, copy.color(v0))
        self.assertEqual(0, self.coloring.color(v0))  # not recolored in old coloring
        self.assertFalse(v0 in self.coloring.get(2))
        self.assertEqual(0, self.coloring.color(v0))


if __name__ == '__main__':
    unittest.main()
