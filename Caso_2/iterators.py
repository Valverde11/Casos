from abc import ABC, abstractmethod

class Iterator(ABC):
    @abstractmethod
    def has_next(self):
        pass

    @abstractmethod
    def next(self):
        pass

class ArrayIterator(Iterator):
    def __init__(self, arr):
        self.arr = arr
        self.index = 0

    def has_next(self):
        return self.index < len(self.arr)

    def next(self):
        val = self.arr[self.index]
        self.index += 1
        return val

class MatrixIterator(Iterator):
    def __init__(self, matrix):
        self.matrix = matrix
        self.row = 0
        self.col = 0

    def has_next(self):
        return self.row < len(self.matrix) and self.col < len(self.matrix[self.row])

    def next(self):
        value = self.matrix[self.row][self.col]
        self.col += 1
        if self.col == len(self.matrix[self.row]):
            self.row += 1
            self.col = 0
        return value

class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

class BinaryTreeIterator(Iterator):
    def __init__(self, root):
        self.stack = []
        self._push_left(root)

    def _push_left(self, node):
        while node:
            self.stack.append(node)
            node = node.left

    def has_next(self):
        return len(self.stack) > 0

    def next(self):
        node = self.stack.pop()
        val = node.value
        if node.right:
            self._push_left(node.right)
        return val
