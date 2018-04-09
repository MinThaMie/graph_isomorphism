"""
Test file for Counter
"""
import unittest

from color_refinement_helper import initialize_coloring, generate_neighbour_count_with_color
from graph_io import *

PATH = 'graphs/'


class CounterCase(unittest.TestCase):

    def test_counter_arrow(self):
        # Takes color 1 (smallest degree)
        # 0,2 and 4 don't have neighbours with degree 1
        # 3 has one neighbour with degree 1
        # 1 has two neighbours with degree 1
        #    1
        #  / | \
        # 0  3  2
        #    |
        #    4
        with open(PATH + "arrow.grl") as f:
            graphs = load_graph(f, read_list=True)
        graph = graphs[0][0]
        coloring = initialize_coloring(graph)
        color = sorted(coloring.colors)[0]
        counter = generate_neighbour_count_with_color(coloring, color)
        for num_neigh in counter.get(1).values():
            self.assertEqual(num_neigh, 0)
        for num_neigh in counter.get(2).values():
            self.assertEqual(num_neigh, 1)
        for num_neigh in counter.get(3).values():
            self.assertEqual(num_neigh, 2)

    def test_counter_domino(self):
        # Takes color 2 (smallest degree)
        # 4 and 5 have each other as neighbours with that color, and 0 and 1 the same
        # 2 and 3 have 0 and 4, 5 and 1 as neighbours with color 2
        #   4 ----- 5
        #   |       |
        #   2 ----- 3
        #   |       |
        #   0 ----- 1
        with open(PATH + "domino.grl") as f:
            graphs = load_graph(f, read_list=True)
        graph = graphs[0][0]
        coloring = initialize_coloring(graph)
        color = sorted(coloring.colors)[0]
        counter = generate_neighbour_count_with_color(coloring, color)
        for num_neigh in counter.get(2).values():
            self.assertEqual(num_neigh, 1)
        for num_neigh in counter.get(3).values():
            self.assertEqual(num_neigh, 2)


if __name__ == '__main__':
    unittest.main()
