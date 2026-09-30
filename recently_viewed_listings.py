# 08/27/2026
# You're building the "recently viewed listings" feature for a real estate app like Zillow. As a user browses properties, the app needs to support:

# visit(listingId) — user opens a new listing. If they had navigated back and then visit a new one, anything "forward" of their current position should be discarded (like browser history).
# back(steps) — move back up to steps listings in history, return the listingId now being viewed. If you can't go back that far, go as far as possible.
# forward(steps) — same idea but forward. If you can't go forward that far, go as far as possible.

# Assume this needs to support a long session (thousands of listings viewed) efficiently, and visit is called far more often than back/forward.


# My thought process: this is likely a linked list problem. We need to be able to go forwards and backwards easily. Go the the next element. We can track the beginning, end and we need to track current position since theres a forward and backwards. Also allows us to add new visits fast in o(1)

class ListNode:

    # we need to be able to go forwards and backwards so prev and next are needed. And we need to know the listing id as well.
    def __init__(self, id):
        self.prev = None
        self.next = None
        self.id = id


class Listings:

    def __init__(self):
        self.head = None # to track the head of the list
        self.tail = None # to track the tail of the list
        self.current_position = None # this tracks the current position

    def traverse(self):

        curr = self.head

        while curr:
            print(curr.id)

            curr = curr.next


    def visit_listing(self, listing_id):
        # we are always appending to where current position is and we discard everything after the new node

        new_node = ListNode(listing_id)

        # if the list is empty
        if self.tail is None:
            self.tail = new_node
            self.head = new_node
            self.current_position = new_node

        # if the current position is not at the beginning or end
        elif self.current_position:

            prev = self.current_position
            prev.next = new_node
            new_node.prev = prev
            new_node.next = None
            self.current_position = new_node
            self.tail = new_node
        
    def backwards(self, num_steps):

        curr = self.current_position
        if curr is None:
            return

        while curr.prev and num_steps > 0:
            curr = curr.prev
            num_steps-=1

        self.current_position = curr

        return self.current_position


    def forward(self, num_steps):

        curr = self.current_position
        if curr is None:
            return
            

        while curr.next and num_steps > 0:
            curr = curr.next
            num_steps-=1

        self.current_position = curr

        return self.current_position


test = Listings()
test.visit_listing(1)
test.visit_listing(2)
test.visit_listing(3)

# test.visit_listing()
# test.visit_listing()
# test.visit_listing()
# test.visit_listing()



test.traverse()

test.backwards(4)

print("current position: ", test.current_position.id)

test.forward(10)
print("current position: ", test.current_position.id)
test.visit_listing(4)
test.traverse()


# finished in 30 mins