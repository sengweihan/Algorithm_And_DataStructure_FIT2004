# import random, math

outputdebug = False


def debug(msg):
    if outputdebug:
        print(msg)


class Node():
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class AVLTree():
    def __init__(self, *args):
        self.node = None
        self.height = -1
        self.balance = 0

        if len(args) == 1:
            for i in args[0]:
                self.insert(i)

    def height(self):
        if self.node:
            return self.node.height
        else:
            return 0

    def is_leaf(self):
        return (self.height == 0)

    def insert(self, key):
        tree = self.node

        newnode = Node(key)

        if tree == None:
            self.node = newnode
            self.node.left = AVLTree()
            self.node.right = AVLTree()
            debug("Inserted key [" + str(key) + "]")

        elif key < tree.key:
            self.node.left.insert(key)

        elif key > tree.key:
            self.node.right.insert(key)

        else:
            debug("Key [" + str(key) + "] already in tree.")

        self.rebalance()

    def rebalance(self):
        '''
        Rebalance a particular (sub)tree
        '''
        # key inserted. Let's check if we're balanced
        self.update_heights(False)
        self.update_balances(False)
        while self.balance < -1 or self.balance > 1:
            if self.balance > 1:
                if self.node.left.balance < 0:
                    self.node.left.lrotate()  # we're in case II
                    self.update_heights()
                    self.update_balances()
                self.rrotate()
                self.update_heights()
                self.update_balances()

            if self.balance < -1:
                if self.node.right.balance > 0:
                    self.node.right.rrotate()  # we're in case III
                    self.update_heights()
                    self.update_balances()
                self.lrotate()
                self.update_heights()
                self.update_balances()

    def rrotate(self):
        # Rotate left pivoting on self
        debug('Rotating ' + str(self.node.key) + ' right')
        A = self.node
        B = self.node.left.node
        T = B.right.node

        self.node = B
        B.right.node = A
        A.left.node = T

    def lrotate(self):
        # Rotate left pivoting on self
        debug('Rotating ' + str(self.node.key) + ' left')
        A = self.node
        B = self.node.right.node
        T = B.left.node

        self.node = B
        B.left.node = A
        A.right.node = T

    def update_heights(self, recurse=True):
        if not self.node == None:
            if recurse:
                if self.node.left != None:
                    self.node.left.update_heights()
                if self.node.right != None:
                    self.node.right.update_heights()

            self.height = max(self.node.left.height,
                              self.node.right.height) + 1
        else:
            self.height = -1

    def update_balances(self, recurse=True):
        if not self.node == None:
            if recurse:
                if self.node.left != None:
                    self.node.left.update_balances()
                if self.node.right != None:
                    self.node.right.update_balances()

            self.balance = self.node.left.height - self.node.right.height
        else:
            self.balance = 0

    def delete(self, key):
        # debug("Trying to delete at node: " + str(self.node.key))
        if self.node != None:
            if self.node.key == key:
                debug("Deleting ... " + str(key))
                if self.node.left.node == None and self.node.right.node == None:
                    self.node = None  # leaves can be killed at will
                # if only one subtree, take that
                elif self.node.left.node == None:
                    self.node = self.node.right.node
                elif self.node.right.node == None:
                    self.node = self.node.left.node

                # worst-case: both children present. Find logical successor
                else:
                    replacement = self.logical_successor(self.node)
                    if replacement != None:  # sanity check
                        debug("Found replacement for " + str(key) +
                              " -> " + str(replacement.key))
                        self.node.key = replacement.key

                        # replaced. Now delete the key from right child
                        self.node.right.delete(replacement.key)

                self.rebalance()
                return
            elif key < self.node.key:
                self.node.left.delete(key)
            elif key > self.node.key:
                self.node.right.delete(key)

            self.rebalance()
        else:
            return

    def logical_predecessor(self, node):
        '''
        Find the biggest valued node in LEFT child
        '''
        node = node.left.node
        if node != None:
            while node.right != None:
                if node.right.node == None:
                    return node
                else:
                    node = node.right.node
        return node

    def logical_successor(self, node):
        '''
        Find the smallese valued node in RIGHT child
        '''
        node = node.right.node
        if node != None:  # just a sanity check

            while node.left != None:
                debug("LS: traversing: " + str(node.key))
                if node.left.node == None:
                    return node
                else:
                    node = node.left.node
        return node

    def check_balanced(self):
        if self == None or self.node == None:
            return True

        # We always need to make sure we are balanced
        self.update_heights()
        self.update_balances()
        return ((abs(self.balance) < 2) and self.node.left.check_balanced() and self.node.right.check_balanced())

    def inorder_traverse(self):
        if self.node == None:
            return []

        inlist = []
        l = self.node.left.inorder_traverse()
        for i in l:
            inlist.append(i)

        inlist.append(self.node.key)

        l = self.node.right.inorder_traverse()
        for i in l:
            inlist.append(i)

        return inlist

    def display(self, level=0, pref=''):
        '''
        Display the whole tree. Uses recursive def.
        TODO: create a better display using breadth-first search
        '''
        self.update_heights()  # Must update heights before balances
        self.update_balances()
        if(self.node != None):
            print('-' * level * 2, pref, self.node.key, "[" + str(self.height) + ":" + str(
                self.balance) + "]", 'L' if self.is_leaf() else ' ')
            if self.node.left != None:
                self.node.left.display(level + 1, '<')
            if self.node.left != None:
                self.node.right.display(level + 1, '>')

    def uncorrupted_merge(self, other, corrupted):
        """
        ARGUMENTS : THIS FUNCTION TAKES IN 3 ARGUMENTS. OTHER IS AN INSTANCE OF AVLTREE AND SELF IS ALSO AN INSTANCE OF AVLTREE.
        CORRUPTED IS A LIST OF KEYS . EVERY ITEM IN CORRUPTED APPEARS IN OTHER.THE NUMBER OF ITEMS IN CORRUPTED IS MUCH SMALLER 
        THAN THE NUMBER OF ITEMS IN OTHER AND SELF.

        OUTPUT : THIS FUNCTION WILL MODIFIES THE SELF SO THAT IT CONTAINS ALL THE ELEMENTS IT ORIGINALLY CONTAINED AS WELL AS
        ALL THE ELEMENTS IN OTHER WHICH ARE NOT CORRUPTED. AT THE END , IT MUST STILL BE A VALID AVL TREE.

        """

        # self represents t2  and other represents t1

        # we first obtained the node of the smaller tree by calling inorder_traverse function.
        sorted_t1 = other.inorder_traverse()  # O(M)

        if len(sorted_t1) > 0:
            # now we will do conditionally checking to determine the root based on the length of the node in t1.
            # we will used the rightmost node in the smaller tree as the new root node.
            root = sorted_t1[len(sorted_t1)-1]  # O(1)
            # once we have determine the root, we will remove the root from the tree by calling the delete method .
            other.delete(root)  # O (log M)
        else:
            return

        # since we knew that the tree other is smaller than the tree self. Hence, we can create a new tree
        new_tree = AVLTree()  # O(1)
        # with the root being determine previously and merge both trees together.
        new_tree.insert(root)  # O(1) since there's only one element

        # O(1) # assign the smaller tree as being the left subtree from the node
        new_tree.node.left.node = other.node
        # O(1) # assign the bigger tree as being the right subtree from the node
        new_tree.node.right.node = self.node
        # Once both left and right subtree is inserted, we need to maintain the balance of the new AVL tree.
        # O(log N) where N = number of nodes in the new_tree created.
        new_tree.rebalance()

        # Once the tree is merged, we can now remove the corrupted item from the Tree by calling delete method.
        # O(k log N) where N = N + M (total number of node combined in both AVL trees) , k = number of corrupted nodes.
        for item in corrupted:
            new_tree.delete(item)

        # lasly we assigned the self to be the new_tree # O(1)
        self.node = new_tree.node


# Usage example
if __name__ == "__main__":
    pass
    # a = AVLTree()
    # print("----- Inserting -------")
    # #inlist = [5, 2, 12, -4, 3, 21, 19, 25]
    # inlist = [7, 5, 2, 6, 3, 4, 1, 8, 9, 0]
    # for i in inlist:
    #     a.insert(i)

    # a.display()

    # print("----- Deleting -------")
    # a.delete(3)
    # a.delete(4)
    # # a.delete(5)
    # a.display()

    # print()
    # print("Input            :", inlist)
    # print("deleting ...       ", 3)
    # print("deleting ...       ", 4)
    # print("Inorder traversal:", a.inorder_traverse())

    # t1 = AVLTree()
    # t2 = AVLTree()

    # lst2 = [1000, 1001, 1002]
    # lst1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, -23, -3, -
    #         10, -7, -210, -2338, 123, 11, 12, 131, 14, 13]
    # corrupted = []

    # for item in lst1:
    #     t1.insert(item)

    # for item in lst2:
    #     t2.insert(item)

    # t2.uncorrupted_merge(t1, corrupted)
    # print(t2.check_balanced())
