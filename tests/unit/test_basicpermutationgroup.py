import unittest
from basicpermutationgroup import *
from basicpermutationgroup import order_computation
from color_refinement_helper import compare
from graph import Graph
from coloring import Coloring
from permv2 import Permutation


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

    def test_member_of4(self):
        # trivial permuatiation
        H = Permutation(n=5)
        f = Permutation(n=5)
        f2 = Permutation(n=5, cycles=[[0, 1]])
        self.assertTrue(member_of(f, [H]))
        self.assertFalse(member_of(f2, [H]))

        H1 = Permutation(n=6, cycles=[[0, 1, 2], [4, 5]])
        H2 = Permutation(n=6, cycles=[[2, 3]])
        H = [H1, H2]
        f = Permutation(n=6, cycles=[[0, 2]])
        self.assertTrue(f, H)

    def test_permutation_coloring(self):
        g = Graph(directed=False, n=5)
        h = Graph(directed=False, n=5)
        vg_0, vg_1, vg_2, vg_3, vg_4 = g.vertices
        vh_0, vh_1, vh_2, vh_3, vh_4 = h.vertices

        coloring_p = Coloring()
        p = Permutation(0, coloring=coloring_p)
        self.assertEqual(0, len(p))

        coloring_p.add([vg_0, vh_0])
        coloring_p.add([vg_1, vh_1])
        p = Permutation(2, coloring=coloring_p)
        self.assertEqual(0, p.P[0])
        self.assertEqual(1, p.P[1])

        coloring_p = Coloring()
        coloring_p.add([vg_0, vh_1])
        coloring_p.add([vg_1, vh_0])
        p = Permutation(2, coloring=coloring_p)
        self.assertEqual(1, p.P[0])
        self.assertEqual(0, p.P[1])

        # TODO: deze test gaat nog mis...
        coloring_p = Coloring()
        coloring_p.add([vg_0, vh_1])
        coloring_p.add([vg_1, vh_2])
        coloring_p.add([vg_2, vh_3])
        coloring_p.add([vg_3, vh_4])
        coloring_p.add([vg_4, vh_0])
        p = Permutation(5, coloring=coloring_p)
        self.assertEqual(1, p.P[0])
        self.assertEqual(2, p.P[1])
        self.assertEqual(3, p.P[2])
        self.assertEqual(4, p.P[3])
        self.assertEqual(0, p.P[4])

    def test_order_computation(self):  # TODO: to a testclass of basicpermutations
        g = Graph(directed=False, n=6)
        vg_0, vg_1, vg_2, vg_3, vg_4, vg_5 = g.vertices
        # mapping only to itself
        coloring_p = Coloring()
        coloring_p.add([vg_0])
        coloring_p.add([vg_1])
        p = Permutation(len(g.vertices), coloring=coloring_p)
        H = [p]
        self.assertEqual(1, order_computation(H))
        # mapping to itself and 1 other node
        coloring_p = Coloring()
        coloring_p.add([vg_0, vg_1])
        p = Permutation(len(g.vertices), coloring=coloring_p)
        H = [p]
        self.assertEqual(2, order_computation(H))
        # this is the permutation example of the lecture
        coloring_p = Coloring()
        coloring_p.add([vg_0, vg_1, vg_2])
        coloring_p.add([vg_4, vg_5])
        p = Permutation(len(g.vertices), coloring=coloring_p)
        coloring_q = Coloring()
        coloring_q.add([vg_2, vg_3])
        q = Permutation(len(g.vertices), coloring=coloring_q)
        H = [p, q]
        self.assertEqual(48, order_computation(H))


if __name__ == '__main__':
    unittest.main()




    # I have commented it out because it makes permutations based on a single graph coloring: don't know if it still works
    # def test_coloring_to_permutation(self):
    #     g = Graph(directed=False, n=6, name='G')
    #     h = Graph(directed=False, n=6, name='H')
    #     vg_1, vg_2, vg_3, vg_4, vg_5, vg_6 = g.vertices
    #     vh_1, vh_2, vh_3, vh_4, vh_5, vh_6 = h.vertices
    #     coloring = Coloring()
    #
    #     # coloring.add([vg_1, vh_1])  #En willen we dit echt op 2 graven doen?
    #     coloring.add([vg_1])  # Is het niet netter om alle vertices te kleuren?
    #     perm = Permutation(len(g.vertices), coloring=coloring)
    #
    #     self.assertEqual(6, len(perm.P))
    #
    #     coloring.add([vg_2, vg_3])  # , vh_2, vh_3])
    #     perm = Permutation(len(g.vertices), coloring=coloring)
    #     # #perm = coloring_to_permutation(coloring, g)
    #     self.assertEqual(6, len(perm.P))
    #     self.assertEqual(vg_2.label, perm.P[vg_3.label])
    #     self.assertEqual(vg_3.label, perm.P[vg_2.label])
    #
    #     coloring.add([vg_4, vg_5, vg_6])  # vh_4, vg_5, vh_5, vg_6, vh_6])
    #     perm = Permutation(len(coloring.vertices), coloring=coloring)
    #     # #perm = coloring_to_permutation(coloring, g)
    #     self.assertEqual(6, len(perm.P))
    #     self.assertEqual(vg_5.label, perm.P[vg_4.label])
    #     self.assertEqual(vg_6.label, perm.P[vg_5.label])
    #     self.assertEqual(vg_4.label, perm.P[vg_6.label])

    # def test_compute_orbit(self):
    #     g = Graph(directed=False, n=6)
    #     vg_0, vg_1, vg_2, vg_3, vg_4, vg_5 = g.vertices
    #     coloring_p = Coloring()
    #     coloring_p.add([vg_0, vg_1, vg_2])
    #     coloring_p.add([vg_4, vg_5])
    #     p = Permutation(len(g.vertices), coloring=coloring_p)
    #
    #     coloring_q = Coloring()
    #     coloring_q.add([vg_2, vg_3])
    #     q = Permutation(len(g.vertices), coloring=coloring_q)
    #
    #     H = list()
    #     H.append(p)
    #     H.append(q)
    #     # test if (0,2) is in generating set (ex of slides)
    #     coloring_f = Coloring()
    #     coloring_f.add([vg_0, vg_2])
    #     f = Permutation(len(g.vertices), coloring=coloring_f)
    #
    #     self.assertTrue(member_of(f, H))
    #     # test if (0,4) is in generating set
    #     coloring_f = Coloring()
    #     coloring_f.add([vg_0, vg_4])
    #     f = Permutation(len(g.vertices), coloring=coloring_f)
    #     self.assertFalse(member_of(f, H))
    #
    #     # test if (0,1) is in generating set
    #     coloring_f = Coloring()
    #     coloring_f.add([vg_0, vg_1])
    #     f = Permutation(len(g.vertices), coloring=coloring_f)
    #     self.assertTrue(member_of(f, H))
    #
    #     # test if (0,5) is in generating set
    #     coloring_f = Coloring()
    #     coloring_f.add([vg_0, vg_5])
    #     f = Permutation(len(g.vertices), coloring=coloring_f)
    #     self.assertFalse(member_of(f, H))
