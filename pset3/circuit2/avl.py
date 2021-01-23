#!/usr/bin/env python

import bst

def height(node):
    if node is None:
        return -1
    else:
        return node.height

def gamma(node):
    if node is None:
        return 0
    else:
        return node.gamma

def update_height(node):
    node.height = max(height(node.left), height(node.right)) + 1

def update_gamma(node):
    node.gamma = gamma(node.left) + gamma(node.right) + 1

class AVL(bst.BST):
    """
AVL binary search tree implementation.
Supports insert, delete, find, find_min, next_larger each in O(lg n) time.
"""
    def left_rotate(self, x):
        y = x.right
        y.parent = x.parent
        if y.parent is None:
            self.root = y
        else:
            if y.parent.left is x:
                y.parent.left = y
            elif y.parent.right is x:
                y.parent.right = y
        x.right = y.left
        if x.right is not None:
            x.right.parent = x
        y.left = x
        x.parent = y
        update_height(x)
        update_height(y)
        update_gamma(x)
        update_gamma(y)

    def right_rotate(self, x):
        y = x.left
        y.parent = x.parent
        if y.parent is None:
            self.root = y
        else:
            if y.parent.left is x:
                y.parent.left = y
            elif y.parent.right is x:
                y.parent.right = y
        x.left = y.right
        if x.left is not None:
            x.left.parent = x
        y.right = x
        x.parent = y
        update_height(x)
        update_height(y)
        update_gamma(x)
        update_gamma(y)

    def rebalance(self, node):
        while node is not None:
            update_height(node)
            update_gamma(node)
            if height(node.left) >= 2 + height(node.right):
                if height(node.left.left) >= height(node.left.right):
                    self.right_rotate(node)
                else:
                    self.left_rotate(node.left)
                    self.right_rotate(node)
            elif height(node.right) >= 2 + height(node.left):
                if height(node.right.right) >= height(node.right.left):
                    self.left_rotate(node)
                else:
                    self.right_rotate(node.right)
                    self.left_rotate(node)
            node = node.parent

    ## find(k), find_min(), and next_larger(k) inherited from bst.BST

    def insert(self, k):
        """Inserts a node with key k into the subtree rooted at this node.
        This AVL version guarantees the balance property: h = O(lg n).
        
        Args:
            k: The key of the node to be inserted.
        """
        node = super(AVL, self).insert(k)
        self.rebalance(node)

    def delete(self, k):
        """Deletes and returns a node with key k if it exists from the BST.
        This AVL version guarantees the balance property: h = O(lg n).
        
        Args:
            k: The key of the node that we want to delete.
            
        Returns:
            The deleted node with key k.
        """
        node = super(AVL, self).delete(k)
        ## node.parent is actually the old parent of the node,
        ## which is the first potentially out-of-balance node.
        self.rebalance(node.parent)

    def rank(self, k):
        r = 0
        node = self.root
        while node != None:
            if k < node.key:
                node = node.left
            elif k > node.key:
                r += gamma(node.left) + 1
                node = node.right
            else:
                r += gamma(node.left) + 1
                return r
        return r

    def lca(self, l, h):
        node = self.root
        while node != None and (l > node.key or h < node.key):
            if l < node.key:
                node = node.left
            else:
                node = node.right
        return node

    def node_list(self, node, l, h, result):
        if node == None:
            return
        if l <= node.key and node.key <= h:
            result.append(node.key)
        if node.key >= l:
            self.node_list(node.left, l, h, result)
        if node.key <= h:
            self.node_list(node.right, l, h, result)

    def list(self, l, h):
        lca_node = self.lca(l,h)
        result = []
        self.node_list(lca_node, l, h, result)
        return result

def test(args=None):
    bst.test(args, BSTtype=AVL)

def test2(args=None):
    t = AVL()
    t.insert(7)
    t.insert(10)
    t.insert(12)
    t.insert(20)
    t.insert(30)
    t.insert(25)
    t.insert(22)
    t.insert(27)
    
    # print t.rank(7)
    # print t.rank(10)
    # print t.rank(12)
    # print t.rank(20)
    # print t.rank(22)
    # print t.rank(25)
    # print t.rank(27)
    # print t.rank(30)
    # print t.rank(-1)

    print t
    print t.list(11, 26)

if __name__ == '__main__': test()
