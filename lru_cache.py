# Design a cache that supports:

# 	•	put(key, value, ttl) — insert/update a key with a time-to-live in seconds
# 	•	get(key) — return the value if present and not expired, else None. A successful get should mark the key as most-recently-used
# 	•	evict_expired() — remove all currently-expired entries
# 	•	Capacity limit: when inserting past capacity, evict the least-recently-used non-expired entry first; if all entries are expired, evicting expired ones should free space naturally

# this seems like we could use a bst to make the exict expired faster
from datetime import datetime, timedelta
class TreeNode:

    def __init__(self, key: str, value: str, ttl, timestamp: datetime):
        self.key = key
        self.value = value
        self.ttl = ttl
        self.timestamp = timestamp
        self.left = None
        self.right = None

class cache:

    def __init__(self):
        self.root = None
        self.id_to_node = {}


    def put(self, key: str, value: str, ttl):

        # if the key item doesn't exist yet
        node = None
        
        # update the node
        if key in self.id_to_node:
            node = self.id_to_node[key]

        # insert new node
        else:
            node = TreeNode(key, value, ttl, datetime.now())
            # if self.root is None:
            #     self.root = node
            print("helo")

        self.root = self.insert(node, self.root)
        
        self.id_to_node[key] = node


        # if it exists and we're updating it

    # insert the node in order
    def insert(self, node_to_insert, root):

        if root is None:
            return node_to_insert

        
        if root.ttl + root.timestamp > datetime.now() + node_to_insert.ttl:
            root.left = self.insert(node_to_insert, root.left)
        else:
            root.right = self.insert(node_to_insert, root.right)

        return root

   
    def evict_expired(self, root):
        
        # we know if a node is expired if it's timestamp + ttl < datetime.now()

        if root is None:
            return None
        if root.timetsamp + root.ttl < datetime.now():
            return None

        root.left = self.evict_expired(root.left)
        root.right = self.evict_expired(root.right)

        # looking for items less than 7
        #            6
        #           /  \
        #       4         9
        #      / \    
        #   #3      5

        # if it's greater than a node, it's definitely greater than the left subtree and could also be greater than the right

        




        return

    def inorder_traversal(self, root):

        if root is None:
            return

        self.inorder_traversal(root.left)
        print("root key: ", root.key)
        self.inorder_traversal(root.right)

    def get(self, key):

        if key in self.id_to_node:
            node = self.id_to_node[key]
            return node.value

        else:
            return "key doesn't exist" 





test = cache()

test.put("hello", "world", timedelta(days=30))
test.put("john", "snow", timedelta(days=12))

test.put("michael", "jackson", timedelta(days=23))
# test.put("joi", "smith", timedelta(days=45))

test.inorder_traversal(test.root)

print("get kyle", test.get("kyle"))



# did put and get in the first 44 mins. wasted a lot of time figuring out how to subtract /add the datetime type and timedelta and integers so the errors would go away















# Constraints:

# 	•	get and put must be O(1) (this is the classic doubly-linked-list + hashmap combo you’ve been drilling)
# 	•	You’ll need a way to check expiry without scanning the whole cache on every get — think about whether to check lazily (on access) or maintain a separate structure for evict_expired to be efficient
# 	•	Watch for the same failure mode as your bookmarks problem: nodes needing to be unlinked and relinked (on touch, eviction, and expiry) without leaving stale prev/next pointers

# This one’s good because TTL forces you to reason about two competing orderings (recency vs. expiry time) instead of just one — a step up from a plain LRU cache.

# Want this one after the browser history problem, or would you rather swap the order?