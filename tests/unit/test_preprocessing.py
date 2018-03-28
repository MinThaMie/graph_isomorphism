import unittest
import preprocessing
from tests import *


class TestPreprocessing(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.v4e4 = graph_vertex4edge4()
        cls.v5e4loop = graph_vertex5edge4loop()

    def test_checks(self):
        g = self.v4e4
        h = self.v4e4
        self.assertTrue(preprocessing.checks(g, h))

        g = self.v5e4loop
        self.assertFalse(preprocessing.checks(g, h))

    def test_loner_removal(self):
        g = self.v5e4loop
        num_vertices = len(g.vertices)
        preprocessing.remove_loners(g)
        self.assertEqual(num_vertices - 1, len(g.vertices))
