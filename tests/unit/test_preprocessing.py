import unittest

from color_refinement_helper import graph_to_modules
from preprocessing import check_modular_decomposition, modular_decomposition_factor, \
    calculate_modular_decomposition_and_factor, remove_loners, checks, check_complement, get_modular_decomposition_sizes
from tests import *


class TestPreprocessing(unittest.TestCase):
    graph = Graph(directed=False)

    @staticmethod
    def _prime_module(): return [Vertex(TestPreprocessing.graph)]

    @staticmethod
    def _twin_module(): return [Vertex(TestPreprocessing.graph), Vertex(TestPreprocessing.graph)]

    @staticmethod
    def _triplet_module(): return [Vertex(TestPreprocessing.graph), Vertex(TestPreprocessing.graph),
                                   Vertex(TestPreprocessing.graph)]

    def setUp(self):
        tests.set_up_test_graphs()

    def setUp(self):
        tests.set_up_test_graphs()

    def test_checks(self):
        g = tests.v4e4_connected
        h = tests.v4e4_connected
        self.assertTrue(checks(g, h))

        g = tests.v5e4loop_unconnected
        self.assertFalse(checks(g, h))

    def test_loner_removal(self):
        g = tests.v5e4loop_unconnected  # g has 1 'loner'
        num_vertices = len(g.vertices)
        g = remove_loners(g)
        self.assertEqual(num_vertices - 1, len(g.vertices))

    def test_use_complement(self):
        # A star shaped graph that should use the complement
        many_edges_graph = tests.v5e7
        g, h = check_complement(many_edges_graph, many_edges_graph)
        self.assertTrue(g is not many_edges_graph)
        self.assertTrue(h is not many_edges_graph)
        # A nice W shaped graph that should not return the complement
        w_shaped_graph = tests.v5e4loop_unconnected
        g, h = check_complement(w_shaped_graph, w_shaped_graph)
        self.assertTrue(g is w_shaped_graph)
        self.assertTrue(h is w_shaped_graph)

    def test_find_components(self):
        is_connected, components = preprocessing.find_components(tests.v5e4loop_unconnected)
        self.assertFalse(is_connected)
        self.assertEqual(2, len(components))
        self.assertEqual([tests.v5e4loop_unconnected.find_vertex(4)], components[2])
        component_to_be_found = [tests.v5e4loop_unconnected.find_vertex(1), tests.v5e4loop_unconnected.find_vertex(2),
                                 tests.v5e4loop_unconnected.find_vertex(3), tests.v5e4loop_unconnected.find_vertex(5)]
        self.assertEqual(component_to_be_found, components[1])
        is_connected, components = preprocessing.find_components(tests.v5e7)
        self.assertTrue(is_connected)
        self.assertEqual(1, len(components))


if __name__ == '__main__':
    unittest.main()
    def test_get_modular_decomposition_sizes(self):
        md = [self._prime_module()]
        self.assertEqual([1], list(get_modular_decomposition_sizes(md)))

        md += [self._prime_module()]
        self.assertEqual([1, 1], list(get_modular_decomposition_sizes(md)))

        md += [self._twin_module()]
        self.assertCountEqual([1, 1, 2], list(get_modular_decomposition_sizes(md)))

        md += [self._triplet_module()]
        self.assertCountEqual([1, 1, 2, 3], list(get_modular_decomposition_sizes(md)))

    def test_check_modular_decomposition(self):
        # Assert that the same singleton modular decompositions (MDs) may be isomorphic
        md0 = [self._prime_module()]
        md1 = [self._prime_module()]
        self.assertTrue(check_modular_decomposition(md0, md1))
        self.assertTrue(check_modular_decomposition(md1, md0))

        # Assert that two prime modules in both MDs can be isomorphic
        md0 += [self._prime_module()]
        md1 += [self._prime_module()]
        self.assertTrue(check_modular_decomposition(md0, md0))
        self.assertTrue(check_modular_decomposition(md1, md0))

        # Assert that different modular decompositions indicate anisomorphism
        md0 += [self._prime_module()]
        self.assertFalse(check_modular_decomposition(md0, md1))
        self.assertFalse(check_modular_decomposition(md1, md0))

        # Assert that a modular decomposition with a different number of different modules in different order do not
        # indicate anisomorphism
        md0 += [self._twin_module()]
        md1 += [self._twin_module(), self._prime_module()]
        self.assertTrue(check_modular_decomposition(md0, md1))
        self.assertTrue(check_modular_decomposition(md1, md0))

        # Assert that MDs with identical size but different module sizes indicate anisomorphism
        md0 += [self._prime_module()]
        md1 += [self._twin_module()]
        self.assertFalse(check_modular_decomposition(md0, md1))
        self.assertFalse(check_modular_decomposition(md1, md0))

    def test_modular_decomposition_factor(self):
        md = [self._prime_module()]
        self.assertEqual(1, modular_decomposition_factor(md))

        md += [self._prime_module()]
        self.assertEqual(1, modular_decomposition_factor(md))

        md += [self._twin_module()]
        self.assertEqual(2, modular_decomposition_factor(md))

        md += [self._twin_module()]
        self.assertEqual(4, modular_decomposition_factor(md))

        md += [self._triplet_module()]
        self.assertEqual(24, modular_decomposition_factor(md))

    def test_calculate_modular_decomposition_and_factor(self):
        graph = Graph(directed=False)
        md_graph = graph_to_modules(graph)
        graph_md, factor = calculate_modular_decomposition_and_factor(graph, md_graph)
        self.assertTrue(graph is graph_md)
        self.assertEqual(1, factor)

        graph = tests.non_trivial_graph
        md_graph = graph_to_modules(graph)
        graph_md, factor = calculate_modular_decomposition_and_factor(graph, md_graph)
        self.assertFalse(graph is graph_md)
        self.assertEqual(2, factor)

        graph = tests.modular_decomposition_graph
        md_graph = graph_to_modules(graph)
        _, factor = calculate_modular_decomposition_and_factor(graph, md_graph)
        self.assertEqual(24, factor)


if __name__ == '__main__':
    unittest.main()
