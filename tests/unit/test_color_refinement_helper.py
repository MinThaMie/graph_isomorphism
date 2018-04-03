import unittest

from color_refiment_helper import *


class TestCRHelper(unittest.TestCase):

    @classmethod
    def create_graph_helper(self, edges: List[List[int]]) -> Graph:
        """
        Create a graph from the given list of edges,
        each edge is represented by a list of 2 integers which represent the vertex labels.

        :param edges: Representation of the edges the graph should get
        :return: Graph
        """
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

    def test_group_by(self):
        # group_by(List[int]) groups by number
        a = [1, 2, 3, 2, 3]
        expected = {1: [1], 2: [2, 2], 3: [3, 3]}
        self.assertEqual(expected, group_by(a))

        # group_by(List[Vertex], key=Vertex.degree)
        # 0 -- 1 -- 2
        #                7 -- 4
        #              /  \
        #             6 - 5
        #             \   /
        #               3
        g = self.create_graph_helper([[0, 1], [1, 2], [4, 7], [3, 5], [3, 6], [5, 7], [6, 7], [5, 6]])
        vertices = sorted(g.vertices, key=lambda vertex: vertex.label)
        expected = {1: [vertices[0], vertices[2], vertices[4]],
                    2: [vertices[1], vertices[3]],
                    3: [vertices[5], vertices[6], vertices[7]]}
        actual = group_by(g.vertices, lambda v: v.degree)

        self.assertEqual(expected.keys(), actual.keys())
        for key in expected.keys():
            self.assertTrue(compare(expected[key], actual[key], lambda v: v.label))

        # group_by(dict{List}, key = lambda x: len(x)) groups by length of the lists
        degrees = {1: [vertices[0], vertices[2], vertices[4]],
                   2: [vertices[1], vertices[3]],
                   3: [vertices[5], vertices[6], vertices[7]]}
        expected = {2: [2], 3: [1, 3]}
        self.assertEqual(expected, group_by(degrees, lambda k: len(degrees[k])))

        # group by amount of neighbours with a given color
        # [x]: node with color/degree 1
        # [0] -- 1 -- [2]
        #                7 -- [4]
        #              /  \
        #             6 - 5
        #             \   /
        #               3
        degree_coloring = group_by(g.vertices, lambda v: v.degree)
        for c in degree_coloring:
            for v in degree_coloring[c]:
                v.colornum = c

        n_neighbors_of_color1 = group_by(vertices, lambda v: len([w for w in v.neighbours if w.colornum == 1]))
        expected = {0: [vertices[0], vertices[2], vertices[3], vertices[4], vertices[5], vertices[6]],
                    1: [vertices[7]],
                    2: [vertices[1]]}

        self.assertEqual(expected.keys(), n_neighbors_of_color1.keys())
        for key in expected.keys():
            self.assertEqual(len(expected[key]), len(n_neighbors_of_color1[key]),
                             "Expect key " + str(key) + ' to have ' + str(len(expected[key])) + ' vertices')
            self.assertTrue(compare(expected[key], n_neighbors_of_color1[key], lambda v: v.label))

    def test_coloring_to_permutation(self):
        g = Graph(directed=False, n=6, name='G')
        h = Graph(directed=False, n=6, name='H')
        vg_1, vg_2, vg_3, vg_4, vg_5, vg_6 = g.vertices
        vh_1, vh_2, vh_3, vh_4, vh_5, vh_6 = h.vertices
        coloring = Coloring()
        coloring.add([vg_1, vh_1])
        perm = coloring_to_permutation(coloring, g)
        self.assertEqual(6, len(perm.P))
        coloring.add([vg_2, vg_3, vh_2, vh_3])
        perm = coloring_to_permutation(coloring, g)
        self.assertEqual(6, len(perm.P))
        self.assertEqual(vg_2.label, perm.P[vg_3.label])
        self.assertEqual(vg_3.label, perm.P[vg_2.label])
        coloring.add([vg_4, vh_4, vg_5, vh_5, vg_6, vh_6])
        perm = coloring_to_permutation(coloring, g)
        self.assertEqual(6, len(perm.P))
        self.assertEqual(vg_5.label, perm.P[vg_4.label])
        self.assertEqual(vg_6.label, perm.P[vg_5.label])
        self.assertEqual(vg_4.label, perm.P[vg_6.label])

    def test_Orbit(self):
        g = Graph(directed=False, n=6)
        vg_0, vg_1, vg_2, vg_3, vg_4, vg_5 = g.vertices
        coloring_p = Coloring()
        coloring_p.add([vg_0, vg_1, vg_2])
        coloring_p.add([vg_4, vg_5])
        p = coloring_to_permutation(coloring_p, g)
        coloring_q = Coloring()
        coloring_q.add([vg_2, vg_3])
        q = coloring_to_permutation(coloring_q, g)
        H = list()
        H.append(p)
        H.append(q)
        # test if (0,2) is in generating set (ex of slides)
        coloring_f = Coloring()
        coloring_f.add([vg_0, vg_2])
        f = coloring_to_permutation(coloring_f, g)
        self.assertTrue(member_of(f, H))
        # test if (0,4) is in generating set
        coloring_f = Coloring()
        coloring_f.add([vg_0, vg_4])
        f = coloring_to_permutation(coloring_f, g)
        self.assertFalse(member_of(f, H))
        # test if (0,1) is in generating set
        coloring_f = Coloring()
        coloring_f.add([vg_0, vg_1])
        f = coloring_to_permutation(coloring_f, g)
        self.assertTrue(member_of(f, H))
        # test if (0,5) is in generating set
        coloring_f = Coloring()
        coloring_f.add([vg_0, vg_5])
        f = coloring_to_permutation(coloring_f, g)
        self.assertFalse(member_of(f, H))

        
if __name__ == '__main__':
    unittest.main()
