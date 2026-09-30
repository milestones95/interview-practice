class TreeNode:

    def __init__(self, val):
        self.left = None
        self.right = None
        self.val = val
        self.right_tree_size = 0


class BST:

    def __init__(self):
        self.root = None
        self.count = 0

    def insert(self, val):

        self.root = self.insert_node(self.root, val)

    def insert_node(self, root, val):
        # if the root is None then this is the point where we want to insert the new node
        if root is None:
            return TreeNode(val)

        # if our new value is greater, then we should keep searching in the right subtree. every right child must be larger than its root
        if val > root.val:
            root.right_tree_size+=1 # if it's greater then that means we are going to insert somewhere in the right subtree. So the right tree size will increase by one
            root.right = self.insert_node(root.right, val)
        else:
            # if the new val is less than the root, we are going to insert somewhere in the left subtree. We don't need to update right tree size.
            root.left = self.insert_node(root.left, val)

        return root

    def print_nodes(self, root):

        if root is None:
            return

        self.print_nodes(root.left)
        print("val: ", root.val)
        self.print_nodes(root.right)


    def get_rank(self, val):
        return self.search(self.root, val) + 1

    def search(self, root, val): # search for 16

        if root is None:
            return 0

        if val < root.val:
            return self.search(root.left, val) + root.right_tree_size + 1


        elif val > root.val:
            return self.search(root.right, val)

        else:
            return root.right_tree_size
        

    def top_n_scores(self, n):
        new_list = self.reverse_traversal(self.root, n, [])
        print("top {n}: ")
        print(new_list)
    
    def reverse_traversal(self, root, n, top_n):

        if root is None:
            return

        if len(top_n) == n:
            return

        # we don't need to set anything or set the top_n list because we can reference lists
        self.reverse_traversal(root.right, n,top_n)
        if len(top_n) <n:
            top_n.append(root.val)

        else:
            return top_n

        if len(top_n) == n:
            return top_n
        self.reverse_traversal(root.left, n,top_n)

        return top_n

    def kth_largest(self, k):
        self.count = 0

        kth = self.find_kth_largest(self.root, k)

        return kth.val

    def find_kth_largest(self, root, k): #2

        if root is None:
            return

        if self.count == k:
            return

        found = self.find_kth_largest(root.right, k)
        if found:
            return found
        self.count+=1

        if self.count == k:
            return root

        found = self.find_kth_largest(root.left, k)

        if found:
            return found


#                   27
#                  /.  \
#                 16    38
#                /  \      \
#               7.  21       45
#                           /   \
#                          41    48  
# rank of 21

test = BST()
test.insert(65)
test.insert(34)
test.insert(78)
test.insert(98)
test.insert(45)
test.insert(54)
test.insert(12)


test.print_nodes(test.root)

# rank = test.get_rank(65)
# rank = test.get_rank(12)
# rank = test.get_rank(98)
# rank = test.get_rank(78)
rank = test.get_rank(34)



print("rank: ", rank)

test.top_n_scores(5)

kth = test.kth_largest(5)
print("kth: ", kth)