class Node(object):

    def __init__(self, vertex: "Vertex", prev: "Vertex"=None, next: "Vertex"=None):
        self._vertex = vertex
        self._prev = prev
        self._next = next


class DoubleLinkedList(object):
    def __init__(self, node: "Vertex"=None):
        self._first_node = node
        self._last_node = node

    def insert_after(self, node, new_node):
        new_node.prev = node
        if node.next is None:
            new_node.next = None
            self._last_node = new_node
        else:
            new_node.next = node.next
            node.next.prev = new_node
        node.next = new_node

    def insert_before(self, node, new_node):
        new_node.next = node
        if node.prev is None:
            new_node.prev = None
            self._first_node = new_node
        else:
            new_node.prev = node.prev
            node.prev.next = new_node
        node.prev = new_node

    def append(self, node):
        if self._first_node is None:
            self._first_node = node
            self._last_node = node
            node.prev = None
            node.next = None
        else:
            self.insert_after(self.last_node, node)

    def remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev
        node.next = None
        node.prev = None
        if self._first_node is node:
            self._first_node = node.next
        if self._last_node is node:
            self._last_node = node.prev

