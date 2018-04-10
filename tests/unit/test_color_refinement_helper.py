"""
Test file for Color Refinement Helper
"""

import unittest

import tests
import tools
from color_refinement_helper import *
from graph import *


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
        self.assertListEqual([v3], list(new_coloring.get(0)))
        self.assertListEqual([v1, v2], list(new_coloring.get(1)))

    def test_has_same_color_neighbours(self):
        # 1 - 2 - 3 - 4
        #         |
        #         5
        g = tools.create_graph_helper([[1, 2], [2, 3], [3, 4], [3, 5]])
        v_g1, v_g2, v_g3, v_g4, v_g5 = g.vertices
        coloring = tests.create_coloring_helper_vertex({0: [v_g1], 1: [v_g4, v_g5], 2: [v_g2], 3: [v_g3]})
        self.assertTrue(has_same_color_neighbours(v_g4, v_g5, coloring))
        self.assertFalse(has_same_color_neighbours(v_g1, v_g4, coloring))

    def test_choose_color(self):
        g = Graph(False, 12)
        vertices = g.vertices

        coloring = tests.create_coloring_helper_vertex({0: vertices[:4]})
        self.assertListEqual(vertices[:4], list(choose_color(coloring)))

        coloring = tests.create_coloring_helper_vertex({0: vertices[:2],
                                                        1: vertices[3:7],
                                                        2: vertices[7:]})
        self.assertListEqual(vertices[3:7], list(choose_color(coloring)))

        # Test that it does not choose color classes with an odd number of vertices
        coloring = tests.create_coloring_helper_vertex({0: vertices[:2],
                                                        1: vertices[3:8]})
        self.assertListEqual([], list(choose_color(coloring)))

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

    def test_initialize_and_unit_coloring(self):
        # empty graph
        g = Graph(False)
        init_coloring = initialize_coloring(g)
        self.assertEqual(0, len(init_coloring))

        # 1 - 2 - 3
        g = tools.create_graph_helper([(1, 2), (2, 3)])
        v_g1, v_g2, v_g3 = g.vertices
        init_coloring = initialize_coloring(g)
        self.assertEqual(2, len(init_coloring))
        self.assertListEqual([v_g1, v_g3], list(init_coloring.get(1)))
        self.assertListEqual([v_g2], list(init_coloring.get(2)))

        # 1 - 2 - 3
        #     |
        #     4 - 6 - 7
        #     |
        #     5
        g = tools.create_graph_helper([(1, 2), (2, 3), (2, 4), (4, 5), (4, 6), (6, 7)])
        v_g1, v_g2, v_g3, v_g4, v_g5, v_g6, v_g7 = g.vertices
        init_coloring = initialize_coloring(g)
        self.assertEqual(3, len(init_coloring))
        self.assertListEqual([v_g1, v_g3, v_g5, v_g7], list(init_coloring.get(1)))
        self.assertListEqual([v_g6], list(init_coloring.get(2)))
        self.assertListEqual([v_g2, v_g4], list(init_coloring.get(3)))

        # 1 - 2 - 3
        #     |
        #     4 - 6 - 7
        #     |
        #     5       8
        v_g8 = Vertex(g)
        g.add_vertex(v_g8)
        init_coloring = initialize_coloring(g)
        self.assertEqual(4, len(init_coloring))
        self.assertListEqual([v_g8], list(init_coloring.get(0)))
        self.assertListEqual([v_g1, v_g3, v_g5, v_g7], list(init_coloring.get(1)))
        self.assertListEqual([v_g6], list(init_coloring.get(2)))
        self.assertListEqual([v_g2, v_g4], list(init_coloring.get(3)))

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
        g = tools.create_graph_helper([(0, 1), (1, 2), (4, 7), (3, 5), (3, 6), (5, 7), (6, 7), (5, 6)])
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

    def setUp(self):
        tests.set_up_test_graphs()

    def test_graph_to_modules(self):
        #
        modules = graph_to_modules(tests.non_trivial_graph)
        expected_labels = [{0}, {1}, {2, 4}, {3}]
        self.assertCountEqual(expected_labels, [{vertex.label for vertex in module} for module in modules])

        #
        modules = graph_to_modules(tests.modular_decomposition_graph)
        expected_labels = [{5, 6}, {0, 1, 4}, {2, 3}]
        self.assertCountEqual(expected_labels, [{vertex.label for vertex in module} for module in modules])

        #
        modules = graph_to_modules(tests.butterfly)
        expected_labels = [{1, 4}, {0}, {2, 3}]
        self.assertCountEqual(expected_labels, [{vertex.label for vertex in module} for module in modules])

        # Assert that redoing modular decomposition results in another simplification of the graph
        butterfly_modular_decomposition_graph, _ = modules_to_graph(modules)
        modules = graph_to_modules(butterfly_modular_decomposition_graph)
        expected_labels = [{"0"}, {"2+3", "1+4"}]
        self.assertCountEqual(expected_labels, [{vertex.label for vertex in module} for module in modules])

    def test_modules_to_graph(self):
        tests.set_up_test_graphs()

        modules = graph_to_modules(tests.non_trivial_graph)
        graph, _ = modules_to_graph(modules)
        labels = [vertex.label for vertex in graph.vertices]
        expected_labels = ["0", "1", "2+4", "3"]
        self.assertTrue(set(labels) == set(expected_labels))

        modules = graph_to_modules(tests.modular_decomposition_graph)
        graph, _ = modules_to_graph(modules)
        labels = [vertex.label for vertex in graph.vertices]
        expected_labels = ["0+1+4", "2+3", "5+6"]
        self.assertTrue(set(labels) == set(expected_labels))

        modules = graph_to_modules(tests.butterfly)
        graph, _ = modules_to_graph(modules)
        labels = [vertex.label for vertex in graph.vertices]
        expected_labels = ["0", "1+4", "2+3"]
        self.assertTrue(set(labels) == set(expected_labels))

        modules2 = graph_to_modules(graph)
        graph2, _ = modules_to_graph(modules2)
        labels = [vertex.label for vertex in graph2.vertices]
        expected_labels = ["0", "1+4+2+3"]
        self.assertTrue(set(labels) == set(expected_labels))

        modules3 = graph_to_modules(graph2)
        graph3, _ = modules_to_graph(modules3)
        labels = [vertex.label for vertex in graph3.vertices]
        expected_labels = ["0+1+4+2+3"]
        self.assertTrue(set(labels) == set(expected_labels))

        modules4 = graph_to_modules(graph3)
        graph4, _ = modules_to_graph(modules4)
        labels = [vertex.label for vertex in graph4.vertices]
        expected_labels = ["0+1+4+2+3"]
        self.assertTrue(set(labels) == set(expected_labels))

        g = tools.create_graph_helper([[1, 2], [1, 3], [2, 3]])
        modules_triangle = graph_to_modules(g)
        graph, _ = modules_to_graph(modules_triangle)
        labels = [vertex.label for vertex in graph.vertices]
        expected_labels = ["1+2+3"]
        self.assertTrue(set(labels) == set(expected_labels))

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

    def test_choose_color_trivial(self):
        g = create_graph_helper([(1, 2), (2, 3)])
        v_g1, v_g2, v_g3 = g.vertices
        g_copy = g.deepcopy()
        v_1, v_2, v_3 = g_copy.vertices
        added = g + g_copy
        coloring = initialize_coloring(added)
        chosen, color_class = choose_color_trivial(coloring, g)
        self.assertEqual([v_g1, v_g3, v_1, v_3], color_class)
        self.assertEqual(v_g1, chosen)


if __name__ == '__main__':
    unittest.main()
