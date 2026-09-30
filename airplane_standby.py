# Problem: Airline Standby List

# Passengers are on standby, ranked by a priority score (higher boards first). Implement StandbyList:

# add_passenger(passenger_id, priority) — Insert into a BST keyed by priority. Assume priorities are unique for now (explicit scope call — flag it, don't build tie-breaking).
# remove_passenger(passenger_id) — Remove by ID (hashmap id → priority, then BST delete by priority, same shape as your real estate deletion).
# get_highest_priority() — Return the passenger with the max priority (boards next). Pure search, no mutation — should be a one-liner walk to the rightmost node.
# get_kth_highest(k) — Return the passenger with the k-th highest priority (k=1 is the same as get_highest_priority). This is the new part: to do this in O(height) instead of O(n), each node needs to track the size of its own subtree, and you use that count to decide whether the answer is in the left subtree, the right subtree, or is the current node itself.
# count_between(low, high) — Count of passengers with low <= priority <= high. Same pruning pattern as your real estate count_in_range.

# Return the passenger with the k-th highest priority (k=1 is the same as get_highest_priority).
# if user A is 3, user b is 2, user c is 1 and user d is 4, we should return user 3 for k = 3
#                       5
#                   /       \
#                  3          8
#               /    \
#              1        4
# 3 right subtree is 1 size
# left subtree is two so we know 3 is k = 3
# we need to track the left subtree
# if we wanted to know if for 4 we'd take the left subtree + 1 for root and then go right. it has no left so zero, and no right +1 so it is 4th

class TreeNode:

    def __init__(self, priority, p_id):
        self.left = None
        self.right = None
        self.priority = priority
        self.passenger_id = p_id
        self.left_subtree_size = 0



class Passengers:

    def __init__(self):
        self.root = None
        self.count = 0
        self.id_to_passenger = {}


    def traverse(self, root):

        if root is None:
            return

        self.traverse(root.left)
        print("passenger id: " , root.passenger_id, " priority: ", root.priority)
        self.traverse(root.right)


    def add_passenger(self, priority):
        new_id = self.count+1

        # make sure to return the new root and assign to self.root !!!

        self.root = self.insert_node(priority, new_id, self.root)
        self.count+=1


    
    def insert_node(self, priority, id, root):

        if root is None:
            new_node = TreeNode(priority, id)
            self.id_to_passenger[id] = new_node

            return new_node

        if priority < root.priority:
            # if it's less than the root priority, that means we will insert into the left subtree. Must increment count
            root.left_subtree_size+=1
            root.left = self.insert_node(priority, id, root.left)

        else:
            root.right = self.insert_node(priority, id, root.right)

        return root



    def delete_passenger(self, passenger_id):

        passenger = self.id_to_passenger[passenger_id]
        priority = passenger.priority

        self.root = self.find_passenger_to_delete(self.root, priority)


    def find_passenger_to_delete(self, root, priority):

        if root is None:
            return None

        if priority < root.priority:
            root.left_subtree_size-=1 # make sure we decrement the left subtree size since we know we're remove a node from it's left subtree
            root.left = self.find_passenger_to_delete(root.left, priority)

        elif priority > root.priority:
            root.right = self.find_passenger_to_delete(root.right, priority)

        else:
            del self.id_to_passenger[root.passenger_id]
            root = self.delete_node(root)

        
        return root


    def delete_node(self, root):
        
        if root.left is None and root.right is None:
            return None

        if root.left is None and root.right:
            return root.right

        if root.left and root.right is None:
            return root.left


        # has both children
        else:
            # get the successor

            successor = root.right

            while successor.left:
                successor = successor.left

            
            root.passenger_id = successor.passenger_id
            root.priority = successor.priority

            root.right = self.find_passenger_to_delete(root.right, successor.priority)
            self.id_to_passenger[root.passenger_id] = root


        return root
            

    def get_highest_priority(self):   
        passenger = self.find_highest(self.root)

        return passenger.priority


    def find_highest(self, root):

        # we need to find the smallest priority and return it if we can't go left anymore that's the smallest
        if root is None: #5,3,1,None
            return None

        found = self.find_highest(root.left) # None,1,1

        # we should never go right

        if found: #F,T
            return found #1,1,1

        else: #T 
            return root #1
# for deleting  node 3       
#                       5 # this left subtree will go from size 4 to size 3
#                   /       \
#                  3  ->1    8 -> doesn't change
#               /    \
# no change-> 1        4 # this left subtree size needs to get updated
#                      /
#                    3.5 should take the root's left subtree. right subtree size isn't tracked so doesn't need to change

    def get_kth_highest(self, k):
        

        highest = self.find_kth_highest(self.root, k, 0)
        return highest


    def find_kth_highest(self, root, k, counted_nodes):

        if root is None: # 3
            return None

        total = counted_nodes + root.left_subtree_size + 1
        if total == k:
            return root

        if k < total:
            found = self.find_kth_highest(root.left, k, counted_nodes)

        else:
            found = self.find_kth_highest(root.right, k, total)


        if found:
            return found
        return root


    def count_in_range(self, low, high):
        nums = []
        self.find_in_range(low, high, self.root, nums)

        return nums


    def find_in_range(self, low, high, root, nums):
        if root is None: #6,3,2
            return

        if root.priority < low:
            self.find_in_range(low, high, root.right, nums)

        elif root.priority > high:
            self.find_in_range(low, high, root.left, nums) #T

        else:
            nums.append(root.priority) #3,4

            self.find_in_range(low, high, root.left, nums)
            self.find_in_range(low, high, root.right, nums)

        return 
# range 3-5
#                           6
#                         /.   \
#                       3       14
#                      /  \       
#                     2    4

        

test = Passengers()

test.add_passenger(6)
test.add_passenger(3)
test.add_passenger(2)
test.add_passenger(4)
test.add_passenger(14)

test.traverse(test.root)

test.delete_passenger(1)

# print("---------------------")
# test.traverse(test.root)

highest_pri = test.get_highest_priority()

print("highest prio: ", highest_pri)

kth = test.get_kth_highest(3)
print("kth prio: ", kth.priority)

# finished insert at 20 mins
# finished deleting passenger at 30
# finished highest priority at 40
# finished kth at 1hr 1 min.

in_range = test.count_in_range(10,20)
print("in range: ", in_range)
