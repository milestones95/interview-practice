"""

Problem: Mutual Connections Suggestion (Twitter "People You May Know")

You're given a directed follow-graph as an adjacency list, where an edge A → B means "A follows B."

python
follows = {
    "alice":   ["bob", "carol"],
    "bob":     ["dave", "erin"],
    "carol":   ["dave"],
    "dave":    ["frank"],
    "erin":    ["frank", "carol"],
    "frank":   []
}

Task: Write a function suggest_follows(graph, user) that returns a list of users user should consider following — accounts that are exactly 2 hops away (a "friend of a friend") but that user doesn't already follow directly, and excluding user themselves.
"""
from collections import deque

def suggest_follows(follows, user, follow_list, visited, count):

    current_follows = follows[user]
    current_follows_set = set()
    for curr in current_follows:
        print("curr: ", curr)
        current_follows_set.add(curr)

    suggest_follows_helper(follows, user, follow_list, visited, current_follows_set, count)

def suggest_follows_helper(follows, user, follow_list, visited, current_follows_set, count):

    # need a base case for when to backtrack

    if count == 0:
        return

    neighbors = follows[user]

    for neighbor in neighbors:
        if neighbor not in visited:
            suggest_follows_helper(follows, neighbor, follow_list, visited, current_follows_set, count-1)
            if neighbor not in current_follows_set:
                follow_list.append(neighbor)
            visited.add(neighbor)



def follows_BFS(follows,user, distance):
    visited = set()
    current_follows = follows[user]
    current_follows_set = set()
    current_follows_set.add(user)
    # for curr_follow in current_follows:
    #     current_follows_set.add(curr_follow)

    new_follows = []
    queue = deque()
    queue.append(user)
    print("current_folows set: ", current_follows_set)
    level = 0
    while len(queue) > 0:
        # print("hi")

        # print("hello")

        for i in range(len(queue)):
            curr = queue.popleft() # alice -> bob
            print("curr: ", curr) # bob
            neighbors = follows[curr] # bob, carol -> dave,erin

            for neighbor in neighbors:# bob, carol -> dave,erin
                if neighbor not in visited: 
                    # print("added")
                    queue.append(neighbor) # bob, carol, -> carol,dave,erin
                    visited.add(neighbor) # # bob, carol -> carol,dave,erin

            if level == distance: #F
                # print("adding")
                new_follows.append(curr)

        level+=1
        print("level: ", level)



        # else:
        #     break

    return new_follows

follows = {
    "alice":   ["bob", "carol"],
    "bob":     ["dave", "erin"],
    "carol":   ["dave"],
    "dave":    ["frank"],
    "erin":    ["frank", "carol"],
    "frank":   []
}

user = "alice"
follow_list = []
visited = set()

# suggest_follows(follows, user, follow_list, visited, 2)
# print("to follow: ", follow_list)

new_follows = follows_BFS(follows, user, 0)
print("new follows: " , new_follows)

# finished in 14 mins. I got the first part even earlier but i needed to figure out how to remove the people the user already follows

# 33 mins to do the BFS i was stuck on a bug where it kept loopoing over and over again in teh queue and wouldn't break out of the loop because i was mutating the queue and i was using the check len(queue) in teh while loop instead of using a for loop