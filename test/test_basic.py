import unittest


from gcb_tree.basic import BasicTree as Tree
from gcb_tree.basic import Root, Node, Leaf, EmptyNode


class BasicTreeTestSuite(unittest.TestCase):
    """ Basic test cases. """

    N = 16
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


    def test_add(self):
        tree = self.tree
        data = 'Data'
        tree.add(5, data)

        tree.add(10, data)
        self.assertEqual(tree.root.child.big_child.value, 10)

        with self.assertRaises(ValueError):
            tree.add(self.N + 1, data)
            tree.add(-1, data)

    def test_get(self):
        tree = self.tree
        data = 'Test_data'
        tree.add(5, data)
        self.assertEqual(tree.get(5), data)
        with self.assertRaises(LookupError):
            tree.get(6)
            tree.get(-1)
            tree.get(self.N + 1)


if __name__ == '__main__':
    unittest.main()