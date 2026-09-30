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


    def get_count(self):

        count = self.count_nodes(self.root)

        return count


    def count_nodes(self, root):

        if root is None:
            return 0

        return self.count_nodes(root.left) + self.count_nodes(root.right) + 1


    def count_greater_than(self, root, val): #26

        if root is None:
            return 0

        if root.val > val:
            return self.count_greater_than(root.left, val) + self.count_greater_than(root.right, val) +1

        else:
            return self.count_greater_than(root.right, val)


    def count_height(self, root):

        if root is None:
            return 0

        return max(self.count_height(root.left) +1 , self.count_height(root.right) +1)

    # count the # of nodes within a given range inclusive of the low and high points
    def count_in_range(self, root, low, high):

        count = self.count_range_helper(root, low, high)

        return count

    def count_range_helper(self, root, low, high): #30-40
        # if the root is none, there ther'es no need to check the right or left subtree to get their counts. it's already empty
        if root is None:
            return 0

        if root.val < low:
            return self.count_range_helper(root.right, low, high)

        elif root.val > high:
            return self.count_range_helper(root.left, low, high)

        else:
            return self.count_range_helper(root.left, low, high) + self.count_range_helper(root.right, low, high) + 1

        #            27
#                  /.  \
#                 16    38
#                /  \      \
#               7.  21       45
#                           /   \
#                          41    48  
    








test = BST()
test.insert(9)
test.insert(17)
test.insert(6)
test.insert(7)
test.insert(14)
test.insert(23)
test.insert(25)


count = test.get_count()

count_greater = test.count_greater_than(test.root, 8)

print("count greater: ", count_greater)

height = test.count_height(test.root)

print("height: ", height)


count_range = test.count_in_range(test.root, 0,12)

print("count_range: ", count_range)




        


# wrote count_nodes method in 6 minutes. I started with just 1 node to see if the correct number would be returned from it's left and right subtree. With 1 node, it's left subtree should return zero and so should it's right subtree. So then i just need to add +1 to include the root node. and then i tried it with two nodes and the function still worked

# finished greater than!! seems like it works based on my test cases 