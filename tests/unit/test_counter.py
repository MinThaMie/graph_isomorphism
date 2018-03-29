"""
Test file for Counter
"""
import unittest
from graph_io import *
from color_refiment_helper import initialize_coloring, generate_neighbour_count_with_color
PATH = 'graphs/'
class CounterCase(unittest.TestCase):

    def test_counter_arrow(self):
        #    1
        #  / | \
        # 0  3  2
        #    |
        #    4
        with open(PATH + "arrow.grl") as f:
            L = load_graph(f, read_list=True)
        graph = L[0][0]
        coloring = initialize_coloring(graph)
        color = sorted(coloring.colors)[0]
        counter = generate_neighbour_count_with_color(graph, color)
        for num_neigh in counter.get(1).values():
            self.assertEqual(num_neigh, 0)
        for num_neigh in counter.get(2).values():
            self.assertEqual(num_neigh, 1)
        for num_neigh in counter.get(3).values():
            self.assertEqual(num_neigh, 2)

    def test_counter_domino(self):
        #   4 ----- 5
        #   |       |
        #   2 ----- 3
        #   |       |
        #   0 ----- 1
        with open(PATH + "domino.grl") as f:
            L = load_graph(f, read_list=True)
        graph = L[0][0]
        coloring = initialize_coloring(graph)
        color = sorted(coloring.colors)[0]
        counter = generate_neighbour_count_with_color(graph, color)
        for num_neigh in counter.get(2).values():
            self.assertEqual(num_neigh, 1)
        for num_neigh in counter.get(3).values():
            self.assertEqual(num_neigh, 2)

if __name__ == '__main__':
    unittest.main()