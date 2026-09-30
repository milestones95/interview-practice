# this is to practice problems where we'd need to exit a recursive function early and return the result

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

    def LCA(self, val1, val2): 
        
        lca = self.find_lca(self.root, val1, val2)

        return lca.val

    def find_lca(self, root, val1, val2): #16, 45

        if root is None:
            return

        # we need to check if the given root has both values as children
        # we need to also consider that the LCA could be val1 or val2 
        found = self.isFound(root, val1) and self.isFound(root, val2)

        if not found:
            return

        # if the node has both val1 and val2 we need to check to see if the left child also has both values and do the same for the right

        result = self.find_lca(root.left, val1, val2)

        if result:
            return result

        result = self.find_lca(root.right, val1, val2)

        if result:
            return result

        return root


    
    def isFound(self, root, val):

        if root is None:
            return False

        if root.val == val:
            return True
        
        found = False
        if val < root.val:
            found = self.isFound(root.left, val)


        else:
            found = self.isFound(root.right, val)

        return found


    def isFoundRewrite(self, root, val1, val2):

        if root is None:
            return

        found = None
        if val1 < root.val and val2 < root.val:
            found = self.isFoundRewrite(root.left, val1, val2)

        elif val1 > root.val and val2 > root.val:
            found = self.isFoundRewrite(root.right, val1, val2)

        else:
            found = root

        return found


    def closest_value(self, val):
        closest = self.find_closest(self.root, val)

        return closest.val


    def find_closest(self, root, val): # find 40

        if root is None: #27,38,45
            return 

        if root.val == val:
            return root

        found = None 

        if val < root.val:
            found = self.find_closest(root.left, val) #T # None

        else: #T,T
            found = self.find_closest(root.right, val)

        if found is None:
            return root

        else:
            found_diff = abs(found.val - val) #13,2,5

            if found_diff < abs(root.val - val):
                return found

            return root

        
#                    27
#                  /.  \
#                 16    38
#                /  \      \
#               7.  21       45
#                           /   \
#                          41    48  
        


    
test = BST()
test.insert(9)
test.insert(8)
test.insert(4)
test.insert(3)
test.insert(34)
test.insert(23)

lca = test.LCA(9,34)

# print("lca: ", lca)

rewrite = test.isFoundRewrite(test.root, 9,34)
# print(" rewrite lca: ", rewrite.val)

closest = test.closest_value(9)

print(" closest: ", closest)


# 20 mins but there's a bug i found
# 31 to finish the entire thing for finding the closest