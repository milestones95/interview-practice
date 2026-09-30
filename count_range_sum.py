"""

Problem: Count Range Sum in a User Database

You're building an internal analytics tool for an e-commerce site. Customer records are stored in a Binary Search Tree, keyed by total_spent (lifetime purchase amount). Marketing wants to run a query: "How many customers have spent between $500 and $2000?"

This needs to run frequently (every time someone adjusts the filter sliders on a dashboard), so a full O(n) scan of all customers is too slow at scale.

Task: Write a function countInRange(root, low, high) that returns the count of nodes whose value falls within [low, high], inclusive — and does it efficiently by pruning subtrees that can't possibly contain valid values (using the BST property instead of visiting every node)."""

# 09/03/2026
# had a bug where i wasn't traversing also left if the node was in range. my test cases didn't hit this bug so i didn't realize it. I forgot to traverse both directions for this condition.

class TreeNode:
    def __init__(self, spent):
        self.left =None
        self.right = None
        self.spent = spent


class customer_records:

    def __init__(self):
        self.root = None

    def insert_record(self, spent):
        
        self.root = self.insert_node(self.root, spent)


    def insert_node(self, root, spent):

        if root is None:
            return TreeNode(spent)

        if spent < root.spent:
            root.left = self.insert_node(root.left, spent)

        else:
            root.right = self.insert_node(root.right, spent)

        return root


def count_in_range(root, low, high):


    return count_in_range_helper(root, low, high)


def count_in_range_helper(root, low, high):

    if root is None:
        return 0

    if root.spent < low:
        found = count_in_range_helper(root.right, low, high)        

    elif root.spent > high:
        found = count_in_range_helper(root.left, low, high)

    else:
        found = count_in_range_helper(root.right, low, high) + count_in_range_helper(root.left, low, high) + 1

    return found


test = customer_records()
test.insert_record(100)
test.insert_record(350)
test.insert_record(700)

count = count_in_range(test.root, 100, 400)

print("count: ", count)

    