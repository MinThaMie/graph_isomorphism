"""
Module for Doubly Linked Lists
"""


class Node(object):

    def __init__(self, vertex: "Vertex", prev: "Vertex" = None, next: "Vertex" = None):
        self._vertex = vertex
        self.prev = prev
        self.next = next

    @property
    def value(self) -> "Vertex":
        return self._vertex

    def __str__(self):
        return str(self._vertex)


class DoubleLinkedList(object):
    def __init__(self, val: "Vertex" = None):
        self._head = None
        self._tail = None
        self._size = 0
        if val:
            self.pushleft(val)

    def pushleft(self, val: "Vertex"):
        """Add element to the start of the list"""
        new_node = Node(val)
        if self._size == 0:
            self._head = new_node
            self._tail = new_node
        else:
            self._head.prev = new_node
            new_node.next = self._head
            self._head = new_node
        self._size += 1

    def push(self, val: "Vertex"):
        """Add element to the end of the list"""
        new_node = Node(val)
        if self._size == 0:
            self._head = new_node
            self._tail = new_node
        else:
            self._tail.next = new_node
            new_node.prev = self._tail
            self._tail = new_node
        self._size += 1

    # def insert_after(self, node, val: "Vertex"):
    #     new_node = Node(val)
    #     new_node.prev = node
    #     if node.next is None:
    #         new_node.next = None
    #         self._tail = new_node
    #     else:
    #         new_node.next = node.next
    #         node.next.prev = new_node
    #     node.next = new_node
    #     self._size += 1
    #
    # def insert_before(self, node, val: "Vertex"):
    #     new_node = Node(val)
    #     new_node.next = node
    #     if node.prev is None:
    #         new_node.prev = None
    #         self._head = new_node
    #     else:
    #         new_node.prev = node.prev
    #         node.prev.next = new_node
    #     node.prev = new_node
    #     self._size += 1
    #
    # def append(self, node):
    #     if self._head is None:
    #         self._head = node
    #         self._tail = node
    #         node.prev = None
    #         node.next = None
    #     else:
    #         self.insert_after(self.last_node, node)
    #     self._size += 1

    def pop(self) -> "Vertex":
        """Remove last node and return value"""
        if self._size == 0:
            return None

        self._tail.prev.next = None
        self._size -= 1
        return self._tail.vertex

    def popleft(self):
        """Remove first node and return value"""
        if self._size == 0:
            return None

        self._head.next.prev = None
        self._size -= 1
        return self._head.vertex

    def delete(self, value: "Vertex"):
        """Remove node with given value if existing"""
        node = self._head
        while node is not None:
            if node.vertex == value:
                self.remove(node)
            node = node.next

    def remove(self, node: "Node") -> "Vertex":
        """Removes and returns value of given node, connects previous and next"""
        node.prev.next = node.next
        node.next.prev = node.prev

        node.next = node.prev = None
        self._size -= 1
        return node.value

    def __len__(self) -> int:
        """Number of nodes in the doubly linked list"""
        return self._size

    def __str__(self):
        """Nice representation, needs to loop over all elements!"""
        txt = "["
        node = self._head
        while node is not None:
            txt += str(node) + ','
            node = node.next
        txt = txt[:-1] + ']'
        return txt

    def __iter__(self):
        """Allows forward looping like 'for i in dll'"""
        node = self._head
        while node:
            yield node.value
            node = node.next

    def __reversed__(self):
        """Allows reversed looping"""
        node = self._tail
        while node:
            yield node.value
            node = node.prev


if __name__ == '__main__':
    from graph import Vertex, Graph

    g = Graph(False)
    v = [Vertex(g) for i in range(5)]
    n = Node(v[0])
    lst = DoubleLinkedList(v[0])
    lst.pushleft(v[1])
    lst.push(v[2])

    for u in lst:
        print(u)
    print(lst)
