'''
This file implements the AVL Tree data structure.
The functions in this file are considerably harder than the
functions in the BinaryTree and BST files,
but there are fewer of them.
'''

from containers.BinaryTree import BinaryTree, Node
from containers.BST import BST


class AVLTree(BST):
    '''
    FIXME:
    AVLTree is currently not a subclass of BST.
    You should make the necessary changes in the class declaration line above
    and in the constructor below.
    '''

    def __init__(self, xs=None):
        '''
        FIXME:
        Implement this function.
        '''
        super().__init__()
        self.xs = xs
        self.insert_list(xs)

    def balance_factor(self):
        '''
        Returns the balance factor of a tree.
        '''
        return AVLTree._balance_factor(self.root)

    @staticmethod
    def _balance_factor(node):
        '''
        Returns the balance factor of a node.
        '''
        if node is None:
            return 0
        return BinaryTree._height(node.left) - BinaryTree._height(node.right)

    def is_avl_satisfied(self):
        '''
        Returns True if the avl tree satisfies that all nodes
        have a balance factor in [-1,0,1].
        '''
        if self.root:
            return AVLTree._is_avl_satisfied(self.root)
        else:
            return True

    @staticmethod
    def _is_avl_satisfied(node):
        '''
        FIXME:
        Implement this function.
        '''
        ret = True
        acceptable = [-1, 0, 1]
        if node:
            if AVLTree._balance_factor(node) not in acceptable:
                return False
        if node.left:
            if AVLTree._balance_factor(node.left) in acceptable:
                ret &= AVLTree._is_avl_satisfied(node.left)
            else:
                ret = False
        if node.right:
            if AVLTree._balance_factor(node.right) in acceptable:
                ret &= AVLTree._is_avl_satisfied(node.right)
            else:
                ret = False

        return ret

    @staticmethod
    def _copy_nodes(node):
        if node:
            cop = Node(node.value, AVLTree._copy_nodes(node.left),
                       AVLTree._copy_nodes(node.right))
        else:
            return None
        return cop

    @staticmethod
    def _left_rotate(node):
        '''
        FIXME:
        Implement this function.

        The lecture videos provide a high-level overview of tree rotations,
        and the textbook provides full python code.
        The textbook's class hierarchy for their AVL tree code is
        fairly different from our class hierarchy,
        however, so you will have to adapt their code.
        '''
        nodecopy = AVLTree._copy_nodes(node)
        newroot = nodecopy.right
        transfer = newroot.left
        newroot.left = nodecopy
        nodecopy.right = transfer
        return newroot

    @staticmethod
    def _right_rotate(node):
        '''
        FIXME:
        Implement this function.

        The lecture videos provide a high-level overview of tree rotations,
        and the textbook provides full python code.
        The textbook's class hierarchy for their AVL tree
        code is fairly different from our class hierarchy,
        however, so you will have to adapt their code.
        '''
        nodecopy = AVLTree._copy_nodes(node)
        newroot = nodecopy.left
        transfer = newroot.right
        newroot.right = nodecopy
        nodecopy.left = transfer
        return newroot

    def insert(self, value):
        '''
        FIXME:
        Implement this function.

        The lecture videos provide a high-level overview of
        how to insert into an AVL tree, and the textbook provides
        full python code.
        The textbook's class hierarchy for their AVL tree code
        is fairly different from our class hierarchy,
        however, so you will have to adapt their code.

        HINT:
        It is okay to add @staticmethod helper functions for this code.
        The code should look very similar to the code for your insert
        function for the BST,
        but it will also call the left and right rebalancing functions.
        '''
        if self.root:
            AVLTree._insert(value, self.root)
            rebal = AVLTree._rebalance(self.root)
            self.root = rebal
        else:
            self.root = Node(value)

    def insert_list(self, xs):
        '''
        Given a list xs, insert each element of xs into self.

        FIXME:
        Implement this function.

        HINT:
        Repeatedly call the insert method.
        You cannot get this method to work correctly until
        you have gotten insert to work correctly.
        '''
        if xs:
            for x in xs:
                self.insert(x)

    @staticmethod
    def _insert(value, node):
        if value < node.value:
            if node.left:
                AVLTree._insert(value, node.left)
                rebal = AVLTree._rebalance(node.left)
                node.left = rebal
            else:
                node.left = Node(value)
        if value > node.value:
            if node.right:
                AVLTree._insert(value, node.right)
                rebal = AVLTree._rebalance(node.right)
                node.right = rebal
            else:
                node.right = Node(value)

    @staticmethod
    def _rebalance(node):
        '''
        There are no test cases for the rebalance function,
        so you do not technically have to implement it.
        But both the insert function needs the rebalancing code,
        so I recommend including that code here.
        '''
        if AVLTree._balance_factor(node) < -1:
            if AVLTree._balance_factor(node.right) > 1:
                rightrot = AVLTree._right_rotate(node.right)
                node.right = rightrot
                leftrot = AVLTree._left_rotate(node)
                node = leftrot
            else:
                leftrot = AVLTree._left_rotate(node)
                node = leftrot
            return node
        elif AVLTree._balance_factor(node) > 1:
            if AVLTree._balance_factor(node.left) < -1:
                leftrot = AVLTree._left_rotate(node.left)
                node.left = leftrot
                rightrot = AVLTree._right_rotate(node)
                node = rightrot
            else:
                rightrot = AVLTree._right_rotate(node)
                node = rightrot
            return node
        else:
            return node
