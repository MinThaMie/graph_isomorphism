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


if __name__ == '__main__':
    unittest.main()
