from datetime import datetime

#
# You're building the backend for a room-booking tool. Requests come in as (start_time, end_time) pairs (integers, e.g. minutes since midnight). You need to support:

# book(start, end) — insert a new booking. Reject (return False) if it overlaps any existing booking; otherwise insert and return True.
# cancel(start) — remove the booking that starts at this time.
# next_available(after_time) — given a time, return the start time of the next booking that begins at or after it (or None if none exists).
# Constraints to build toward:

# Bookings should stay sorted by start time internally.
# No two bookings can overlap — this is the tricky part of book(), since you need to check the neighbors (the booking right before and right after your insertion point), not just do a duplicate-key check.
# Aim for O(log n) for all three operations against a balanced tree.
# Structure:

# Use a BST keyed by start_time, where each node also stores end_time.
# Implement your own Node class with left/right/parent pointers (no library shortcuts) — that's the point of practicing it raw.
# for this problem are we assuming that there are multiple rooms or are we managing bookings for 1 room?

class TreeNode:

    def __init__(self, id: int, start_time: datetime, end_time: datetime):
        self.left = None
        self.right = None
        self.id = id
        self.start_time = start_time
        self.end_time = end_time


class booking:

    def __init__(self):
        self.root = None
        self.count = 0

    def add_booking(self, start_time: datetime, end_time: datetime):

        # we know there is a violation if end_time >= root.start_time and start_time < root.end_time
        # 1:30 -2pm
        # 10-11 am, 11:30-12:30, 1-2pm, 3-5pm

        try:

            conflict =  self.is_conflict(start_time, end_time, self.root)
            if conflict:
                
                raise ValueError("there is a meeting conflict")

            
            else:
                self.root = self.insert(self.root, start_time, end_time)
                self.count+=1
    

        except ValueError as error:
            print("Error: ", error)

            
    def is_conflict(self, start_time: datetime, end_time: datetime, root):
        if root is None:
            return False

        if end_time >= root.start_time and start_time < root.end_time:
            return True

        if start_time < root.start_time:
            root = self.is_conflict(start_time, end_time, root.left)

        else:
            root = self.is_conflict(start_time, end_time, root.right)

        return root

    
    def insert(self, root, start_time, end_time):

        if root is None:
            return TreeNode(self.count+1, start_time, end_time)

        
        if start_time < root.start_time:
            root.left = self.insert(root.left, start_time, end_time)
        
        else:
            root.right = self.insert(root.right, start_time, end_time)

        
        return root

    def cancel_booking(self, start_time):

        self.root = self.cancel(self.root, start_time)

    def cancel(self, root, start_time):
        # print("root time: ", root.start_time)
        if root is None:
            return None

        if start_time < root.start_time:
            root.left = self.cancel(root.left, start_time)

        elif start_time > root.start_time:
            root.right = self.cancel(root.right, start_time)

        else:
            print("hello there")
            root = self.remove_booking(root, start_time)

        return root

    def remove_booking(self, root, start_time):

        if root.left is None and root.right is None:
            return None

        if root.left is None and root.right:
            print("hi")
            return root.right

        elif root.left and root.right is None:
            print("hello")
            return root.left

        else:
            print("i'm here")
            new_node = root.right
            while new_node.left:
                new_node = new_node.left

            root.id = new_node.id
            root.start_time = new_node.start_time
            root.end_time = new_node.end_time

            root.right = self.cancel(root.right, new_node.start_time)

        return root

    
    def next_booking(self, root, start_time):

        # find next booked node
        try:
            next_available = self.search(self.root, None, start_time)

            if next_available is None:

                raise ValueError("there is no slot after ", start_time)

            else:
                print("next available is : ", next_available.start_time)

        except ValueError as error:
            print(error)


    def search(self, root, possible_next, start_time): # 10, 10:30, 11:30, 1:30, looking for next at 11:23

    #               10:30
    #           /          \
    #          10           11:30
    #                           \ 
    #                           130pm
    #
    #
    #

        if root is None:
            return possible_next

        # if it's greater it could be the next node, but we also need to check if there are any left children first
        if start_time > root.start_time:

            root = self.search(root.right, possible_next, start_time)


        # If it's less than the node we keep searching right
        else:
            root = self.search(root.left, root, start_time) #None

        return root

        







        


    def get_bookings(self, root):

        if root is None:
            return

        root.left = self.get_bookings(root.left)

        print("id: ", root.id, " start: ", root.start_time, " end: ", root.end_time)
        root.right = self.get_bookings(root.right)


    # def cancel(self)

    # def next_available(self):


test = booking()
test.add_booking(datetime(2026, 1, 4, 8, 12), datetime(2026, 1, 4, 9, 40))
test.add_booking(datetime(2026, 1, 9, 10, 12), datetime(2026, 1, 9, 10, 30))
test.add_booking(datetime(2026, 1, 2, 10, 12), datetime(2026, 1, 3, 10, 30))
# test.add_booking(datetime(2026, 1, 1, 8, 12), datetime(2026, 1, 1, 9, 40))
# test.add_booking(datetime(2026, 1, 9, 11, 20), datetime(2026, 1, 9, 12, 40))


test.next_booking(test.root, datetime(2026, 1, 2, 10, 13))

# test.get_bookings(test.root)

# print("test root time: ", test.root.start_time)

test.cancel_booking(datetime(2026, 1, 4, 8, 12))

test.get_bookings(test.root)








# wasted time debugging why test cases weren't working. figuring out the condition for what causses a conflict took some time as well.
# had minor bugs like wasn't assigning/updating the root after i did the recursion and made updates to the tree. i did the operations but 
# never set it back

# in the remove_booking i was not returning the root.left or the root.right in those conditions i was just setting it to the root