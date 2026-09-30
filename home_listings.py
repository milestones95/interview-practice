class Home:

    def __init__(self, id: int, price: float):
        self.left = None
        self.right = None
        self.id = id
        self.price = price

class HomeListings:

    def __init__(self):
        self.root = None
        self.id_to_home = {}
        self.total_homes = 0

    
    def add_home(self, price):

        id = self.total_homes + 1

        new_home = Home(id, price)
        
        self.root = self.insert_node(self.root, new_home)
        self.total_homes+=1

    def insert_node(self, root, node_to_insert):

        if root is None:
            self.id_to_home[node_to_insert.id] = node_to_insert
            return node_to_insert

        if node_to_insert.price < root.price:
            root.left = self.insert_node(root.left, node_to_insert)

        else:
            root.right = self.insert_node(root.right, node_to_insert)


        return root

    def remove_home(self, id):
        home = self.id_to_home[id]
        price = home.price

        self.root = self.search(price, self.root)


    def search(self, price, root):
        if root is None:
            return None
        if price < root.price:
            root.left = self.search(price, root.left)

        elif price > root.price:
            root.right = self.search(price, root.right)

        else:
            del self.id_to_home[root.id]
            root = self.remove(root)

        return root

    def remove(self, root):

        if root.left is None and root.right is None:
            return None

        if root.left is None and root.right:
            return root.right

        if root.left and root.right is None:
            return root.left

        # if the house has 2 children

        else:

            # find the successor
            successor = root.right

            # get the smallest home from the right tree

            while successor.left:
                successor = successor.left

            # copy the successor attributes to the root node to replace it
            print("price found: ", successor.price)
            root.id = successor.id
            root.price = successor.price
            self.id_to_home[root.id] = root # need to update the hashmap to track the new position of the successor node now that it's the root

            # now that the root is updated with the successor, we need to delete the old root. make sure to delete the old node

            root.right = self.search(successor.price, root.right)

        return root


    def closest_price(self, price):
        
        closest = self.find_closest(self.root, price)

        return closest.price


    def find_closest(self, root, price):
        if root is None:
            return None

        if root.price == price:
            return root


        if price < root.price:
            found = self.find_closest(root.left, price)

        else:
            found = self.find_closest(root.right, price)


        if found is None:
            return root

        else:

            found_diff = abs(found.price - price)
            if found_diff < abs(root.price - price):
                return found

            return root


    def count_in_range(self, root, low, high):

        if root is None:
            return 0

        if root.price < low:
            return self.count_in_range(root.right, low, high)

        if root.price > high:
            return self.count_in_range(root.left, low, high)

        else:
            return self.count_in_range(root.left, low, high) + self.count_in_range(root.right, low, high) + 1



    def get_next_expensive(self, root, price, possible_next): #price = 21 , possible next: None, 27
        if root is None: #F,F
            return None

        # if root.price == price:
        #     return None

        if price < root.price: # T
            found = self.get_next_expensive(root.left, price, root) # 27

            if found is None:
                return root

            else:
                return found


        else: #T

            found = self.get_next_expensive(root.right, price, possible_next) # node: 21, possible next = 27

            if found is None:
                return possible_next

            else:
                return found



    #                27
#                  /.  \
#                 16    38
#                /  \      \
#               7.  21       45
#                           /   \
#                          41    48  
        



    def print_nodes(self, root):

        if root is None:
            return

        self.print_nodes(root.left)
        print("price: ", root.price)
        self.print_nodes(root.right)


    


test = HomeListings()

test.add_home(800)
test.add_home(600)
test.add_home(900)
test.add_home(700)
test.add_home(500)
test.add_home(550)
test.add_home(300)




# test.remove_home(1)

test.print_nodes(test.root)
closest = test.closest_price(788)

print("closest: ", closest)

in_range = test.count_in_range(test.root, 0, 500)

print("in range: ", in_range)

# finished insert and delete node. stumbled on delete took a bit of debugging...26 mins so far
# finished get closest by 34 mark
# finished in range by 41 min mark
# finished the next expensive at the 1 hr and 9 min mark

next_expensive = test.get_next_expensive(test.root, 710, None)

print("next expensive: ", next_expensive.price)