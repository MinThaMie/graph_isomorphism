"""
This module contains a class <permutation> for working with permutations.
Convention: the ground set is labeled 0...n-1.

Remark: composition / multiplication is reversed compared to the earlier version 
(ADS practicum 0): Now P*Q means apply Q first, then P.
"""

from coloring import Coloring
from tests import create_coloring_helper,create_graph_helper


# permv2: based on permv2SOL / perm2
# Paul Bonsma, 18-03-2015.

testvalidity = False
# Check whether permutations are initialized correctly
# (Whether they are bijections to 0..n-1, etc).
# Set to <False> for slightly faster, but possibly error prone initialization.
safeInit = True
# If <True>, then permutations are initialized safely, avoiding "shared reference"
# errors. Set to <False> for slightly faster, but possibly error prone initialization.
UseReadableOutput = True


# If True: prints permutations always using nicely readable
# cycle notations.
# If False: print(P) gives nice representation, but
# repr(P) gives technical representation (following Python style conventions).

class Permutation():
    def __init__(self, n, cycles=None, mapping=None, coloring:Coloring=None):
        """
        A permutation P on n elements can be initialized in various ways:

             P=permutation(n) gives the trivial permutation.

        A permutation can be initialized by giving the mapping from 0...n-1 to 0...n-1
        explicitly, as a Python list, e.g.:

            P=permutation(5,mapping=[0,2,1,4,3])

        The same permutation can also be initialized by giving its cycles, using a
        list of lists e.g.:

            P=permutation(5,cycles=[[1,2],[3,4]])

        Or a permutation is initialized from a Coloring
            P=Permutation(len(coloring.vertices),coloring)

        """
        self.n = n
        self.P = [i for i in range(n)] # Trivial permutation
        if mapping is not None:
            self.construct_from_mapping(mapping, n)
        elif cycles is not None:
            self.construct_from_cycles(cycles)
        elif coloring is not None:
            self.construct_from_coloring(coloring)

    def construct_from_coloring(self, coloring):
        """
        Construct permutation from coloring. Color classes form cycles.

        :param coloring: Coloring to create permutation from
        """
        cycles = []
        for _, vertices in coloring.items():
            cycles.append([v.label for v in vertices])
        self.construct_from_cycles(cycles)

    def construct_from_cycles(self, cycles):
        """
        Construct permutation by giving its cycles, using a
        list of lists e.g.:

            P=Permutation(5,cycles=[[1,2],[3,4]])
        :param cycles: list of lists
        """
        for cycle in cycles:
            for i in range(len(cycle)):
                assert self.P[cycle[i]] == cycle[i]
                # if self.P[cycle[i]]!=cycle[i]:
                #	raise permError
                self.P[cycle[i]] = cycle[(i + 1) % len(cycle)]

    def construct_from_mapping(self, mapping, n):
        """
        Construct permutation by giving the mapping from 0...n-1 to 0...n-1
        explicitly, eg. P=Permutation(5,mapping=[0,2,1,4,3])

        :param mapping: list which maps 0...n-1 to 0...n-1
        :param n: number of elements
        """
        if testvalidity:
            assert len(mapping) == n
            # if len(mapping)!=n:
            #	raise permError
            test = [0] * n
            for val in mapping:
                test[val] += 1
                assert test[val] <= 1
        # if test[val]>1:
        #	raise permError
        if safeInit:
            self.P = mapping[:]  # safe
        else:
            self.P = mapping  # fast

    def cycles(self):
        """
        Returns the cycles of the permutation.

        (Can be used to create a copy of the permutation: type:
          CopyOfP=permutation(P.n,cycles=P.cycles())
        )
        """
        C = []
        incyc = [0] * self.n
        for i in range(self.n):
            if not incyc[i]:
                if self.P[i] != i:
                    newcycle = [i]
                    C.append(newcycle)
                    incyc[i] = 1
                    next = self.P[i]
                    while next != i:
                        newcycle.append(next)
                        incyc[next] = 1
                        next = self.P[next]
        return C

    def __repr__(self):
        """
        Returns a technical string representation of the permutation.
        (Can be used to create copy of this object.)
        """
        if UseReadableOutput:
            return str(self)
        else:
            return 'permutation(' + str(self.n) + ',cycles=' + str(self.cycles()) + ')'

    def __str__(self):
        """
        Returns a nice string representation of the permutation, using cycle notation.
        """
        # C = self.cycles()
        # s = ''
        # for cycle in C:
        #     cyclestr = '('
        #     for el in cycle:
        #         cyclestr += str(el) + ','
        #     s += cyclestr[:len(cyclestr) - 1] + ')'
        # if s == '':
        #     s = '()'
        return str(self.P)

    def __getitem__(self, key):
        """
        Returns the image of element <key> under this permutation.
        (<key> should be an integer from 0 to n-1.)
        """
        return self.P[key]

    def __neg__(self):
        """
        Returns the *inverse* of this permutation.
        Usage: simply type -P, for a permutation object P.
        """
        Q = [0] * self.n
        for i in range(self.n):
            Q[self.P[i]] = i
        return Permutation(self.n, mapping=Q)

    def __mul__(self, other):
        """
        Returns the *composition* of permutation <self> and permutation <other>.
        Convention: <other> is applied first!
        Usage: simply type P*Q to obtain the composition of P and Q.
        (Q is applied first.)
        """
        # if self.n != other.n:
        #     raise permError()
        Q = [0] * self.n
        for i in range(self.n):
            Q[i] = self.P[other.P[i]]
        return Permutation(self.n, mapping=Q)

    def __pow__(self, i):
        """
        Returns the <i>-th power of the permutation.
        Usage: simply type P**i.
        """
        if i == 0:
            return Permutation(self.n)
        if i < 0:
            i = -i
            P = -self
        else:
            P = self
        Q = Permutation(self.n)
        while i != 0:
            if i % 2 == 1:
                Q *= P
            i = i // 2
            P = P * P
        return Q

    def istrivial(self):
        """
        Returns <True> iff the permutation is trivial, so if it maps
        every element in 0...n-1 to itself.
        """
        for i in range(self.n):
            if self.P[i] != i:
                return False
        return True

    def __eq__(self, other):
        """
        Returns <True> iff permutation <self> equals permutation <other>, in the sense
        that they represent the same mapping.
        (May be different objects in memory.)
        Usage: Type P==Q.
        """
        if not hasattr(other, 'P'):
            return False
        for i in range(self.n):
            if self.P[i] != other.P[i]:
                return False
        return True

    def __len__(self):
        return len(self.P)

if __name__ == "__main__":
    G0 = create_graph_helper(edges=[[0, 1], [1, 2], [2, 3], [3, 4], [2, 4], [4, 5], [5, 6]])
    coloring = create_coloring_helper(G0.vertices,
                                        {0: [0, 6], 1: [1, 5], 2: [3], 3: [2, 4]})
    perm = Permutation(len(coloring.vertices), coloring=coloring)
    print(perm)
