from iterators import ArrayIterator, MatrixIterator, BinaryTreeIterator, TreeNode

print("=== ARRAY ===")
arr = (1, 2, 3, 4)
it = ArrayIterator(arr)
while it.has_next():
    print(it.next())

print("\n=== MATRIX ===")
m = [[1,2,3],[4,5],[6,7,8]]
it = MatrixIterator(m)
while it.has_next():
    print(it.next())

print("\n=== BINARY TREE ===")
root = TreeNode(5, TreeNode(3, TreeNode(2), TreeNode(4)), TreeNode(8, None, TreeNode(9)))
it = BinaryTreeIterator(root)
while it.has_next():
    print(it.next())
