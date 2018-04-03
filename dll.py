"""
Module for Doubly Linked Lists
"""
# See for more info on generics in python https://docs.python.org/3/library/typing.html
from typing import TypeVar

T = TypeVar('T')


class Node(object):
    def __init__(self, value: T, prev_node:"Node"= None, next_node:"Node"= None):
        """
        Initializes a node

        Creates a node with the value as the node, and prev as the previous node and next as the next node in the list.
        If no previous and next node are given, these values are set to `None`
        :param vertex: node to add
        :param prev_node: previous node
        :param next_node: next node
        """
        self._value = value
        self.prev = prev_node
        self.next = next_node

    @property
    def value(self) -> T:
        """
        Returns the value of the node
        :return: the value of the node
        """
        return self._value

    def __str__(self):
        """
        Returns a string representation of the node
        """
        return str(self._value)


class DoubleLinkedList(object):
    def __init__(self):
        """
        Initializes a double linked list

        The head and tail are set to `None` and the size of the list is 0.
        """
        self._head = None
        self._tail = None
        self._size = 0

    def append_left(self, val: T):
        """
        Adds a value at the start of the DoubleLinkedList

        Creates a new node with the given value. This node is set as the head of the DoubleLinkedList. If the list was
        empty, also the tail is set to this node. If there was already a head of the list, the current head gets the
        added node as previous node, and the added node gets the previous head as next node.
        Afterward, the size of the list is increased by one.
        :param val: value of the node to add
        """
        new_node = Node(val)
        if self._size == 0:
            self._head = new_node
            self._tail = new_node
        else:
            self._head.prev = new_node
            new_node.next = self._head
            self._head = new_node
        self._size += 1

    def append(self, val: T):
        """
        Adds a value at the end of the DoubleLinkedList

        Creates a new node with the given value. This node is set as the tail of the DoubleLinkedList. If the list was
        empty, also the head is set to this node. If there was already a tail of the list, the current tail gets the
        added node as next node, and the added node gets the previous tail as previous node.
        Afterward, the size of the list is increased by one.
        :param val: value of the node to add
        """
        new_node = Node(val)
        if self._size == 0:
            self._head = self._tail = new_node
        else:
            self._tail.next = new_node
            new_node.prev = self._tail
            self._tail = new_node
        self._size += 1

    def pop(self) -> T:
        """
        Removes and returns the tail of the list

        If the list has more than one node, the tail is removed and the previous node of the tail is set as the new
        tail. This new tail now has no next node. If the list has one element, the head and tail are set to `None`. And
        if the list is empty, the list is not adapted and `None` is returned.
        Finally, the size of the list is decreased by one.
        :return: the value of the tail of the list
        """
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
        """
        Removes and returns the head of the list

        If the list has more than one node, the head is removed and the next node of the head is set as the new head.
        This new head now has no previous node. If the list has one element, the head and tail are set to `None`. And
        if the list is empty, the list is not adapted and `None` is returned.
        Finally, the size of the list is decreased by one.
        :return: the value of the head of the list
        """
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

    def insert_after(self, node: Node, val: T):
        """
        Inserts a value after another node

        Creates a new node with the given value. The new node has the _node_ as previous node and the next node of
        _node_ is set as the next node of the added node. If _node_ is the tail of the list, the tail is set to the new
        node and the new node has no next node.
        Afterwards, the size of the list is increased by one.
        :param node: node after which the new value must be added
        :param val: value to add to the list
        """
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

    def insert_before(self, node: Node, val: T):
        """
        Inserts a value before another node

        Creates a new node with the given value. The new node has the _node_ as next node and the previous node of
        _node_ is set as the previous node of the added node. If _node_ is the head of the list, the head is set to the
        new node and the new node has no previous node.
        Afterwards, the size of the list is increased by one.
        :param node: node before which the new value must be added
        :param val: value to add to the list
        """
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

    def remove(self, value: T):
        """
        Removes the first occurrence of a node with the given value from the list

        Removes the first occurrence of the given value from the list. If no node with the value can be found, no node
        is removed.
        :param value: the value to remove from the list
        """
        node = self._head
        while node is not None:
            if node.value == value:
                self.delete(node)
                return
            node = node.next

    def delete(self, node: Node) -> T:
        """
        Deletes the given node from the list and returns it's value

        Deletes the given node from the list. The node before of the deleted node has now the next node of the deleted
        node as next node. And the node after the deleted node now has the previous node of the deleted node as previous
        node.
        If the deleted node is the head, the head is set to the next node of the deleted node.
        If the deleted node is the tail, the tail is set to the previous node of the deleted node.
        Afterwards, the size of the list is decreased by one.
        If the node cannot be found, the list is not changed.
        :param node: node to delete
        :return: the value of the deleted node, `None` if the node could not be found
        """
        if node.value not in self:
            return None

        prev_node, next_node = node.prev, node.next
        if prev_node is not None:
            prev_node.next = next_node
        if next_node is not None:
            next_node.prev = prev_node

        if node == self._head:
            self._head = next_node
        if node == self._tail:
            self._tail = prev_node
        node.next = None
        node.prev = None
        self._size -= 1
        return node.value

    def find(self, value: T) -> Node:
        """
        Returns the first occurrence of a node with the given value

        Returns the first occurrence of the given value. If no node with the value is found, `None` is returned.
        :param value: value to find in the list
        :return: the node with the given value, `None` if the value could not be found
        """
        node = self._head
        while node is not None:
            if node.value == value:
                return node
            node = node.next
        return None

    def __len__(self) -> int:
        """
        Returns the length of the list

        :return: number of nodes in the list
        """
        return self._size

    def __str__(self):
        """
        Returns a string representation of the list
        """
        txt = "["
        node = self._head
        while node is not None:
            txt += str(node) + ','
            node = node.next
        txt = txt[:-1] + ']'
        return txt

    def __iter__(self):
        """
        Returns an iterator for the values of the nodes in the list
        """
        node = self._head
        while node:
            yield node
            node = node.next

    def __reversed__(self):
        """
        Returns a reversed iterator for the values of the nodes in the list
        """
        node = self._tail
        while node:
            yield node.value
            node = node.prev

    def __contains__(self, item: T) -> bool:
        """
        Returns whether a value is in the list

        :param item: value to find in the list
        :return: `True` if a node with the given value is in the list, `False` otherwise
        """
        return (self.find(item) is not None);


if __name__ == '__main__':
    from graph import Vertex, Graph

    g = Graph(False)
    v = [Vertex(g) for i in range(5)]
    n = Node(v[0])
    lst = DoubleLinkedList()
    lst.append([0])
    lst.append_left(v[1])
    lst.append(v[2])
    print(type(lst))

    for u in lst:
        print(u)
    print(lst)

    lst2 = DoubleLinkedList()
    lst2.append(1)
    lst2.append(2)
    lst2.append(2)
    lst2.append_left(3)
    print(lst2)
