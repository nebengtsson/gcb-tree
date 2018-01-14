import unittest


from gcb_tree.basic import BasicTree as Tree
from gcb_tree.basic import Root, Node, Leaf, EmptyNode

class BasicTreeTestSuite(unittest.TestCase):
    """ Basic test cases. """

    N = 16
    data = 'data'

    def print_content(self):
        pass

    def setUp(self):
        self.tree = Tree(self.N)

    def test_tree_init(self):
        self.assertIsInstance(self.tree.root.child, EmptyNode)

    def test_add_first_value(self):
        tree = self.tree
        value = 5
        data = {'sum': 10}
        tree.add(value, data)
        self.assertEqual(tree.root.child.value, value)

    def set_up_from_list(self, values):
        tree = Tree(self.N)
        for value in values:
            tree.add(value, self.data)
        return tree

    def test_node_range(self):
        tree = self.set_up_from_list([0, 15])
        self.assertEqual(tree.root.child.range_small, 0)
        self.assertEqual(tree.root.child.range_big, 15)

        tree = self.set_up_from_list([7, 8])
        self.assertEqual(tree.root.child.range_small, 0)
        self.assertEqual(tree.root.child.range_big, 15)

        tree = self.set_up_from_list([3, 7])
        self.assertEqual(tree.root.child.range_small, 0)
        self.assertEqual(tree.root.child.range_big, 7)

        tree = self.set_up_from_list([2, 3])
        self.assertEqual(tree.root.child.range_small, 2)
        self.assertEqual(tree.root.child.range_big, 3)


    def test_add(self):
        tree = self.tree
        data = 'Data'
        tree.add(5, data)

        tree.add(10, data)
        self.assertEqual(tree.root.child.big_child.value, 10)
        # Add same twice
        tree.add(10, data)
        self.assertEqual(tree.root.child.big_child.value, 10)

        with self.assertRaises(ValueError):
            tree.add(self.N + 1, data)
            tree.add(-1, data)

    def test_add_meny(self):
        tree = self.tree
        data = 'Data'
        tree.add(5, data)
        tree.add(4, data)
        tree.add(1, data)
        tree.add(16, data)
        tree.add(7, data)

    def test_get(self):
        tree = self.tree
        data = 'Test_data'
        tree.add(5, 'a')
        tree.add(4, 'b')
        tree.add(1, 'c')
        self.assertEqual(tree.get(5), 'a')
        with self.assertRaises(LookupError):
            tree.get(6)  # not in tree
        with self.assertRaises(LookupError):
            tree.get(-1)  # To small value
        with self.assertRaises(LookupError):
            tree.get(self.N + 1)  # To large value

    def test_remove(self):
        tree = self.tree
        tree.add(2, self.data)
        tree.add(3, self.data)
        tree.remove(3)
        self.assertEqual(tree.root.child.value, 2)

        tree.add(5, self.data)
        tree.add(6, self.data)
        with self.assertRaises(LookupError):
            tree.remove(7)  # not in tree
        with self.assertRaises(LookupError):
            tree.remove(-1)  # To small value
        with self.assertRaises(LookupError):
            tree.remove(self.N + 1)  # To large value

    def test_remove_last(self):
        tree = self.tree
        tree.add(3, self.data)
        tree.remove(3)
        self.assertIsInstance(self.tree.root.child, EmptyNode)

    def test_pop(self):
        tree = self.tree
        tree.add(3, 'a')
        tree.add(8, 'b')
        tree.add(5, 'c')
        self.assertEqual(tree.pop(8), 'b')
        self.assertEqual(tree.pop(5), 'c')
        self.assertEqual(tree.pop(3), 'a')
        self.assertIsInstance(self.tree.root.child, EmptyNode)


if __name__ == '__main__':
    unittest.main()