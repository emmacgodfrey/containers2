'''
this file implements the Heap data structure as a subclass of the BinaryTree.
The book implements Heaps using an *implicit* tree with an *explicit* vector
implementation, so the code in the book is likely to be less helpful than
the code for the other data structures. The book's implementation is the
traditional implementation because it has a faster constant factor (but
the same asymptotics).
This homework is using an explicit tree implementation to help you get
more practice with OOP-style programming and classes.
'''

from containers.BinaryTree import BinaryTree, Node
import copy


class Heap(BinaryTree):
    '''
    FIXME:
    Heap is currently not a subclass of BinaryTree.
    You should make the necessary changes in the class declaration line above
    and in the constructor below.
    '''

    def __init__(self, xs=None):
        '''
        FIXME:
        If xs is a list (i.e. xs is not None),
        then each element of xs needs to be inserted into the Heap.
        '''
        super().__init__()
        self.xs = xs
        self.insert_list(xs)

    def __repr__(self):
        '''
        Notice that in the BinaryTree class,
        we defined a __str__ function,
        but not a __repr__ function.
        Recall that the __repr__ function should return a string that
        can be used to recreate a valid instance of the class.
        Thus, if you create a variable using the command Heap([1,2,3])
        it's __repr__ will return "Heap([1,2,3])"

        For the Heap, type(self).__name__ will be the string "Heap",
        but for the AVLTree, this expression will be "AVLTree".
        Using this expression ensures that all subclasses of Heap will have
        a correct implementation of __repr__,
        and that they won't have to reimplement it.
        '''
        return type(self).__name__ + '(' + str(self.to_list('inorder')) + ')'

    def is_heap_satisfied(self):
        '''
        Whenever you implement a data structure,
        the first thing to do is to implement a function that checks whether
        the structure obeys all of its laws.
        This makes it possible to automatically test whether insert/delete
        functions are actually working.
        '''
        if self.root:
            return Heap._is_heap_satisfied(self.root)
        return True

    @staticmethod
    def _is_heap_satisfied(node):
        '''
        FIXME:
        Implement this method.
        '''
        ret = True
        if (not node.left) and (not node.right):
            return True
        if (node.right) and (not node.left):
            return False
        if (not node.right) and (node.left):
            if (node.left.value < node.value):
                return False
        else:
            if (node.right.value >= node.value) and \
               (node.left.value >= node.value):
                ret &= Heap._is_heap_satisfied(node.left)
                ret &= Heap._is_heap_satisfied(node.right)
            else:
                return False
        return ret

    def insert(self, value):
        '''
        Inserts value into the heap.

        FIXME:
        Implement this function.

        HINT:
        The pseudo code is
        1. Find the next position in the tree using the binary representation
        of the total number of nodes
            1. You will have to explicitly store the size of your heap in
            a variable (rather than compute it) to maintain the O(log n)
            runtime
            1. See https://stackoverflow.com/questions/18241192/implement-heap
            -using-a-binary-tree for hints
        1. Add `value` into the next position
        1. Recursively swap value with its parent until the heap property is
        satisfied

        HINT:
        Create a @staticmethod helper function,
        following the same pattern used in the BST and AVLTree insert
        functions.
        '''
        if self.root:
            num_nodes = Heap._count_nodes(self.root)
            binrep = "{0:b}".format(num_nodes + 1)
            lbinrep = [int(x) for x in str(binrep)]
            Heap._insert(value, self.root, lbinrep[1:])
            Heap._trickle_up(value, self.root, lbinrep[1:])
        else:
            self.root = Node(value)

    @staticmethod
    def _insert(value, path, lbinrep):
        if len(lbinrep) == 1:
            if lbinrep[0] == 1:
                path.right = Node(value)
            if lbinrep[0] == 0:
                path.left = Node(value)
        else:
            if lbinrep[0] == 1:
                Heap._insert(value, path.right, lbinrep[1:])
            if lbinrep[0] == 0:
                Heap._insert(value, path.left, lbinrep[1:])

    @staticmethod
    def _trickle_up(value, path, lbinrep):
        if len(lbinrep) > 0:
            if len(lbinrep) == 1:
                if lbinrep[0] == 1:
                    if path.right.value < path.value:
                        temp = copy.copy(path.right.value)
                        path.right.value = path.value
                        path.value = temp
                elif lbinrep[0] == 0:
                    if path.left.value < path.value:
                        temp = copy.copy(path.left.value)
                        path.left.value = path.value
                        path.value = temp
            else:
                if lbinrep[0] == 1:
                    Heap._trickle_up(value, path.right, lbinrep[1:])
                elif lbinrep[0] == 0:
                    Heap._trickle_up(value, path.left, lbinrep[1:])

            Heap._trickle_up(value, path, lbinrep[:-1])

    @staticmethod
    def _count_nodes(root):
        if root is None:
            return 0
        else:
            return (1 + Heap._count_nodes(root.left) + Heap._count_nodes(root.right))

    def insert_list(self, xs):
        '''
        Given a list, insert each element of xs into self.

        FIXME:
        Implement this function.
        '''
        if xs:
            for x in xs:
                self.insert(x)

    def find_smallest(self):
        '''
        Returns the smallest value in the tree.

        FIXME:
        Implement this function.
        '''
        if self.root:
            return self.root.value

    def remove_min(self):
        '''
        Removes the minimum value from the Heap.
        If the heap is empty, it does nothing.

        FIXME:
        Implement this function.

        HINT:
        The pseudocode is
        1. remove the bottom right node from the tree
        2. replace the root node with what was formerly the bottom right
        3. "trickle down" the root node: recursively swap it with its
        largest child until the heap property is satisfied

        HINT:
        I created two @staticmethod helper functions: _remove_bottom_right
        and _trickle.
        It's possible to do it with only a single helper (or no helper at all),
        but I personally found dividing up the code into two made
        the most sense.
        '''
        if self.root:
            path = self.root
            num_nodes = Heap._count_nodes(self.root)
            if num_nodes == 1:
                self.root = None
                return self.root
            binrep = "{0:b}".format(num_nodes)
            lbinrep = [int(x) for x in str(binrep)][1:]
            self.root.value = Heap._remove_bottom_right(path, lbinrep)
            Heap._trickle(self.root)
        else:
            return None

    @staticmethod
    def _remove_bottom_right(path, lbinrep):
        if len(lbinrep) == 1:
            if lbinrep[0] == 1:
                temp = path.right.value
                path.right = None
                return temp
            else:
                temp = path.left.value
                path.left = None
                return temp
        elif len(lbinrep) > 1:
            if lbinrep[0] == 1:
                return Heap._remove_bottom_right(path.right, lbinrep[1:])
            elif lbinrep[0] == 0:
                return Heap._remove_bottom_right(path.left, lbinrep[1:])

    @staticmethod
    def _trickle(node):
        if node.left and node.right:
            if node.left.value <= node.right.value:
                if node.value > node.left.value:
                    temp = copy.copy(node.left.value)
                    node.left.value = node.value
                    node.value = temp
                    Heap._trickle(node.left)
            elif node.right.value < node.left.value:
                if node.value > node.right.value:
                    temp = copy.copy(node.right.value)
                    node.right.value = node.value
                    node.value = temp
                    Heap._trickle(node.right)
        elif node.left:
            if node.value > node.left.value:
                temp = copy.copy(node.left.value)
                node.left.value = node.value
                node.value = temp
        elif node.right:
            if node.value > node.right.value:
                temp = copy.copy(node.right.value)
                node.right.value = node.value
                node.value = temp
