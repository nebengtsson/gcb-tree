import numpy as np


arange = np.arange

def biggest_bit(a):
    return 1 << a.bit_length()-1

def smallest_bit(a):
    return (1 + (a ^ (a-1))) >> 1


def node_range(value):
    sb = smallest_bit(value)
    return (value-sb, value+sb-1)


def find_value_node_value(a,b):
    first_diff = 1 << (a^b).bit_length()-1
    return (a|first_diff) & ~(first_diff-1)


class BasicTree():

    def __init__(self, max_value):
        self.root = Root(max_value)
        self.root.child = EmptyNode(self.root)
        self.max_value = max_value
        self.max_hight = 1 + max_value.bit_length()

    def add(self, value, data):
        leaf = self.root.add(value)
        leaf.data = data

    def get(self, value):
        leaf = self.root.get(value)
        if leaf:
            return leaf.data
        raise LookupError(f'Value not found: {value}.')

    def pop(self, value):
        pass


class EmptyNode():
    def __init__(self, root):
        self.root = root
        pass

    def add(self, value):
        leaf = Leaf(value)
        self.root.child = leaf
        leaf.parent = self.root
        return leaf

    def get(self, value):
        return None

    def pop(self, value):
        pass


class Node():
    __slots__ = [#"type",
                 "value", "child_type",
                 "parent", "big_child", "smal_child",
                 "range_smal", "range_big"]

    def __init__(self, value, child_type, parent, big_child, small_child):
        #self.type = 'node'
        self.value = value
        self.child_type = child_type
        self.parent = parent
        self.big_child = big_child
        self.small_child = small_child

        # Pre-calc node range
        nr = node_range(value)
        self.range_small = nr[0]
        self.range_big = nr[1]

    def add(self, value):
        if self._test_value(value):
            if value < self.value:
                return self.small_child.add(value)
            return self.big_child.add(value)
        else:
            return self.insert_new_node_above(value)

    def get(self, value):
        if value < self.value:
            return self.small_child.get(value)
        return self.big_child.get(value)

    def insert_new_node_above(self, value):
        new_leaf = Leaf(value)
        if value < self.value:
            big_child = self
            small_child = new_leaf
        else:
            big_child = new_leaf
            small_child = self

        new_node = Node(
            find_value_node_value(value, self.value),
            self.child_type,
            self.parent,
            big_child,  # big
            small_child,  # small
        )

        if self.child_type == 'small':
            self.parent.small_child = new_node
        else:
            self.parent.big_child = new_node
        big_child.parent = new_node
        small_child.parent = new_node
        big_child.child_type = 'big'
        small_child.child_type = 'small'

        return new_leaf

    def _test_value(self, value):
        return self.range_small <= value and value <= self.range_big


class Leaf(Node):

    def __init__(self, value, child_type=''):
        #self.type = 'leaf'
        self.parent = None
        self.child_type = child_type
        self.value = value
        self.leaf_obj = None

    def add(self, value):
        if self._test_value(value):
            return self
        return self.insert_new_node_above(value)

    def get(self, value):
        if value == self.value:
            return self
        return None

    def _test_value(self, value):
        return value == self.value

class Root(Node):

    def __init__(self, max_value):
        self.child = None
        self.value = max_value / 2  # This is ambiguis but neede to use Node-functions

        self.range_small = 0
        self.range_big = max_value

    def get(self, value):
        return self.child.get(value)

    def add(self, value):
        if self._test_value(value):
            return self.child.add(value)
        raise ValueError('Value not in Tree-range. ({self.range_small} to {self.range_big})')

    @property
    def small_child(self):
        return self.child

    @small_child.setter
    def small_child(self, node):
        self.child = node

    @property
    def big_child(self):
        return self.child

    @big_child.setter
    def big_child(self, node):
        self.child = node

    def set_root(self, node):
        self.root = node