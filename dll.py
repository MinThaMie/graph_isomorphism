class Node(object):

    def __init__(self, vertex, prev, next):
        self.vertex = vertex
        self.prev = prev
        self.next = next


class DoubleLinkedList(object):
    firstNode = None
    lastNode = None

    def insert_after(self, node, new_node):
        new_node.prev = node
        if node.next is None:
            new_node.next = None
            self.lastNode = new_node
        else:
            new_node.next = node.next
            node.next.prev = new_node
        node.next = new_node

    def insert_before(self, node, new_node):
        new_node.next = node
        if node.prev is None:
            new_node.prev = None
            self.firstNode = new_node
        else:
            new_node.prev = node.prev
            node.prev.next = new_node
        node.prev = new_node

    def append(self, node):
        if self.firstNode is None:
            self.firstNode = node
            self.lastNode = node
            node.prev = None
            node.next = None
        else:
            self.insert_after(self.lastNode, node)
