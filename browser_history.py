# Design a browser history system that supports:

# 	•	visit(url) — visit a new page. If you’d navigated back and then visit a new URL, it should discard the “forward” history (like a real browser)
# 	•	back(steps) — move back up to steps pages, return the current URL after moving
# 	•	forward(steps) — move forward up to steps pages, return the current URL after moving
# 	•	get_current() — return current URL

# Then extend it with a twist that’s closer to what you’ll actually get asked in an interview:

# Follow-up: Support multiple named tabs, where each tab has its own independent history, but tabs can be “cloned” — clone_tab(source_tab, new_tab) creates a new tab whose history starts as a copy of the source tab’s history up to the current position (not including any forward history).

# Constraints to keep you honest:

# 	•	All operations should be O(steps) or better, not O(n) full-list rebuilds
# 	•	Think about whether cloning should deep-copy nodes or whether structure sharing is safe (this is where the “stale field” and “cross-container pointer leakage” bugs from your last sessions tend to resurface)

# Give yourself 45 minutes. Want me to hold off and just check in at the end, or run/verify code with you as you go like last time?

class Visit:

    def __init__(self, url, id):
        self.prev = None
        self.next = None
        self.url = url
        self.id = id

class browser_history:

    def __init__(self):
        self.head = None
        self.tail = None


class tab:

    def __init__(self, id):
        self.id = id
        self.history = browser_history()
        self.current_visit_id = None
        self.id_to_visit = {}
        self.count = 0

class tab_list:

    def __init__(self):
        self.id_to_tab = {}
        self.count = 0


    def new_tab(self):
        count = self.count
        new_id = count+1

        # create new tab object
        new_tab = tab(new_id)

        # add new tab to the collection
        self.id_to_tab[new_id] = new_tab

        # update the counter for tabs 
        self.count+=1   

        return new_id

    def clone_tab(self, source_tab_id):

        source_tab = self.id_to_tab[source_tab_id]

        # create new tab
        new_tab_id = self.new_tab()
        new_tab = self.id_to_tab[new_tab_id]


        head = source_tab.history.head
        curr = head 

        while curr:
            # create new node

            visit = Visit(curr.url, new_tab.count + 1) # # 1->

            if  new_tab.history.tail is None:
                visit.next = None
                visit.prev = None
                new_tab.history.tail = visit
                new_tab.history.head = visit

            else:
                # append new node to new tab
                new_tab.history.tail.next = visit
                visit.next = None
                visit.prev = new_tab.history.tail
                new_tab.history.tail = visit

                # update tab id counter
            new_tab.count+=1
            new_tab.id_to_visit[visit.id] = visit

            if curr.id == source_tab.current_visit_id:
                break

            curr = curr.next

        # copy the new tab back into the list of tabs

        self.id_to_tab[new_tab.id] = new_tab



    def get_number_of_tabs(self):

        return len(self.id_to_tab)


    # def clone_tab(self, tab_id):

    def visit(self, url, tab_id):

        # get current tab first

        tab = self.id_to_tab[tab_id]

        visit_id = tab.count + 1

        tab.count+=1
        new_node = None
        # if browser history is empty bc it's a new tab
        if tab.history.tail is None:
            new_node = Visit(url, visit_id)
            new_node.next = None
            new_node.prev = None
            tab.history.head = new_node
            tab.history.tail = new_node

        # there already is browserhistory
        else:
            new_node = Visit(url, visit_id)
            tab.history.tail.next = new_node
            new_node.next = None
            new_node.prev = tab.history.tail
            tab.history.tail = new_node
        
        tab.current_visit_id = visit_id
        tab.id_to_visit[visit_id] = new_node

        self.id_to_tab[tab_id] = tab

    def forward(self, tab_id, moves: int):
        tab = self.id_to_tab[tab_id]
        print(" current visit: ", tab.current_visit_id)
        curr_visit_id = tab.current_visit_id
        visit = tab.id_to_visit[curr_visit_id]

        while visit and moves > 0:

            visit = visit.next
            moves-=1

        tab.current_visit_id = visit.id

        self.id_to_tab[tab_id] = tab


    
    def backwards(self, tab_id, moves: int):
        tab = self.id_to_tab[tab_id]

        curr_visit_id = tab.current_visit_id
        visit = tab.id_to_visit[curr_visit_id]

        while visit and moves > 0:

            visit = visit.prev
            moves -=1

        tab.current_visit_id = visit.id

        self.id_to_tab[tab_id] = tab



    def get_current(self, tab_id):

        # get current tab

        tab = self.id_to_tab[tab_id]
        visit_id = tab.current_visit_id

        visit = tab.id_to_visit[visit_id]
        print("url: ", visit.url)

        return visit.url

    def get_history(self, tab_id):

        tab = self.id_to_tab[tab_id]

        curr = tab.history.head

        while curr:
            print("curr: ", curr.url)
            curr = curr.next






test = tab_list()
test.new_tab()
test.new_tab()
test.new_tab()


num_tabs = test.get_number_of_tabs()
print("num tabs: ", num_tabs)

test.visit("google.com", 2)
test.visit("amazon.com", 2)
test.visit("netflix.com", 2)

# test.get_history(2)

current = test.get_current(2)

print("current visit: ", current)

test.backwards(2, 1)

current = test.get_current(2)


test.forward(2, 1)

current = test.get_current(2)

test.backwards(2, 2)
current = test.get_current(2)

test.visit("atlassian.com", 3)

curr3 = test.get_current(3)
print("curr3: ", curr3)

test.visit("booking.com", 3)
test.visit("airbnb.com", 1)
test.visit("coinbase.com", 1)

test.clone_tab(1)

print("cloned history")
test.get_history(4)

test.visit("expedia.com", 4)
print("4 again: ")
test.get_history(4)

print("making sure tab 1 didn't change: ")
test.get_history(1)




# test.backwards(3, 1)

# print("curr tab 1: ", test.get_current(1))
# print("curr tab 3: ", test.get_current(3))

# test.forward(3, 1)

# print("curr tab 1: ", test.get_current(3))








# got to everything except for clone in 50 minutes. I realized that i needed a seperate pointer for tracking the current so that i can go forward or backward from the current point and not only from the head or the tail. Since you can't go forward from the tail and can't go backwards from the head. So i spent a little time restructuring the class. I probably spent the most time on the restructuing and then implementing and testing forward and backward. and bugs where i wasn't tracking and setting current_visit_id consistently

# then it took me another 24 mins to add this clone logic