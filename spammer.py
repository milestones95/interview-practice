# 10:12 am, 10:15am, 10:30am, 10:45am, 11am, 1145am 
# new event: 10:50 , W = 30 mins, N = 4
from datetime import datetime, timedelta

class TreeNode:
    def __init__(self, timestamp: datetime):
        self.right = None
        self.left = None
        self.left_size = 0
        self.timestamp = timestamp
class user_spammers:

    def __init__(self, W: int, N: int):
        self.events = {}
        self.spammers = set()
        self.N = N
        self.W = W

    
    def new_request(self, timestamp: datetime, user_id: str):

        user_node = self.events.get(user_id, None)

        if self.count_nodes_in_window(user_node, timestamp) + 1 >self.N:
            self.spammers.add(user_id)

        else:
            ## insert new node

            self.events[user_id] = self.insert_node(user_node, timestamp)


    def count_nodes_in_window(self, root, timestamp):

        if root is None:
            return 0

        timestamp_min = timestamp - self.W

        
        return self.count(root, timestamp) - self.count(root, timestamp_min)

    def count(self, root, timestamp: datetime):

        count = 0

        while root is not None:
            if root.timestamp <= timestamp:
                count += root.left_size + 1
                root = root.right
            
            else:
                root = root.left

        return count

    def insert_node(self, root, timestamp: datetime):

        if root is None:
            return TreeNode(timestamp)
        if timestamp >= root.timestamp:
            root.right = self.insert_node(root.right, timestamp)

        else:
            root.left_size +=1
            root.left = self.insert_node(root.left, timestamp)

        return root

        

    
    def get_unique_spammers(self):
        return len(self.spammers)



test = user_spammers(timedelta(minutes=30), 5)
test.new_request(datetime(2026, 1, 1, 10, 12), "alice")
test.new_request(datetime(2026, 1, 1, 10, 11), "alice")
test.new_request(datetime(2026, 1, 1, 10, 13), "alice")
test.new_request(datetime(2026, 1, 1, 10, 14), "alice")
test.new_request(datetime(2026, 1, 1, 10, 15), "alice")
test.new_request(datetime(2026, 1, 1, 10, 56), "alice")

print('spammers: ', test.get_unique_spammers())

