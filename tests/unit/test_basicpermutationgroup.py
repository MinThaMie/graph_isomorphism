import unittest
from basicpermutationgroup import *
from color_refinement_helper import compare
from graph import Graph
from coloring import Coloring


class TestBasicPermutationGroup(unittest.TestCase):

    def test_compute_orbit(self):
        # H = <p,q> with p = (0,1,2)(4,5) and q = (2,3). Let alpha = 0.
        p = Permutation(6, cycles=[[0, 1, 2], [4, 5]])
        q = Permutation(6, cycles=[[2, 3]])
        orbit, transversal = compute_orbit([p, q], 0, return_transversal=True)

        expected_orbit = [0, 1, 2, 3]
        expected_transversal = [Permutation(6),
                                Permutation(6, cycles=[[0, 1, 2], [4, 5]]),
                                Permutation(6, cycles=[[0, 2, 1]]),
                                Permutation(6, cycles=[[0, 3, 2, 1]])]

        self.assertListEqual(expected_orbit, orbit)
        self.assertListEqual(expected_transversal, transversal)

        # Wolfram alpha example: http://mathworld.wolfram.com/GroupOrbit.html
        #  H = {(0123),(1023),(0132),(1032)}
        h = [Permutation(4, mapping=[0, 1, 2, 3]), Permutation(4, mapping=[1, 0, 2, 3]),
             Permutation(4, mapping=[0, 1, 3, 2]), Permutation(4, mapping=[1, 0, 3, 2])]

        self.assertTrue(compare([0, 1], compute_orbit(h, 0)))
        self.assertTrue(compare([0, 1], compute_orbit(h, 1)))
        self.assertTrue(compare([2, 3], compute_orbit(h, 2)))
        self.assertTrue(compare([2, 3], compute_orbit(h, 3)))

    def test_schreier_generators(self):
        pass

    def test_find_non_trivial_orbit(self):
        pass
        # p = Permutation(6, cycles=[[0, 1, 2], [4, 5]])
        # q = Permutation(6, cycles=[[2, 3]])
        #
        # print(find_non_trivial_orbit([p, q]))

    def test_reduce(self):
        pass

    def test_stabilizer(self):
        # Wolfram alpha example: http://mathworld.wolfram.com/GroupOrbit.html
        #  H = {(0123),(1023),(0132),(1032)}
        h = [Permutation(4, mapping=[0, 1, 2, 3]), Permutation(4, mapping=[1, 0, 2, 3]),
             Permutation(4, mapping=[0, 1, 3, 2]), Permutation(4, mapping=[1, 0, 3, 2])]

        # Note: it the trivial permutation is ignored
        self.assertTrue(compare([h[2]], stabilizer(h, 0)), 'expected [[0,1,3,2]] got' + str(stabilizer(h, 0)))
        self.assertTrue(compare([h[2]], stabilizer(h, 1)), 'expected [[0,1,3,2]] got' + str(stabilizer(h, 0)))
        self.assertTrue(compare([h[1]], stabilizer(h, 2)), 'expected [[1,0,2,3]] got' + str(stabilizer(h, 0)))

    def test_member_of(self):
        # Use example of sheets
        # H = <p,q> with p = (0,1,2)(4,5) and q = (2,3)

        g = Graph(directed=False, n=6)
        vg_0, vg_1, vg_2, vg_3, vg_4, vg_5 = g.vertices
        coloring_p = Coloring()
        coloring_p.add([vg_0, vg_1, vg_2])
        coloring_p.add([vg_4, vg_5])
        p = Permutation(len(g.vertices), coloring=coloring_p)

        coloring_q = Coloring()
        coloring_q.add([vg_2, vg_3])
        q = Permutation(len(g.vertices), coloring=coloring_q)

        H = list()
        H.append(p)
        H.append(q)

        # test if (0,2) is in generating set (ex of slides)
        coloring_f = Coloring()
        coloring_f.add([vg_0, vg_2])
        f = Permutation(len(g.vertices), coloring=coloring_f)
        self.assertTrue(member_of(f, H))

        # test if (0,4) is in generating set
        coloring_f = Coloring()
        coloring_f.add([vg_0, vg_4])
        f = Permutation(len(g.vertices), coloring=coloring_f)
        self.assertFalse(member_of(f, H))

        # test if (0,1) is in generating set
        coloring_f = Coloring()
        coloring_f.add([vg_0, vg_1])
        f = Permutation(len(g.vertices), coloring=coloring_f)
        self.assertTrue(member_of(f, H))

        # test if (0,5) is in generating set
        coloring_f = Coloring()
        coloring_f.add([vg_0, vg_5])
        f = Permutation(len(g.vertices), coloring=coloring_f)
        self.assertFalse(member_of(f, H))

        # test if p and q are in the generating set <p,q>
        self.assertTrue(member_of(p, H))
        self.assertTrue(member_of(q, H))

    def test_member_of2(self):
        # Permutation group D_4: symmetries of a rectangle
        #  0 -- 1     <- trivial permutation
        #  |    |
        #  3 -- 2
        # Has generators p = (0123) rotation, and q = (03)(12) reflection across horizontal plane

        D4_members = {'e': [[]], 'p': [[0, 1, 2, 3]], 'pp': [[0, 2], [1, 3]], 'ppp': [[0, 3, 2, 1]],
                      'q': [[0, 3], [1, 2]], 'qp': [[1, 3]], 'qpp': [[0, 1], [2, 3]], 'qppp': [[0, 2]]}

        p = Permutation(4, cycles=D4_members['p'])
        q = Permutation(4, cycles=D4_members['q'])
        D4 = [p, q, Permutation(4)]

        for element in D4_members.values():
            f = Permutation(4, cycles=element)
            print(element, 'member of D4?', member_of(f, D4))
            self.assertTrue(member_of(f, D4))

        # (3210) should not be an element
        f = Permutation(4, cycles=[[1, 2]])
        self.assertFalse(member_of(f, D4))

    def test_member_of3(self):
        # Another is_member test
        # Use example of sheets
        # H = <p,q> with p = (0,1,2)(4,5) and q = (2,3)

        p = Permutation(6, cycles=[[0, 1, 2], [4, 5]])
        q = Permutation(6, cycles=[[2, 3]])
        H = [p,q]
        f = Permutation(6, cycles=[[0, 2]]) # f = p q p^2 q p q p^2

        # Check that f = p q p^2 q p q p^2
        self.assertEqual(f, p * q * p**2 * q * p * q * p**2)

        # Check that trivial permutation is part of H
        self.assertTrue(Permutation(6),H)

        factors_of_f = [p, q, p**2, q, p, q, p**2]
        element = Permutation(6)
        for elem in factors_of_f:
            element *= elem
            self.assertTrue(member_of(element, H))


if __name__ == '__main__':
    unittest.main()
