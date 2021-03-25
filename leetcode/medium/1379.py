# Find a Corresponding Node of a Binary Tree in a Clone of That Tree

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    def getTargetCopy(self, original: TreeNode, cloned: TreeNode, target: TreeNode) -> TreeNode:
        def adjustTargetPath(node: TreeNode):
            if target == node:
                return True
            targetPath.append(False)  # left
            if node is not None and adjustTargetPath(node.left):
                return True
            targetPath[-1] = True  # right
            if node is not None and adjustTargetPath(node.right):
                return True
            targetPath.pop()

        targetPath: list[bool] = []
        adjustTargetPath(original)
        for direction in targetPath:
            cloned = cloned.right if direction else cloned.left
        return cloned
