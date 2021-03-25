# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    def getTargetCopy(self, original: TreeNode, cloned: TreeNode, target: TreeNode):
        def getTargetCopy_(originalNode: TreeNode, clonedNode: TreeNode):
            if originalNode:
                if originalNode is target:
                    self.targetCopy = clonedNode
                    raise
                getTargetCopy_(originalNode.left, clonedNode.left)
                getTargetCopy_(originalNode.right, clonedNode.right)

        try: getTargetCopy_(original, cloned)
        except: return self.targetCopy
