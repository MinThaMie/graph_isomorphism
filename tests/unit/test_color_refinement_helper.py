"""
Test file for Color Refinement Helper
"""

import unittest
from color_refinement_helper import *
from basicpermutationgroup import order_computation
from tests import *


class ColorRefineHelper(unittest.TestCase):
    """Tests for `color_refinement_helper.py`."""

    def test_compare(self):
        # Test empty lists are equivalent
        list1 = []
        list2 = []
        # Test lists with some numbers
        self.assertTrue(compare(list1, list2))
        list1.append(1)
        self.assertFalse(compare(list1, list2))
        list2.append(1)
        self.assertTrue(compare(list1, list2))
        list1.append(1)
        list2.append(1)
        self.assertTrue(compare(list1, list2))
        list1 = [1, 1, 2]
        list2 = [1, 2, 1]
        self.assertTrue(compare(list1, list2))
        list2 = [1, 2, 2]
        self.assertFalse(compare(list1, list2))

        # Compare using a key
        g = Graph(False)
        list1 = [Vertex(g, label=str(i)) for i in range(5)]
        list2 = [list1[i] for i in range(4, -1, -1)]
        self.assertTrue(compare(list1, list2, key=lambda v: v.label))

    def test_create_new_color_class(self):
        g = Graph(False)
        v1 = Vertex(g)
        v2 = Vertex(g)
        v3 = Vertex(g)
        coloring = Coloring()
        coloring.set(v1, 0)
        coloring.set(v2, 0)
        coloring.set(v3, 0)
        new_coloring = create_new_color_class(coloring, v1, v2)
        self.assertEqual(2, len(new_coloring))
        self.assertListEqual([v3], new_coloring.get(0))
        self.assertListEqual([v1, v2], new_coloring.get(1))

    def test_has_same_color_neighbours(self):
        # 1 - 2 - 3 - 4
        #         |
        #         5
        g = create_graph_helper([[1, 2], [2, 3], [3, 4], [3, 5]])
        v_g1, v_g2, v_g3, v_g4, v_g5 = g.vertices
        coloring = create_coloring_helper_vertex({0: [v_g1], 1: [v_g4, v_g5], 2: [v_g2], 3: [v_g3]})
        self.assertTrue(has_same_color_neighbours(v_g4, v_g5, coloring))
        self.assertFalse(has_same_color_neighbours(v_g1, v_g4, coloring))

    def test_choose_color(self):
        g = Graph(False, 12)
        vertices = g.vertices

        coloring = create_coloring_helper_vertex({0: vertices[:4]})
        self.assertListEqual(vertices[:4], choose_color(coloring))

        coloring = create_coloring_helper_vertex({0: vertices[:2],
                                                  1: vertices[3:7],
                                                  2: vertices[7:]})
        self.assertListEqual(vertices[3:7], choose_color(coloring))

        # Test that it does not choose color classes with an odd number of vertices
        coloring = create_coloring_helper_vertex({0: vertices[:2],
                                                  1: vertices[3:8]})
        self.assertListEqual([], choose_color(coloring))

    def test_choose_vertex(self):
        g = Graph(False, 2)
        v_g1, v_g2 = g.vertices
        h = Graph(False, 1)
        v_h1 = h.vertices[0]
        self.assertEqual(v_g1, choose_vertex([v_g1, v_g2, v_h1], g))
        self.assertEqual(v_h1, choose_vertex([v_g1, v_g2, v_h1], h))
        self.assertEqual(v_g1, choose_vertex([v_h1, v_g1, v_g2], g))
        self.assertIsNone(choose_vertex([v_g1, v_g2], h))
        self.assertIsNone(choose_vertex([], g))

    def test_get_vertices_of_graph(self):
        g = Graph(False, 2)
        v_g1, v_g2 = g.vertices
        h = Graph(False, 1)
        v_h1 = h.vertices[0]
        self.assertListEqual([v_g1, v_g2], get_vertices_of_graph([v_g1, v_g2, v_h1], g))
        self.assertListEqual([v_h1], get_vertices_of_graph([v_g1, v_g2, v_h1], h))
        self.assertListEqual([], get_vertices_of_graph([v_g1, v_g2], h))
        self.assertListEqual([], get_vertices_of_graph([], g))

    def test_are_twins(self):
        # 1 - 2
        #  \ /
        #   3
        g = create_graph_helper([[1, 2], [1, 3], [2, 3]])
        v_g1, v_g2, v_g3 = g.vertices
        self.assertTrue(are_twins(v_g1, v_g2))
        self.assertTrue(are_twins(v_g1, v_g3))
        self.assertTrue(are_twins(v_g2, v_g3))
        # 1 - 2
        #  \ /
        #   3 - 4
        g = create_graph_helper([[1, 2], [1, 3], [2, 3], [3, 4]])
        v_g1, v_g2, v_g3, v_g4 = g.vertices
        self.assertTrue(are_twins(v_g1, v_g2))
        self.assertFalse(are_twins(v_g3, v_g4))

    def test_get_twins(self):
        # 1 - 2
        #  \
        #   3
        g = create_graph_helper([[1, 2], [1, 3]])
        v_g1, v_g2, v_g3 = g.vertices
        twins, false_twins = get_twins(g)
        self.assertListEqual([], twins)
        self.assertListEqual([(v_g2, v_g3)], false_twins)
        # 1 - 2
        #  \ /
        #   3
        g.add_edge(Edge(v_g2, v_g3))
        twins, false_twins = get_twins(g)
        self.assertListEqual([(v_g1, v_g2), (v_g1, v_g3), (v_g2, v_g3)], twins)
        self.assertListEqual([], false_twins)
        # 1 - 2
        #  \ /
        #   3 - 4
        g = create_graph_helper([[1, 2], [1, 3], [2, 3], [3, 4]])
        v_g1, v_g2, v_g3, v_g4 = g.vertices
        twins, false_twins = get_twins(g)
        self.assertListEqual([(v_g1, v_g2)], twins)
        self.assertListEqual([], false_twins)

    def test_initialize_and_unit_coloring(self):
        # empty graph
        g = Graph(False)
        init_coloring = initialize_coloring(g)
        unit_coloring = get_unit_coloring(g)
        self.assertEqual(0, len(init_coloring))
        self.assertEqual(0, len(unit_coloring))

        # 1 - 2 - 3
        g = create_graph_helper([(1, 2), (2, 3)])
        v_g1, v_g2, v_g3 = g.vertices
        init_coloring = initialize_coloring(g)
        self.assertEqual(2, len(init_coloring))
        self.assertListEqual([v_g1, v_g3], init_coloring.get(1))
        self.assertListEqual([v_g2], init_coloring.get(2))
        unit_coloring = get_unit_coloring(g)
        self.assertEqual(1, len(unit_coloring))
        self.assertListEqual(g.vertices, unit_coloring.get(0))
        # 1 - 2 - 3
        #     |
        #     4 - 6 - 7
        #     |
        #     5
        g = create_graph_helper([(1, 2), (2, 3), (2, 4), (4, 5), (4, 6), (6, 7)])
        v_g1, v_g2, v_g3, v_g4, v_g5, v_g6, v_g7 = g.vertices
        init_coloring = initialize_coloring(g)
        self.assertEqual(3, len(init_coloring))
        self.assertListEqual([v_g1, v_g3, v_g5, v_g7], init_coloring.get(1))
        self.assertListEqual([v_g6], init_coloring.get(2))
        self.assertListEqual([v_g2, v_g4], init_coloring.get(3))
        unit_coloring = get_unit_coloring(g)
        self.assertEqual(1, len(unit_coloring))
        self.assertListEqual(g.vertices, unit_coloring.get(0))
        # 1 - 2 - 3
        #     |
        #     4 - 6 - 7
        #     |
        #     5       8
        v_g8 = Vertex(g)
        g.add_vertex(v_g8)
        init_coloring = initialize_coloring(g)
        self.assertEqual(4, len(init_coloring))
        self.assertListEqual([v_g8], init_coloring.get(0))
        self.assertListEqual([v_g1, v_g3, v_g5, v_g7], init_coloring.get(1))
        self.assertListEqual([v_g6], init_coloring.get(2))
        self.assertListEqual([v_g2, v_g4], init_coloring.get(3))
        unit_coloring = get_unit_coloring(g)
        self.assertEqual(1, len(unit_coloring))
        self.assertListEqual(g.vertices, unit_coloring.get(0))

    # TODO: test_generate_neighbour_count_with_color

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
        g = create_graph_helper([(0, 1), (1, 2), (4, 7), (3, 5), (3, 6), (5, 7), (6, 7), (5, 6)])
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

    def test_get_mappings(self):
        g = Graph(directed=False, n=5, name='g')
        h = Graph(directed=False, n=5, name='h')
        vg_0, vg_1, vg_2, vg_3, vg_4 = g.vertices
        vh_0, vh_1, vh_2, vh_3, vh_4 = h.vertices

        triv, non_triv = get_mappings(vg_0, h.vertices)
        self.assertEqual(vh_0, triv)
        self.assertEqual(4, len(non_triv))
        self.assertEqual([vh_1, vh_2, vh_3, vh_4], non_triv)

        triv, non_triv = get_mappings(vg_0, [vh_1, vh_2, vh_3, vh_4])
        self.assertIsNone(triv)
        self.assertEqual(4, len(non_triv))
        self.assertEqual([vh_1, vh_2, vh_3, vh_4], non_triv)

        triv, non_triv = get_mappings(vg_0, [vh_0])
        self.assertEqual(vh_0, triv)
        self.assertEqual(0, len(non_triv))

    def test_member_of(self):
        # trivial permuatiation
        H = Permutation(n=5)
        f = Permutation(n=2)
        f2 = Permutation(n=2, cycles=[[0, 1]])
        self.assertTrue(member_of(f, [H]))
        self.assertFalse(member_of(f2, [H]))

        H1 = Permutation(n=6, cycles=[[0, 1, 2], [4, 5]])
        H2 = Permutation(n=6, cycles=[[2, 3]])
        H = [H1, H2]
        f = Permutation(n=6, cycles=[[0, 2]])
        self.assertTrue(f, H)

    # I have commented it out because it makes permutations based on a single graph coloring: don't know if it still works
    # def test_coloring_to_permutation(self):
    #     g = Graph(directed=False, n=6, name='G')
    #     h = Graph(directed=False, n=6, name='H')
    #     vg_1, vg_2, vg_3, vg_4, vg_5, vg_6 = g.vertices
    #     vh_1, vh_2, vh_3, vh_4, vh_5, vh_6 = h.vertices
    #     coloring = Coloring()
    #
    #     # coloring.add([vg_1, vh_1])  #En willen we dit echt op 2 graven doen?
    #     coloring.add([vg_1])  # Is het niet netter om alle vertices te kleuren?
    #     perm = Permutation(len(g.vertices), coloring=coloring)
    #
    #     self.assertEqual(6, len(perm.P))
    #
    #     coloring.add([vg_2, vg_3])  # , vh_2, vh_3])
    #     perm = Permutation(len(g.vertices), coloring=coloring)
    #     # #perm = coloring_to_permutation(coloring, g)
    #     self.assertEqual(6, len(perm.P))
    #     self.assertEqual(vg_2.label, perm.P[vg_3.label])
    #     self.assertEqual(vg_3.label, perm.P[vg_2.label])
    #
    #     coloring.add([vg_4, vg_5, vg_6])  # vh_4, vg_5, vh_5, vg_6, vh_6])
    #     perm = Permutation(len(coloring.vertices), coloring=coloring)
    #     # #perm = coloring_to_permutation(coloring, g)
    #     self.assertEqual(6, len(perm.P))
    #     self.assertEqual(vg_5.label, perm.P[vg_4.label])
    #     self.assertEqual(vg_6.label, perm.P[vg_5.label])
    #     self.assertEqual(vg_4.label, perm.P[vg_6.label])

    # def test_compute_orbit(self):
    #     g = Graph(directed=False, n=6)
    #     vg_0, vg_1, vg_2, vg_3, vg_4, vg_5 = g.vertices
    #     coloring_p = Coloring()
    #     coloring_p.add([vg_0, vg_1, vg_2])
    #     coloring_p.add([vg_4, vg_5])
    #     p = Permutation(len(g.vertices), coloring=coloring_p)
    #
    #     coloring_q = Coloring()
    #     coloring_q.add([vg_2, vg_3])
    #     q = Permutation(len(g.vertices), coloring=coloring_q)
    #
    #     H = list()
    #     H.append(p)
    #     H.append(q)
    #     # test if (0,2) is in generating set (ex of slides)
    #     coloring_f = Coloring()
    #     coloring_f.add([vg_0, vg_2])
    #     f = Permutation(len(g.vertices), coloring=coloring_f)
    #
    #     self.assertTrue(member_of(f, H))
    #     # test if (0,4) is in generating set
    #     coloring_f = Coloring()
    #     coloring_f.add([vg_0, vg_4])
    #     f = Permutation(len(g.vertices), coloring=coloring_f)
    #     self.assertFalse(member_of(f, H))
    #
    #     # test if (0,1) is in generating set
    #     coloring_f = Coloring()
    #     coloring_f.add([vg_0, vg_1])
    #     f = Permutation(len(g.vertices), coloring=coloring_f)
    #     self.assertTrue(member_of(f, H))
    #
    #     # test if (0,5) is in generating set
    #     coloring_f = Coloring()
    #     coloring_f.add([vg_0, vg_5])
    #     f = Permutation(len(g.vertices), coloring=coloring_f)
    #     self.assertFalse(member_of(f, H))

    # TODO: to testclass of basicpermutationgroup
    def test_order_computation(self):  # TODO: to a testclass of basicpermutations
        g = Graph(directed=False, n=6)
        vg_0, vg_1, vg_2, vg_3, vg_4, vg_5 = g.vertices
        # mapping only to itself
        coloring_p = Coloring()
        coloring_p.add([vg_0])
        coloring_p.add([vg_1])
        p = Permutation(len(g.vertices), coloring=coloring_p)
        H = [p]
        self.assertEqual(1, order_computation(H))
        # mapping to itself and 1 other node
        coloring_p = Coloring()
        coloring_p.add([vg_0, vg_1])
        p = Permutation(len(g.vertices), coloring=coloring_p)
        H = [p]
        self.assertEqual(2, order_computation(H))
        # this is the permutation example of the lecture
        coloring_p = Coloring()
        coloring_p.add([vg_0, vg_1, vg_2])
        coloring_p.add([vg_4, vg_5])
        p = Permutation(len(g.vertices), coloring=coloring_p)
        coloring_q = Coloring()
        coloring_q.add([vg_2, vg_3])
        q = Permutation(len(g.vertices), coloring=coloring_q)
        H = [p, q]
        self.assertEqual(48, order_computation(H))

    # TODO: move to test class of basicpermuationgroup
    def test_permutation_coloring(self):
        g = Graph(directed=False, n=5)
        h = Graph(directed=False, n=5)
        vg_0, vg_1, vg_2, vg_3, vg_4 = g.vertices
        vh_0, vh_1, vh_2, vh_3, vh_4 = h.vertices

        coloring_p = Coloring()
        p = Permutation(0, coloring=coloring_p)
        self.assertEqual(0, len(p))

        coloring_p.add([vg_0, vh_0])
        coloring_p.add([vg_1, vh_1])
        p = Permutation(2, coloring=coloring_p)
        self.assertEqual(0, p.P[0])
        self.assertEqual(1, p.P[1])

        coloring_p = Coloring()
        coloring_p.add([vg_0, vh_1])
        coloring_p.add([vg_1, vh_0])
        p = Permutation(2, coloring=coloring_p)
        self.assertEqual(1, p.P[0])
        self.assertEqual(0, p.P[1])

        # TODO: deze test gaat nog mis...
        coloring_p = Coloring()
        coloring_p.add([vg_0, vh_1])
        coloring_p.add([vg_1, vh_2])
        coloring_p.add([vg_2, vh_3])
        coloring_p.add([vg_3, vh_4])
        coloring_p.add([vg_4, vh_0])
        p = Permutation(5, coloring=coloring_p)
        self.assertEqual(1, p.P[0])
        self.assertEqual(2, p.P[1])
        self.assertEqual(3, p.P[2])
        self.assertEqual(4, p.P[3])
        self.assertEqual(0, p.P[4])


if __name__ == '__main__':
    unittest.main()
