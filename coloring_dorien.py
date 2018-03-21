"""
This is a module for the Coloring class used in the Color Refinement Algorithm
"""
# version: 7-3-18, Dorien Meijer Cluwen

from graph import *


class Coloring(object):
    def __init__(self):
        self._dict = {}

    def set(self, color: "Integer", vertex: "Vertex"):
        if color not in self._dict.keys():
          self._dict[color] = []
        self._dict[color].append(vertex)
        vertex.colornum = color

    def get(self, color) -> List["Vertex"]:
        return list(self._dict[color])

    def color(self, vertex) -> "Integer":
        for color in self._dict.keys():
            if vertex in self._dict[color]:
                return color
        return None

    def recolor(self, vertex, new_color, color=None):
        if color is None:
            color = self.color(vertex)
        if color is not None:
            self._dict[color].remove(vertex)
            self.set(new_color,vertex)
        else:
            print(vertex,'not found')

    @property
    def colors(self):
        return self._dict.keys()

    @property
    def num_colors(self):
        return len(self._dict.keys())

    def next_color(self):
        if self._dict:
            return max(self._dict.keys()) + 1
        else:
            return 0

    def __str__(self) -> str:
        return "{ " + ', '.join(str(color) + "(" + str(len(self._dict[color]))+ "): [" + ', '.join(str(v) for v in self._dict[color]) + "]" for color in self._dict.keys()) + " }"

    def status(self, g: "Graph", h: "Graph"):
        """
        Determine status of given coloring, eg. defines a bijection, balanced, unbalanced
        :param g: Graph G
        :param h: Graph H
        :return: "Bijection" when coloring defines a bijection, "Unbalanced" if unbalanced, None otherwise
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

    def copy(self):
        new_coloring = Coloring()
        for color in self._dict.keys():
            for v in self._dict[color]:
                new_coloring.set(color,v)
        return new_coloring

