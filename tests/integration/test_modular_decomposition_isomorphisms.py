import unittest

from color_refinement_helper import graph_to_modules, modules_to_graph_with_module_isomorphism
from tools import create_graph_helper


class Test(unittest.TestCase):
    def test_moeilijkere_graaf(self):
        # Dit assert nu niks, maar deze method is wel een begin

        g = create_graph_helper(
            [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (5, 7), (5, 8), (3, 8), (3, 9), (1, 9), (2, 9),
             (1, 10), (6, 11), (7, 11), (11, 12), (11, 13), (11, 14), (12, 13), (12, 14), (13, 14)])

        h = g.deepcopy()

        md = graph_to_modules(g + h)
        graph_md, modular_iso = modules_to_graph_with_module_isomorphism(md)


if __name__ == '__main__':
    unittest.main()
