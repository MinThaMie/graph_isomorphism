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
        self._vertex_dict = {}

    def set(self, vertex: Vertex, color: int):
        """
        Adds the given vertex to the given color class

        Add the given vertex to the color class. If the color class does not yet exist, a new color class is created to
        which the vertex is added.
        :param color: the name of the color class
        :param vertex: the `Vertex` to add to the color class
        :raises KeyError when vertex already belongs to the coloring
        """
        if color not in self._dict:
            self._dict[color] = DoubleLinkedList()
        if vertex in self._vertex_dict:
            raise KeyError('Vertex {} already in coloring, color: {}'.format(str(vertex), str(self.color(vertex))))

        self._dict[color].append(vertex)
        self._vertex_dict[vertex] = color

    def get(self, color) -> DoubleLinkedList:
        """
        Returns the vertices belonging to the given color class

        :param color: the number (or color) of the color class
        :return: a list of vertices belonging to the color class
        """
        return list(self._dict[color])

    def add(self, vertices: List[Vertex], color=None):
        """
        Add multiple colors, recolors vertices already in the coloring

        :param vertices: vertices to add/recolor
        :param color: color for vertices, pick new color if None
        :return:
        """
        if color is None:
            color = self.next_color()

        for v in vertices:
            if v in self._vertex_dict:
                self.recolor(v,color)
            else:
                self.set(v, color)

    def color(self, vertex: Vertex) -> int:
        """
        Returns the number (or color) of the color class to which the given vertex belongs

        :param vertex: the vertex for which the color class is searched
        :return: the number (or color) of the color class of the vertex or None if not found
        """
        return self._vertex_dict.get(vertex)

    def recolor(self, vertex: Vertex, new_color: int):
        """
        Moves the vertex from the old color class color to a new color class (new_color)

        :param vertex: the vertex to put in another color class
        :param new_color: the color class to put the vertex in
        :param color: the color class to remove the vertex from
        :raises KeyError when vertex is not found in the coloring
        """
        old_color = self.color(vertex)
        if old_color is None:
            raise KeyError('Vertex ' + str(vertex) + ' not found in coloring')
        else:
            self._dict[old_color].remove(vertex)
            self._vertex_dict.pop(vertex)
            self.set(vertex, new_color)

    @property
    def colors(self) -> List[int]:
        """
        Returns the number (or colors) of the coloring

        :return: a list of colors of the coloring
        """
        return list(self._dict.keys())

    @property
    def vertices(self) -> List[Vertex]:
        """
        Returns the vertices in the coloring

        :return: list of vertices in the coloring
        """
        return list(self._vertex_dict.keys())

    def __len__(self) -> int:
        """
        Returns the number of color classes in the coloring

        :return: the number of color classes in the coloring
        """
        return len(self._dict.keys())

    def items(self):
        """
        Return a copy of a set of the (color,List[Vertex]) pairs in the Coloring
        :return: set of (color,DoubleLinkedList()) pairs
        """
        return self._dict.items()

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
                return "Unbalanced"
            else:
                vertices_in_g = [v for v in vertices if v.in_graph(g)]
                vertices_in_h = [v for v in vertices if v.in_graph(h)]
                if len(vertices_in_g) != len(vertices_in_h):
                    return "Unbalanced"
                else:
                    if len(vertices) != 2:
                        maybe = True

        if maybe:
            return None
        else:
            return "Bijection"

    def copy(self) -> "Coloring":
        """
        Returns a copy of the coloring

        Note that the copy uses the same vertices
        :return: a copy of the coloring
        """
        new_coloring = Coloring()
        for c, v in self.items():
            new_coloring.add(v,color=c)
        return new_coloring
