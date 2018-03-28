"""
Test file for Color Refinement Helper
"""

import unittest
from color_refiment_helper import *


def create_graph_helper(edges: List[List[int]]) -> Graph:
    """
    Creates a Graph with edges over each pair of vertex numbers
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


def create_coloring_helper_vertex(mapping: dict) -> Coloring:
    """
    Converts a dictionary to Coloring
    """
    coloring = Coloring()
    for key in mapping:
        for vertex in mapping[key]:
            coloring.set(key, vertex)
    return coloring


def create_coloring_helper(graph: Graph, mapping: dict) -> Coloring:
    """
    Converts a dictionary with numbers of the vertices to a Coloring
    """
    coloring = Coloring()
    for key in mapping:
        for value in mapping[key]:
            vertex = graph.find_vertex(value)
            coloring.set(key, vertex)
    return coloring


class ColorRefineHelper(unittest.TestCase):
    """Tests for `color_refinement_helper.py`."""

    def test_compare(self):
        list1 = []
        list2 = []
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

    def test_create_new_color_class(self):
        g = Graph(False)
        v1 = Vertex(g)
        v2 = Vertex(g)
        v3 = Vertex(g)
        coloring = Coloring()
        coloring.set(0, v1)
        coloring.set(0, v2)
        coloring.set(0, v3)
        new_coloring = create_new_color_class(coloring, v1, v2)
        self.assertEqual(2, new_coloring.num_colors)
        self.assertListEqual([v3],     new_coloring.get(0))
        self.assertListEqual([v1, v2], new_coloring.get(1))

    def test_has_same_color_neighbours(self):
        # 1 - 2 - 3 - 4
        #         |
        #         5
        g = create_graph_helper([[1, 2], [2, 3], [3, 4], [3, 5]])
        v_g1, v_g2, v_g3, v_g4, v_g5 = g.vertices
        coloring = create_coloring_helper_vertex({0: [v_g1], 1: [v_g4, v_g5], 2: [v_g2], 3: [v_g3]})
        self.assertTrue(has_same_color_neighbours(v_g4, v_g5,  coloring))
        self.assertFalse(has_same_color_neighbours(v_g1, v_g4, coloring))

    def test_choose_color(self):
        g = Graph(False, 8)
        vertices = sorted(g.vertices, key=Vertex.__str__)
        v_g1, v_g2, v_g3, v_g4, v_g5, v_g6, v_g7, v_g8 = g.vertices
        coloring = create_coloring_helper_vertex({0: [v_g1, v_g2, v_g3, v_g4]})
        self.assertListEqual(vertices[:4], choose_color(coloring))

        coloring = create_coloring_helper_vertex({0: [v_g1, v_g2],
                                                  1: [v_g1, v_g2, v_g3, v_g4],
                                                  2: [v_g1, v_g2, v_g3, v_g4, v_g5, v_g6]})
        self.assertListEqual(vertices[:4], sorted(choose_color(coloring), key=Vertex.__str__))

        coloring = create_coloring_helper_vertex({0: [v_g1, v_g2],
                                                  1: [v_g1, v_g2, v_g3, v_g4, v_g5]})
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
        self.assertListEqual([v_h1],       get_vertices_of_graph([v_g1, v_g2, v_h1], h))
        self.assertListEqual([],           get_vertices_of_graph([v_g1, v_g2], h))
        self.assertListEqual([],           get_vertices_of_graph([], g))

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
        self.assertEqual(0, init_coloring.num_colors)
        self.assertEqual(0, unit_coloring.num_colors)

        # 1 - 2 - 3
        g = create_graph_helper([[1, 2], [2, 3]])
        v_g1, v_g2, v_g3 = g.vertices
        init_coloring = initialize_coloring(g)
        self.assertEqual(2, init_coloring.num_colors)
        self.assertListEqual([v_g1, v_g3], init_coloring.get(1))
        self.assertListEqual([v_g2],       init_coloring.get(2))
        unit_coloring = get_unit_coloring(g)
        self.assertEqual(1, unit_coloring.num_colors)
        self.assertListEqual(g.vertices, unit_coloring.get(0))
        # 1 - 2 - 3
        #     |
        #     4 - 6 - 7
        #     |
        #     5
        g = create_graph_helper([[1, 2], [2, 3], [2, 4], [4, 5], [4, 6], [6, 7]])
        v_g1, v_g2, v_g3, v_g4, v_g5, v_g6, v_g7 = g.vertices
        init_coloring = initialize_coloring(g)
        self.assertEqual(3, init_coloring.num_colors)
        self.assertListEqual([v_g1, v_g3, v_g5, v_g7], init_coloring.get(1))
        self.assertListEqual([v_g6],                   init_coloring.get(2))
        self.assertListEqual([v_g2, v_g4],             init_coloring.get(3))
        unit_coloring = get_unit_coloring(g)
        self.assertEqual(1, unit_coloring.num_colors)
        self.assertListEqual(g.vertices, unit_coloring.get(0))
        # 1 - 2 - 3
        #     |
        #     4 - 6 - 7
        #     |
        #     5       8
        v_g8 = Vertex(g)
        g.add_vertex(v_g8)
        init_coloring = initialize_coloring(g)
        self.assertEqual(4, init_coloring.num_colors)
        self.assertListEqual([v_g8],                   init_coloring.get(0))
        self.assertListEqual([v_g1, v_g3, v_g5, v_g7], init_coloring.get(1))
        self.assertListEqual([v_g6],                   init_coloring.get(2))
        self.assertListEqual([v_g2, v_g4],             init_coloring.get(3))
        unit_coloring = get_unit_coloring(g)
        self.assertEqual(1, unit_coloring.num_colors)
        self.assertListEqual(g.vertices, unit_coloring.get(0))


if __name__ == '__main__':
    unittest.main()
