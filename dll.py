"""
Module for Doubly Linked Lists
"""
#See for more info on generics in python https://docs.python.org/3/library/typing.html
from typing import TypeVar
T = TypeVar('T')


class Node(object):
    def __init__(self, value: "T", prev: "Node" = None, next: "Node" = None):
        self._value = value
        self.prev = prev
        self.next = next

    @property
    def value(self) -> "T":
        return self._value

    def __str__(self):
        return str(self._value)


class DoubleLinkedList(object):
    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0

    def append_left(self, val: "T"):
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

    def append(self, val: "T"):
        """Add element to the end of the list"""
        new_node = Node(val)
        if self._size == 0:
            self._head = self._tail = new_node
        else:
            self._tail.next = new_node
            new_node.prev = self._tail
            self._tail = new_node
        self._size += 1

    def pop(self) -> "T":
        """Remove last node and return value"""
        if self._size == 0:
            return None
        elif self._size == 1:
            last_node = self._tail
            self._head = self._tail = None
        else:
            last_node, self._tail = self._tail, self._tail.prev
            self._tail.next = None
        self._size -= 1
        return last_node.value

    def pop_left(self):
        """Remove first node and return value"""
        if self._size == 0:
            return None
        elif self._size == 1:
            first_node = self._head
            self._head = self._tail = None
        else:
            first_node, self._head = self._head, self._head.next
            self._head.prev = None

        self._size -= 1
        return first_node.value


    def insert_after(self, node: "Node", val: "T"):
        new_node = Node(val)
        new_node.prev = node
        if node.next is None:
            new_node.next = None
            self._tail = new_node
        else:
            new_node.next = node.next
            node.next.prev = new_node
        node.next = new_node
        self._size += 1

    def insert_before(self, node: "Node", val: "T"):
        new_node = Node(val)
        new_node.next = node
        if node.prev is None:
            new_node.prev = None
            self._head = new_node
        else:
            new_node.prev = node.prev
            node.prev.next = new_node
        node.prev = new_node
        self._size += 1

    def delete(self, value: "T"):
        """Remove node with given value if existing"""
        node = self._head
        while node is not None:
            if node.value == value:
                self.remove(node)
                return
            node = node.next

    def remove(self, node: "Node") -> "T":
        """Removes and returns value of given node, connects previous and next"""
        node.prev.next = node.next
        node.next.prev = node.prev

        node.next = node.prev = None
        self._size -= 1
        return node.value

    def find(self, value: "T") -> "Node":
        """Returns first node with given value, or None if no such node is found"""
        node = self._head
        while node is not None:
            if node.value == value:
                return node
            node = node.next
        return None

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

    lst2 = DoubleLinkedList(1)
    lst2.push(2)
    lst2.push(2)
    lst2.pushleft(3)
    print(lst2)
