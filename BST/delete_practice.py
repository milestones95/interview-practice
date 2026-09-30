class TreeNode:

    def __init__(self, val):
        self.left = None
        self.right = None
        self.val = val


class BST:

    def __init__(self):
        self.root = None

    def insert(self, val):

        self.root = self.insert_node(self.root, val)


    def insert_node(self, root, val):
        if root is None:
            return TreeNode(val)

        if val > root.val:
            root.right = self.insert_node(root.right, val)

        else:
            root.left = self.insert_node(root.left, val)

        return root

    
    def get_values(self):

        self.traverse(self.root)

    def traverse(self, root):

        if root is None:
            return

        self.traverse(root.left)
        print("val: ", root.val)

        self.traverse(root.right)


    def delete(self, val):
        self.root = self.find_node(self.root, val)


    def find_node(self, root, val):

        if root is None:
            return None

        if val < root.val:
            root.left = self.find_node(root.left, val)

        elif val > root.val:
            root.right = self.find_node(root.right, val)

        else:
            print("found it: ", root.val)
            root = self.delete_node(root, val)

        return root


    def delete_node(self, root, val):
        
        if root.left is None and root.right is None:
            return None


        # if there is only a right child and no left child, then we will make the right child the new root
        if root.right and root.left is None:
            return root.right

        # if there is only a left child and no right child, then we will make the left child the new root

        if root.left and root.right is None:
            return root.left

        # the root we're deleting has both a left and right child. So we need to take the smallest node that is greater than the current root
        else:
            # first get the smallest node that's greater than root
            successor = root.right

            while successor.left:
                successor = successor.left

            # we aren't actually going to move this successor, we will instead copy over it's data to the current root. that's easier

            root.val = successor.val

            # now that we've updated the current root to now have the new successor value, we need to delete the old successor value. 
            # we will make sure we delete the old successor by passing the root.right tree into self.find_node()

            root.right = self.find_node(root.right, successor.val)

        
        # don't forget to return the new updated root.

        return root

            


        


test = BST()
test.insert(8)
test.insert(9)
test.insert(30)
test.insert(23)
test.insert(17)
test.insert(35)
test.insert(3)
test.insert(2)
test.insert(4)




test.get_values()

# test.delete(17)
# test.delete(30)
# test.delete(35)
# test.delete(9)
test.delete(3)



print("---------------------")
test.get_values()
