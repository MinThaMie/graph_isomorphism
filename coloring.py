"""
This is a module for the Coloring class used in the Color Refinement Algorithm
"""
# version: 7-3-18, Dorien Meijer Cluwen

from graph import *
from dll import DoubleLinkedList


class Coloring(object):
    def __init__(self):
        """
        Initializes the coloring

        Creates a dictionary to store the color classes. Color classes are stored as a key, value-pair where the key is
        a number (the color) and the value is a list of vertices belonging to that color.
        """
        self._dict = {}

    def set(self, color: int, vertex: Vertex):
        """
        Adds the given vertex to the given color class

        Add the given vertex to the color class. If the color class does not yet exist, a new color class is created to
        which the vertex is added.
        :param color: the name of the color class
        :param vertex: the `Vertex` to add to the color class
        """
        if color not in self._dict.keys():
            self._dict[color] = DoubleLinkedList()
        self._dict[color].append(vertex)
        vertex.colornum = color

    def get(self, color) -> DoubleLinkedList:
        """
        Returns the vertices belonging to the given color class

        :param color: the number (or color) of the color class
        :return: a list of vertices belonging to the color class
        """
        return list(self._dict[color])

    def color(self, vertex: Vertex) -> int:
        """
        Returns the number (or color) of the color class to which the given vertex belongs

        :param vertex: the vertex for which the color class is searched
        :return: the number (or color) of the color class of the vertex
        """
        for color in self._dict.keys():
            if vertex in self._dict[color]:
                return color
        return None

    def recolor(self, vertex: Vertex, new_color: int, color: int=None):
        """
        Puts the vertex from the color class color to a new color class (new_color)

        :param vertex: the vertex to put in another color class
        :param new_color: the color class to put the vertex in
        :param color: the color class to remove the vertex from
        """
        if color is None:
            color = self.color(vertex)
        if color is not None:
            self._dict[color].remove(vertex)
            self.set(new_color, vertex)
        else:
            print(vertex, 'not found')

    @property
    def colors(self) -> List[int]:
        """
        Returns the number (or colors) of the coloring

        :return: a list of colors of the coloring
        """
        return self._dict.keys()

    @property
    def num_colors(self) -> int:
        """
        Returns the number of color classes in the coloring

        :return: the number of color classes in the coloring
        """
        return len(self._dict.keys())

    def next_color(self) -> int:
        """
        Returns the next number (or color) for a color class

        It returns the number for the next color class. It returns 0 if there is not yet a coloring defined. If a
        coloring is initiated, the next number is the length of the dictionary + 1.
        :return:
        """
        if self._dict:
            return max(self._dict.keys()) + 1
        else:
            return 0

    def __str__(self) -> str:
        return "{ " + ', '.join(
            str(color) + "(" + str(len(self._dict[color])) + "): [" + ', '.join(str(v) for v in self._dict[color]) + "]"
            for color in self._dict.keys()) + " }"

    def status(self, g: Graph, h: Graph) -> str:
        """
        Determines the status of the coloring

        A coloring is defined as a bijection when each color class contains exactly two vertices of which one belongs to
        the graph g and the other to graph h.
        The status of the coloring is unbalanced when one of the color classes has an odd length.
        The status is `None` if the coloring is neither unbalanced nor defines a bijection.
        :param g: graph g
        :param h: graph h
        :return: "Bijection" when coloring defines a bijection, "Unbalanced" if unbalanced, `None` otherwise
        """
        maybe = False
        for color in self.colors:
            vertices = self.get(color)
            if len(vertices) % 2 == 1:
                return "Unbalanced"  # corresponds to is_unbalanced() method
            else:
                vertices_in_g = [v for v in vertices if v.in_graph(g)]
                vertices_in_h = [v for v in vertices if v.in_graph(h)]
                if len(vertices_in_g) != len(vertices_in_h):
                    return "Unbalanced"  # In my opinion also unbalanced if not exactly half the vertices are from G
                else:
                    if len(vertices) != 2:
                        maybe = True

        if maybe:
            return None
        else:
            return "Bijection"  # responds to is_bijection method

    def copy(self) -> "Coloring":
        """
        Returns a copy of the coloring

        :return: a copy of the coloring
        """
        new_coloring = Coloring()
        for color in self._dict.keys():
            for v in self._dict[color]:
                new_coloring.set(color, v)
        return new_coloring
