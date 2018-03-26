import unittest

import tests
from graph import Graph


class GraphTests(unittest.TestCase):

    def test_name(self):
        graph = Graph(directed=False)
        self.assertEqual('G', graph.name)
        graph.name = 'spam'
        self.assertEqual('spam', graph.name)


if __name__ == '__main__':
    unittest.main()
