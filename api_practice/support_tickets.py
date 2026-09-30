"""
PRACTICE PROBLEM #4 — "Support Ticket Activity Feed"
======================================================
Same interview shape: a provided client, paginated + messy responses,
three parts of increasing difficulty. This one sticks to structures
you're already solid on — doubly linked list + hashmap, then a BST —
combined in a fresh scenario, per your own plan's Day 4 focus
(combining two structures correctly for a new problem).

Time budget: 40-45 min. Run it as you go.

===========================================================================
SCENARIO
===========================================================================
You work on internal tooling for a support team. `TicketFeedClient`
wraps a paginated API returning ticket update events (a ticket got
created, touched, or closed by some agent, at some time). You need to:
  1. Clean the raw events.
  2. Track each agent's N most-recently-handled tickets.
  3. Support "which tickets happened in this time window" queries.

You are given the client. Do not modify it. Implement the three
functions below it.

===========================================================================
PART 1 (Easy) — parse_page(response) -> list[dict]
===========================================================================
`client.get_events(cursor)` returns one page:

    {
        "events": [ <raw event dict>, ... ],
        "next_cursor": "<str>" | None
    }

Each raw event dict on a GOOD day:

    {"ticket_id": "T1", "agent_id": "agent_1",
     "timestamp": "2026-08-20T09:00:00Z", "status": "open"}

Real entries may:
  - be `None` entirely (dropped upstream)
  - have a non-string "ticket_id" — unrecoverable, skip the event
  - have "agent_id" missing or `None` — unrecoverable (we can't
    attribute the event to anyone), skip the event
  - have "timestamp" missing, `None`, or malformed — unrecoverable
    (we can't order it), skip the event
  - have "status" missing — default it to `"open"`

Return a clean list of:
    {"ticket_id": str, "agent_id": str, "timestamp": datetime, "status": str}

===========================================================================
PART 2 (Medium) — recent_tickets_by_agent(client, capacity) -> dict[str, list[str]]
===========================================================================
Paginate through ALL pages via `client.get_events(cursor)` /
`next_cursor`. Using your Part 1 parser, track each agent's tickets in
the order they were handled (by timestamp, which arrives in
chronological order across pages in this fixture — you don't need to
re-sort).

For each agent, keep only their `capacity` MOST RECENT tickets — once
an agent exceeds `capacity`, the oldest one they handled drops off.

Model this internally with an actual doubly linked list per agent
(append new tickets at the tail, evict from the head when over
capacity) — not just a Python list with slicing. The point of this
part is DLL mechanics under a wrapping scenario, same as your browser
history / tab management practice. The function's return type is a
plain dict of lists (chronological order, oldest-of-the-kept-ones
first) so it's easy to test — but build the mechanism with a real DLL.

===========================================================================
PART 3 (Medium) — build_ticket_time_index(client) -> TreeNode
                   get_tickets_in_range(root, start, end) -> list[str]
===========================================================================
Using the same fully-paginated, parsed data, build a BST keyed by
timestamp (one node per event, allow duplicate timestamps to both be
stored — don't assume timestamps are unique). Then implement a range
query: given a start and end datetime (inclusive), return the
ticket_ids of every event with a timestamp in that range, in ascending
timestamp order.

Design your own `TreeNode`/BST structure — you've done this before
(real estate listings, airline standby list). Same judgment call as
those: an unbalanced BST is fine here given the bounded, non-adversarial
input, but be ready to name that tradeoff if asked.

===========================================================================
THE CLIENT (do not modify — this simulates the provided SDK)
===========================================================================
"""

from datetime import datetime

class TicketNode:

    def __init__(self, ticket_id, status, agent_id, timestamp):
        self.ticket_id = ticket_id
        self.status = status
        self.agent_id = agent_id
        self.timestamp = timestamp
        self.left = None
        self.right = None

class TicketTree:

    def __init__(self):
        self.root = None

class Ticket:

    def __init__(self, ticket_id, status, agent_id, timestamp):
        self.ticket_id = ticket_id
        self.status = status
        self.agent_id = agent_id
        self.timestamp = timestamp
        self.prev = None
        self.next = None

class Agent:

    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.head = None
        self.tail = None
        self.count = 0


class AgentTicketSystem:

    def __init__(self):
        self.agent_id_to_agent = {}
        self.ticket_id_to_ticket = {}




class TicketFeedClient:
    """Simulates a paginated internal support-ticket event feed. 3 pages, deliberately messy."""

    _PAGES = [
        {
            "events": [
                {"ticket_id": "T1", "agent_id": "agent_1",
                 "timestamp": "2026-08-20T09:00:00Z", "status": "open"},
                {"ticket_id": "T2", "agent_id": "agent_1",
                 "timestamp": "2026-08-20T09:05:00Z"},  # no status -> default "open"
                None,  # dropped upstream
                {"ticket_id": "T3", "agent_id": None,
                 "timestamp": "2026-08-20T09:10:00Z", "status": "closed"},  # no agent
                {"ticket_id": "T4", "agent_id": "agent_2",
                 "timestamp": "not-a-timestamp", "status": "open"},  # bad timestamp
            ],
            "next_cursor": "page2",
        },
        {
            "events": [
                {"ticket_id": "T5", "agent_id": "agent_1",
                 "timestamp": "2026-08-20T09:15:00Z", "status": "closed"},
                {"ticket_id": "T6", "agent_id": "agent_2",
                 "timestamp": "2026-08-20T09:20:00Z", "status": "open"},
                {"ticket_id": 77, "agent_id": "agent_1",
                 "timestamp": "2026-08-20T09:25:00Z"},  # non-string ticket_id
                {"ticket_id": "T7", "agent_id": "agent_2",
                 "timestamp": "2026-08-20T09:30:00Z", "status": "open"},
            ],
            "next_cursor": "page3",
        },
        {
            "events": [
                {"ticket_id": "T8", "agent_id": "agent_1",
                 "timestamp": "2026-08-20T09:35:00Z", "status": "open"},
                {"ticket_id": "T9", "agent_id": "agent_3",
                 "timestamp": "2026-08-20T09:40:00Z", "status": "open"},
                {"ticket_id": "T10", "agent_id": "agent_1",
                 "timestamp": "2026-08-20T09:45:00Z", "status": "closed"},
            ],
            "next_cursor": None,
        },
    ]

    def get_events(self, cursor=None):
        if cursor is None:
            return self._PAGES[0]
        idx = {"page2": 1, "page3": 2}.get(cursor)
        if idx is None:
            raise ValueError(f"invalid cursor: {cursor}")
        return self._PAGES[idx]

# ===========================================================================
# YOUR CODE BELOW
# ===========================================================================

def parse_page(response: dict) -> list:
    
    # print("response: ", response)

    events = response.get('events', None)
    valid_events = []
    if events:

        for evt in events:
            if evt:

                if not is_valid_string(evt.get('ticket_id',None)) or not is_valid_string(evt.get('agent_id',None)):
                    continue

                if not is_valid_timestamp(evt.get('timestamp', None)):
                    continue
                
                #     {"ticket_id": str, "agent_id": str, "timestamp": datetime, "status": str}
                new_ticket = {
                    "ticket_id": evt.get('ticket_id'),
                    "agent_id": evt.get('agent_id'),
                    "timestamp": evt.get('timestamp'),
                    "status": evt.get('status', 'open')
                }

                valid_events.append(new_ticket)
    print("---------------------------------")
    # print("valid events: ", valid_events)
    return valid_events




def recent_tickets_by_agent(client, capacity: int) -> dict:
    # TODO: Part 2 — build this with a real doubly linked list per agent

    cursor = None

    ticket_system = AgentTicketSystem()

    while True:
        page = client.get_events(cursor)
        ticket_events = parse_page(page)

        for tick_evt in ticket_events:

            agent_id = tick_evt.get('agent_id')
            ticket_node = Ticket(tick_evt.get('ticket_id'), tick_evt.get('status'), agent_id, tick_evt.get('timestamp'))

            # if agent doesn't exist and have a list yet
            if agent_id not in ticket_system.agent_id_to_agent:
                print("new agent: ", agent_id)
                new_agent = Agent(agent_id)
                new_agent.head = ticket_node
                new_agent.tail = ticket_node
                new_agent.count +=1
                ticket_system.agent_id_to_agent[agent_id] = new_agent

            # if agent already exists

            else:
                # print("existing agent: ", agent_id)

                # if currently at capacity
                print("agent id: ", agent_id, " count: ", ticket_system.agent_id_to_agent[agent_id].count, "  capacity: ", capacity)
                if ticket_system.agent_id_to_agent[agent_id].count == capacity: 
                    print("deleting")
                    curr_head = ticket_system.agent_id_to_agent[agent_id].head # None -> 1->3->4->5
                    prev = curr_head.prev
                    curr_next = curr_head.next
                    ticket_system.agent_id_to_agent[agent_id].head = curr_next
                    ticket_system.agent_id_to_agent[agent_id].head.prev = None

                    existing_agent = ticket_system.agent_id_to_agent[agent_id]
                    print("existing agent head: ", existing_agent.head.ticket_id)

                    existing_agent.tail.next = ticket_node
                    ticket_node.prev = existing_agent.tail
                    existing_agent.tail = ticket_node
                    # existing_agent.count+=1
                    ticket_system.agent_id_to_agent[agent_id] = existing_agent

                else:
                    existing_agent = ticket_system.agent_id_to_agent[agent_id]
                    print("existing agent head: ", existing_agent.head.ticket_id)

                    existing_agent.tail.next = ticket_node
                    ticket_node.prev = existing_agent.tail
                    existing_agent.tail = ticket_node
                    existing_agent.count+=1
                    ticket_system.agent_id_to_agent[agent_id] = existing_agent
                # if ticket_system.agent_id_to_agent[agent_id].count <  capacity:
                #     existing_agent = ticket_system.agent_id_to_agent[agent_id]
                #     print("existing agent head: ", existing_agent.head.ticket_id)

                #     existing_agent.tail.next = ticket_node
                #     ticket_node.prev = existing_agent.tail
                #     existing_agent.tail = ticket_node
                #     existing_agent.count+=1
                #     ticket_system.agent_id_to_agent[agent_id] = existing_agent
                # else:
                #     print("hola")
                #     curr_head = ticket_system.agent_id_to_agent[agent_id].head # None -> 1->3->4->5
                #     prev = curr_head.prev
                #     curr_next = curr_head.next
                #     ticket_system.agent_id_to_agent[agent_id].head = curr_next
                #     ticket_system.agent_id_to_agent[agent_id].head.prev = None

                #     existing_agent = ticket_system.agent_id_to_agent[agent_id]
                #     print("existing agent head: ", existing_agent.head.ticket_id)

                #     existing_agent.tail.next = ticket_node
                #     ticket_node.prev = existing_agent.tail
                #     existing_agent.tail = ticket_node
                #     existing_agent.count+=1
                #     ticket_system.agent_id_to_agent[agent_id] = existing_agent

                # we are always adding a ticket to the end of the list
       





        cursor = page.get('next_cursor')
        print("cursor: ", cursor)
        if cursor is None:
            break

    agent_per_ticket_arr = []

    items = ticket_system.agent_id_to_agent.items()

    for k,v in items:
        new_obj = {
            k: []
        }
        curr_agent = ticket_system.agent_id_to_agent[k]
        curr_head = curr_agent.head
        while curr_head:
            new_obj.get(k).append(curr_head.ticket_id)
            curr_head = curr_head.next

        agent_per_ticket_arr.append(new_obj)
    print("final array: ", agent_per_ticket_arr)
    return agent_per_ticket_arr


def build_ticket_time_index(client):
    # TODO: Part 3a — design your own TreeNode / BST

    ticket_tree = TicketTree()
    cursor = None
    while True:
        page = client.get_events(cursor) # get the page
        ticket_events = parse_page(page) # get the valid ticket events from the page

        for tick_evt in ticket_events: # go through each ticket in the list and add it to the bst
            ticket_tree.root = insert_node(ticket_tree.root, tick_evt.get('ticket_id'), tick_evt.get('status'), tick_evt.get('agent_id'), tick_evt.get('timestamp'))

        cursor = page.get('next_cursor') # get the next cursor
        if cursor is None: # if the next cursor is empty then we don't need to continue paging because we're done
            break


    traverse_node(ticket_tree.root)
    return ticket_tree.root


def traverse_node(root):

    if root is None:
        return

    traverse_node(root.left)
    print('ticket id: ', root.ticket_id, " timestamp: ", root.timestamp)
    traverse_node(root.right)

    # raise NotImplementedError

def insert_node(root, ticket_id, status, agent_id, timestamp):

    if root is None:
        return TicketNode(ticket_id, status, agent_id, timestamp)

    if (timestamp, ticket_id) < (root.timestamp, root.ticket_id):
        root.left = insert_node(root.left, ticket_id, status, agent_id, timestamp)
    else:
        root.right = insert_node(root.right, ticket_id, status, agent_id, timestamp)

    
    return root


def get_tickets_in_range(root, start, end) -> list:

    ticket_list = []
    get_tickets_in_range_helper(root, start, end, ticket_list)

    for tick in ticket_list:
        print("ticket: ", tick.ticket_id, "----- timestamp: ", tick.timestamp)

    return ticket_list

    

def get_tickets_in_range_helper(root, start, end, ticket_list)-> list:
    if root is None:
        return

    
    if datetime.fromisoformat(root.timestamp) < start:
        root = get_tickets_in_range_helper(root.right, start, end, ticket_list)

    elif datetime.fromisoformat(root.timestamp) > end:
        root = get_tickets_in_range_helper(root.left, start, end, ticket_list)

    else:
        ticket_list.append(root)
        get_tickets_in_range_helper(root.right, start, end, ticket_list)
        get_tickets_in_range_helper(root.left, start, end, ticket_list)
# def ingest_page

def is_valid_string(string_to_check):

    return isinstance(string_to_check,str)

def is_valid_timestamp(ts_to_check):

    try:

        timestamp = datetime.fromisoformat(ts_to_check)
        return True
    except (ValueError, TypeError) as Error:
        return False


# ===========================================================================
# TEST HARNESS — run this file directly to check your work
# ===========================================================================

def _run_tests():
    client = TicketFeedClient()

    # --- Part 1 ---
    page1 = client.get_events()
    parsed = parse_page(page1)
    ids = sorted(e["ticket_id"] for e in parsed)
    print("Part 1 parsed ticket_ids:", ids)
    assert set(ids) == {"T1", "T2"}, \
        f"expected T1/T2 kept (None, no-agent, bad-timestamp events dropped), got {ids}"
    t2 = next(e for e in parsed if e["ticket_id"] == "T2")
    assert t2["status"] == "open", "T2 has no status in the raw data, should default to 'open'"
    print("Part 1: looks right\n")

    # --- Part 2 ---
    recents = recent_tickets_by_agent(client, capacity=3)
    print("Part 2 recent_tickets_by_agent(capacity=3):", recents)
    print("  expect agent_1: ['T5', 'T8', 'T10'] (T1, T2 evicted, oldest-of-kept first)")
    print("  expect agent_2: ['T6', 'T7'] (under capacity, nothing evicted)")
    print("  expect agent_3: ['T9']\n")

    # # --- Part 3 ---
    root = build_ticket_time_index(client)
    start = datetime.fromisoformat("2026-08-20T09:05:00+00:00")
    end = datetime.fromisoformat("2026-08-20T09:30:00+00:00")
    result = get_tickets_in_range(root, start, end)
    print(f"Part 3 get_tickets_in_range({start}, {end}):", result)
    print("  expect: ['T2', 'T5', 'T6', 'T7'] in ascending timestamp order\n")


if __name__ == "__main__":
    _run_tests()


# finished part 1 by the 16 min mark. finished part 2 by the 1hr 15 mark. took me a while to debug the linked list and see the values. the parsing and paging part was easy. For some reason the head wasn't removing from the linked list with my initial implementation when the capacity was reached

# finished part 3a in 14 mins. finished 3b in another 10 mins 