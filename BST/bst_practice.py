class TreeNode:

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


class BST:
    
    def __init__(self):
        self.root = None


    def search(self, root, value_to_search):

        if root is None:
            return False


        if value_to_search > root.val:
            return self.search(root.right, value_to_search)

        elif value_to_search < root.val:
            return self.search(root.left, value_to_search) 

        else:
            return True


    def insert(self, value_to_insert):

        self.root = self.insert_node(self.root, value_to_insert)


    
    def insert_node(self, root, value_to_insert):

        if root is None:
            return TreeNode(value_to_insert)

        
        if value_to_insert > root.val:
            root.right = self.insert_node(root.right, value_to_insert)

        else:
            root.left = self.insert_node(root.left, value_to_insert)

        return root

    def find_min(self):

        root = self.min_helper(self.root)

        return root.val

    def min_helper(self, root):

        if root.left is None:
            return root

        root = self.min_helper(root.left)

        return root

    def get_values(self):

        self.traverse(self.root)

    def traverse(self, root):

        if root is None:
            return

        self.traverse(root.left)
        print("val: ", root.val)

        self.traverse(root.right)




# took 20 mins to write
test = BST()

test.insert(77)
test.insert(87)
test.insert(43)
test.insert(23)
test.insert(37)
test.insert(12)


test.get_values()

searchFor = 88
isFound = test.search(test.root, searchFor)

print("found {searchFor}: ", isFound)

found_min = test.find_min()

print("min: ", found_min)

