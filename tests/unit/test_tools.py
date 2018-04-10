import unittest

import color_refinement
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

    def test_store_isomorphism(self):
        i = 0
        j = 1
        k = 2
        known_isomorphisms = {}.fromkeys([i, j, k], set())

        # Assert that storing an isomorphism results in a known mapping from i to j and from j to i
        color_refinement.update_known_isomorphisms(i, j, known_isomorphisms)
        self.assertEqual({j}, known_isomorphisms[i])
        self.assertEqual({i}, known_isomorphisms[j])
        self.assertEqual(set(), known_isomorphisms[k])

        # Assert that storing the same isomorphism twice changes nothing
        color_refinement.update_known_isomorphisms(j, i, known_isomorphisms)

        self.assertEqual({j}, known_isomorphisms[i])
        self.assertEqual({i}, known_isomorphisms[j])
        self.assertEqual(set(), known_isomorphisms[k])

        # Assert that storing a new known isomorphism updates all known isomorphism mappings
        color_refinement.update_known_isomorphisms(j, k, known_isomorphisms)
        self.assertEqual({j, k}, known_isomorphisms[i])
        self.assertEqual({i, k}, known_isomorphisms[j])
        self.assertEqual({i, j}, known_isomorphisms[k])


if __name__ == '__main__':
    unittest.main()
