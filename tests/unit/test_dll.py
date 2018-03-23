"""
Test file for Doubly Linked Lists
"""
import unittest
from dll import DoubleLinkedList, Node


class DoublyLinkedListCase(unittest.TestCase):
    dll = None

    def setUp(self):
        self.dll = DoubleLinkedList()

    def test_init(self):
        self.assertEqual(self.dll._head, None, "Initial HEAD should be None")
        self.assertEqual(self.dll._tail, None, "Initial TAIL should be None")
        self.assertEqual(len(self.dll), 0, "Initial length should be zero")

    def test_append_left(self):
        self.dll.append_left(1)
        self.assertEqual(self.dll._head.value, 1, "Expected value 1 in first Node")
        self.assertEqual(len(self.dll), 1, "Length should be 1")
        self.assertEqual(self.dll._head, self.dll._tail, "HEAD should equal TAIL")

        prev_added_node = self.dll._head
        count = 1
        for i in range(5):
            self.dll.append_left(i)
            count += 1

            self.assertEqual(self.dll._head.value, i, "Expected value " + str(i) + " in first Node")
            self.assertEqual(self.dll._head.next.value, prev_added_node.value, "Expected value" + str(prev_added_node.value) + "in next Node")
            self.assertEqual(len(self.dll), count, "Length should be " + str(count))
            self.assertEqual(self.dll._head.next, prev_added_node, "First node should point to second node")
            self.assertEqual(prev_added_node.prev, self.dll._head, "Second node should point to this node")
            prev_added_node = self.dll._head

    def test_append(self):
        self.dll.append(1)
        self.assertEqual(self.dll._head.value, 1, "Expected value 1 in first Node")
        self.assertEqual(len(self.dll), 1, "Length should be 1")
        self.assertEqual(self.dll._head, self.dll._tail, "HEAD should equal TAIL")

        prev_added_node = self.dll._tail
        count = 1
        for i in range(5):
            self.dll.append(i)
            count += 1

            self.assertEqual(self.dll._tail.value, i, "Expected value " + str(i) + " in last Node")
            self.assertEqual(self.dll._tail.prev.value, prev_added_node.value,
                             "Expected value" + str(prev_added_node.value) + "in previous Node")
            self.assertEqual(len(self.dll), count, "Length should be " + str(count))
            self.assertEqual(self.dll._tail.prev, prev_added_node, "Added node should point to second last node")
            self.assertEqual(prev_added_node.next, self.dll._tail, "Second Last node should point to added node")
            prev_added_node = self.dll._tail

    def test_pop(self):
        count = 5
        for i in range(count):
            self.dll.append(i)

        self.assertEqual(len(self.dll), count, "Length should be " + str(count))

        # Pop from a dll with > 1 elements
        for i in range(count,1, -1):
            value = self.dll.pop()
            count -= 1

            self.assertEqual(len(self.dll), count, "Length should be " + str(count))
            self.assertEqual(value, i - 1, "Value should equal " + str(i - 1))
            self.assertIsNone(self.dll._tail.next, "TAIL.next should be None")

        # Pop from a dll with 1 element
        self.assertEqual(len(self.dll), count, "Length should be " + str(1))
        value = self.dll.pop()

        self.assertEqual(len(self.dll), 0, "Length should be " + str(0))
        self.assertEqual(value, 0, "Value should equal " + str(0))
        self.assertIsNone(self.dll._head, "HEAD should be None")
        self.assertIsNone(self.dll._tail, "TAIL should be None")

        # Pop from an empty dll
        node = self.dll.pop()
        self.assertIsNone(node, "Popping an empty dll returns None")

    def test_pop_left(self):
        n = count = 5
        for i in range(count):
            self.dll.append(i)

        self.assertEqual(len(self.dll), count, "Length should be " + str(count))

        # Pop_left from a dll with > 1 elements
        for i in range(count - 1):
            value = self.dll.pop_left()
            count -= 1

            self.assertEqual(len(self.dll), count, "Length should be " + str(count))
            self.assertEqual(value, i, "Value should equal " + str(i))
            self.assertEqual(self.dll._head.value, i + 1, "Next value should equal " + str(i + 1))

        # Pop from a dll with 1 element
        self.assertEqual(len(self.dll), count, "Length should be " + str(1))
        value = self.dll.pop_left()

        self.assertEqual(len(self.dll), 0, "Length should be " + str(0))
        self.assertEqual(value, n - 1, "Value should equal " + str(n - 1))
        self.assertIsNone(self.dll._head, "HEAD should be None")
        self.assertIsNone(self.dll._tail, "TAIL should be None")

        # Pop from an empty dll
        node = self.dll.pop_left()
        self.assertIsNone(node, "Popping an empty dll returns None")

    def test_find(self):
        n = 5
        for i in range(n):
            self.dll.append(i)

        self.assertEqual(self.dll.find(3).value, 3, "Can find value of 3")
        self.assertIsNone(self.dll.find(10), "Cannot find a node with a value of 10")

    def test_insert_after(self):
        n, m = 5, 3
        node = None
        for i in range(n):
            self.dll.append(i)

        node = self.dll.find(m)
        node2 = node.next
        self.dll.insert_after(node, 10)
        self.assertEqual(node.next.value, 10, "Value of 10 is inserted after given node")
        self.assertEqual(node2.prev, node.next, "New node is inserted before 'node2")

        expected = [i for i in range(n)]
        expected.insert(m+1, 10)
        count = 0
        for i in self.dll:
            self.assertEqual(i, expected[count])
            count += 1

        # Insert after TAIL
        self.dll.insert_after(self.dll._tail, 11)
        self.assertEqual(self.dll._tail.value, 11, "Value of 11 is inserted at TAIL")
        self.assertIsNone(self.dll._tail.next, "HEAD.next is None")

    def test_insert_before(self):
        n, m = 5, 3
        node = None
        for i in range(n):
            self.dll.append(i)

        node = self.dll.find(m)
        node2 = node.prev
        self.dll.insert_before(node, 10)
        self.assertEqual(node.prev.value, 10, "Value of 10 is inserted before 'node'")
        self.assertEqual(node2.next, node.prev, "New node is inserted after 'node2")

        expected = [i for i in range(n)]
        expected.insert(m-1, 10)
        count = 0
        for i in self.dll:
            self.assertEqual(i, expected[count])
            count += 1

        # Insert before HEAD
        self.dll.insert_before(self.dll._head, 11)
        self.assertEqual(self.dll._head.value, 11, "Value of 11 is inserted at HEAD")
        self.assertIsNone(self.dll._head.prev, "HEAD.prev is None")

    def test_delete(self):
        n = 5
        for i in range(n):
            self.dll.append(i)

        # Delete existing value
        self.dll.delete(2)
        self.assertEqual(len(self.dll), n - 1, "Length should be " + str(n - 1))
        self.assertIsNone(self.dll.find(2), "There should be no value of 2 in the dll")

        # Delete non existing value
        self.dll.delete(-1)
        self.assertEqual(len(self.dll), n - 1, "Length should still be" + str(n - 1))

    def test_remove(self):
        n = 5
        for i in range(n):
            self.dll.append(i)

        # Delete existing value
        node = self.dll.find(2)
        prev = node.prev
        next = node.next
        self.dll.delete(node)
        self.assertEqual(len(self.dll), n - 1, "Length should be " + str(n - 1))
        self.assertIsNone(self.dll.find(2), "There should be no value of 2 in the dll")
        self.assertEqual(prev.next, next.prev, "Links previous and next nodes")

        # Delete non existing value
        node = Node(4)
        self.dll.delete(node)
        self.assertEqual(len(self.dll), n - 1, "Length should still be" + str(n - 1))


if __name__ == '__main__':
    unittest.main()