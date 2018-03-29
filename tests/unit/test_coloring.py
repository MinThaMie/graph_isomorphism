"""
Test file for Coloring class
"""
import unittest
from coloring import *
from graph_io import load_graph


class ColoringCase(unittest.TestCase):
    coloring = None
    graph = None
    v1 = None
    v2 = None

    def create_coloring_helper(self, vertices: List[int], map: dict):
        coloring = Coloring()
        for key in map:
            for value in map[key]:
                vertex = [v for v in vertices if v.label == value][0]
                coloring.set(key, vertex)
        return coloring

    def create_graph_helper(self, edges: List[List[int]]):
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

    def setUp(self):
        self.coloring = Coloring()
        self.graph = Graph(False, 5)
        self.v1, self.v2 = Vertex(self.graph), Vertex(self.graph)

    def test_init(self):
        # Has no colors
        self.assertEqual(0, len(self.coloring))

    def test_set(self):
        # Adds a new color if not existing
        self.coloring.set(4, self.v1)
        self.assertEqual(1, len(self.coloring))
        self.assertEqual(4, list(self.coloring.colors)[0])
        self.assertEqual(4, self.v1.colornum)

        # Adds no new color if already existing
        self.coloring.set(4, self.v2)
        self.assertEqual(1, len(self.coloring))
        self.assertEqual(4, self.v2.colornum)

    def test_get(self):
        self.coloring.set(4, self.v1)
        self.coloring.set(4, self.v2)
        vertices = self.coloring.get(4)
        self.assertEqual(2, len(vertices))
        self.assertEqual(True, self.v1 in vertices)
        self.assertEqual(True, self.v2 in vertices)

    def test_add(self):
        # Adds new vertices
        self.coloring.add([self.v1,self.v2], 4)
        vertices = self.coloring.get(4)
        self.assertEqual(2, len(vertices))
        self.assertEqual(True, self.v1 in vertices)
        self.assertEqual(True, self.v2 in vertices)

        # Recolors old vertices when old color is given
        v3 = Vertex(self.graph)
        self.coloring.set(4, v3)
        self.coloring.add([self.v1, self.v2], 0, 4)
        vertices = self.coloring.get(0)
        self.assertEqual(2, len(vertices))
        self.assertEqual(True, self.v1 in vertices)
        self.assertEqual(True, self.v2 in vertices)
        self.assertEqual(False, v3 in vertices)
        self.assertEqual(1, len(self.coloring.get(4)))

    def test_color(self):
        self.coloring.set(3, self.v1)
        self.coloring.set(4, self.v2)
        self.assertEqual(3, self.coloring.color(self.v1))
        self.assertEqual(4, self.coloring.color(self.v2))

    def test_recolor(self):
        self.coloring.set(1, self.v1)
        self.assertEqual(1, self.coloring.color(self.v1))
        self.assertEqual(1, self.v1.colornum)

        self.coloring.recolor(self.v1, 2)
        self.assertEqual(2, len(self.coloring))
        self.assertEqual(False, self.v1 in self.coloring.get(1))
        self.assertEqual(True, self.v1 in self.coloring.get(2))

        # Cannot recolor vertex that is not in the coloring
        with self.assertRaises(KeyError) as e:
            self.coloring.recolor(self.v2, 2)

        self.assertEqual("\'Vertex " + str(self.v2) + " not found in coloring\'", str(e.exception))

    def test_colors(self):
        self.coloring.set(0, self.v1)
        self.coloring.set(1, self.v2)
        self.coloring.set(2, Vertex(self.graph))

        self.assertEqual(3, len(self.coloring))
        self.assertIn(0, self.coloring.colors)
        self.assertIn(1, self.coloring.colors)
        self.assertIn(2, self.coloring.colors)

    def test_next_color(self):
        for i in range(10):
            self.assertEqual(i, len(self.coloring))
            self.assertEqual(i, self.coloring.next_color())
            self.coloring.set(i, Vertex(self.graph))

    def test_items(self):
        self.coloring.set(0, self.v1)
        self.coloring.set(1, self.v2)
        self.coloring.set(2, Vertex(self.graph))

        for c, v in self.coloring.items():
            self.assertIn(c, self.coloring.colors)
            self.assertEqual(self.coloring.get(c),list(v))

    def test_status(self):
        # For different graphs
        G0 = self.create_graph_helper(edges=[[0, 1], [1, 2], [2, 3], [3, 4], [2, 4], [4, 5], [5, 6]])
        G1 = self.create_graph_helper(edges = [[10,12],[12,13],[12,14],[13,14],[11,14],[11,15],[15,16]])
        G2 = self.create_graph_helper(edges=[[21, 23], [23, 25], [20, 25], [20, 24], [24, 25], [20, 26], [22, 26]])
        G3 = self.create_graph_helper(edges = [[30,32],[32,34],[34,35],[35,36],[31,35],[31,36],[31,33]])

        coloring13 = self.create_coloring_helper(G1.vertices + G3.vertices,
                {0:[10,33], 1:[16,30],2:[11,34], 3:[13,36], 4:[15,32], 5:[12,31],6:[14,35]})
        coloring02 = self.create_coloring_helper(G0.vertices + G2.vertices,
                {0: [0,6,21,22], 1:[1,5,23,26], 2:[3,24], 3:[2,4,20,25]})
        coloring01 = self.create_coloring_helper(G0.vertices + G1.vertices,
                {0: [0,6], 1: [1,5], 2:[2,4], 3:[3],4:[10],5:[11],6:[12],7:[13],8:[14],9:[15],10:[16]})
        coloring = self.create_coloring_helper(G0.vertices+G1.vertices, {0:[0,1], 1:[10,11]})

        self.assertEqual("Bijection", coloring13.status(G1,G3))
        self.assertEqual(None, coloring02.status(G1, G3))
        self.assertEqual("Unbalanced", coloring01.status(G1, G3))
        self.assertEqual("Unbalanced", coloring.status(G1, G3))

        # Automorphism
        G0copy = G0.deepcopy()
        coloring0 = self.create_coloring_helper(G0.vertices, {0: [0,6], 1: [1,5], 2:[2,4], 3:[3]})
        coloring0.set(0, G0copy.vertices[0])
        coloring0.set(0, G0copy.vertices[6])
        coloring0.set(1, G0copy.vertices[1])
        coloring0.set(1, G0copy.vertices[5])
        coloring0.set(2, G0copy.vertices[2])
        coloring0.set(2, G0copy.vertices[4])
        coloring0.set(3, G0copy.vertices[3])
        self.assertEqual(None, coloring0.status(G0,G0copy))

        # TODO add more?

    def test_copy(self):
        g = Graph(False, n= 10)
        self.coloring.add(g.vertices[0:2])
        self.coloring.add(g.vertices[2:3])
        self.coloring.add(g.vertices[3:7])
        self.coloring.add(g.vertices[7:])

        copy = self.coloring.copy()
        for c,v in self.coloring.items():
            self.assertEqual(list(v), list(copy.get(c)))

        # Test that changing the copy does not change to old coloring
        # But that it does change the colornum of those vertices
        v0 = g.vertices[0]
        copy.recolor(v0,2,0) #recolor v0
        self.assertEqual(2, v0.colornum)
        self.assertEqual(2, copy.color(v0))
        self.assertEqual(0, self.coloring.color(v0)) #not recolored in old coloring

    def test_reset(self):
        g = Graph(False, n=10)
        for idx, v in enumerate(g.vertices):
            v.colornum = idx

        self.coloring.reset(g.vertices)
        for i in range(10):
            self.assertEqual(i, self.coloring.color(g.vertices[i]))


if __name__ == '__main__':
    unittest.main()