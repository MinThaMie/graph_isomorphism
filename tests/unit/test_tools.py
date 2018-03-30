import unittest

import tools
from tools import unique_integer


class ToolsTests(unittest.TestCase):

    def test_unique_integer(self):
        # Ensure we know the maximum generated int so we can test if the next generated int is unique
        generated_max = max(tools._generated_integers, default=0)
        tools._generated_integers |= set(range(0, 2 * generated_max))

        self.assertEqual(2 * generated_max, unique_integer())
        self.assertEqual(2 * generated_max + 1, unique_integer())
        self.assertEqual(tools._last_integer + 1, unique_integer())

    def test_store_morphism(self):
        i = 0
        j = 1
        known_isomorphisms = {}.fromkeys({i, j}, set())

        tools.store_morphism(i, j, known_isomorphisms)

        self.assertEqual({j}, known_isomorphisms[i])
        self.assertEqual({i}, known_isomorphisms[j])

        tools.store_morphism(i, j, known_isomorphisms)

        self.assertEqual({j}, known_isomorphisms[i])
        self.assertEqual({i}, known_isomorphisms[j])

        i = 2
        known_isomorphisms[2] = set()

        tools.store_morphism(i, j, known_isomorphisms)

        self.assertEqual({1, 2}, known_isomorphisms[0])
        self.assertEqual({0, 2}, known_isomorphisms[1])
        self.assertEqual({0, 1}, known_isomorphisms[2])


if __name__ == '__main__':
    unittest.main()
