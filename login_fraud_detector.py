from datetime import datetime,timedelta 


class TreeNode:
    
    def __init__(self, timestamp: datetime):
        self.left = None
        self.right = None
        self.timestamp = timestamp
        self.left_size = 0

class FraudDetector:

    def __init__(self, w: datetime, n: int):
        self.N = n
        self.W = w
        self.logins = {}
        self.suspicious_users = set()
    # we need to make sure a user isn't logging in too frequently or we will believe they are suspicious.
    # we have a time window
    # we have a number of times they can log in before it gets flagged
    # we need to track the time stamp of each login
    # get the suspicious users
    # answer if a given user is suspicious
    # we need a hashmap with each ip address (basically a user id)
    # we want to search faster than o(n) so we can use a bst

    def login(self, timestamp: datetime, user: str):
        user_node = self.logins.get(user, None)

        beginning = timestamp - self.W
        found = self.count_times_less_than_timestamp(user_node, timestamp) - self.count_times_less_than_timestamp(user_node, beginning) +1
        print("found: ", found)
        if found > self.N:
            self.suspicious_users.add(user)


        new_node = self.insert_login(user_node, timestamp)
        self.logins[user] = new_node

    def insert_login(self, root, timestamp: datetime):
        if root is None:
            return TreeNode(timestamp)

        
        if timestamp >= root.timestamp:
            root.right = self.insert_login(root.right, timestamp)
        else:
            root.left_size+=1
            root.left = self.insert_login(root.left, timestamp)

        return root


    def count_times_less_than_timestamp(self, root, timestamp):

        count = 0

        while root is not None:
            if timestamp > root.timestamp:
                count+= root.left_size +1
                root = root.right
            else:
                root = root.left

        print("count: ", count)

        return count

    def get_suspicious_users(self):
        return len(self.suspicious_users)





test = FraudDetector(timedelta(minutes=30), 5)
test.login(datetime(2026, 1, 1, 10, 12), "alice")
test.login(datetime(2026, 1, 1, 10, 11), "alice")
test.login(datetime(2026, 1, 1, 10, 13), "alice")
test.login(datetime(2026, 1, 1, 10, 14), "alice")
test.login(datetime(2026, 1, 1, 10, 15), "alice")
# test.login(datetime(2026, 1, 1, 10, 16), "alice")
test.login(datetime(2026, 1, 1, 10, 13), "jim")
test.login(datetime(2026, 1, 1, 10, 14), "jim")
test.login(datetime(2026, 1, 1, 10, 15), "jim")
test.login(datetime(2026, 1, 1, 10, 16), "jim")
print("suspicious users: ", test.get_suspicious_users())