"""Problem: Customer Support Ticket Queue

Define a Ticket class with two fields:

severity — an integer from 1 to 5, where 5 is the most critical.
wait_time — how many minutes the customer has been waiting, as an integer.

You want sorted(tickets) to produce a list ordered from most urgent to least urgent, using no key= argument — just __lt__. The rules:

Higher severity should come first in the sorted result.
If two tickets have the same severity, the one with the longer wait_time should come first.
"""

import heapq

class ticket:

    def __init__(self, ticket_id, severity, wait_time):
        self.severity = severity
        self.id = ticket_id
        self.wait_time = wait_time

    
    def __lt__(self, other):

        if self.severity != other.severity:
            return self.severity < other.severity

        if self.wait_time != other.wait_time:
            return self.wait_time < other.wait_time

        return self.id < other.id


class tickets:

    def __init__(self):
        self.tickets = []


    def add_ticket(self, id, sev, wait_time):

        # create new ticket
        new_ticket = ticket(id, -sev, -wait_time)


        # add new ticket to the heap. Cover if there's a tie in priority which ticket should come first

        heapq.heappush(self.tickets, (new_ticket.severity, new_ticket.wait_time, new_ticket))


    def get_order(self):

        ordered_tickets = []
        end = len(self.tickets)

        for i in range(end):
            _,_,t = heapq.heappop(self.tickets)
            ordered_tickets.append(t.id)

        print("ordered tickets: ", ordered_tickets)




test = tickets()

test.add_ticket(1, 2, 4)
test.add_ticket(2, 1, 9)
test.add_ticket(3, 7, 5)
test.add_ticket(4, 7, 10)
test.add_ticket(5, 7, 10)

test.get_order()


# finished in 17 mins