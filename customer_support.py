"""Problem: Support Ticket Queue

Part 1 — create_ticket(customer_id, subject, priority)
A customer opens a ticket. priority is one of a small fixed set (e.g. low/medium/high/urgent). Returns a unique ticket_id.

Part 2 — assign_next_ticket(agent_id)
An available support agent asks for their next ticket to work. They should get the highest-priority, oldest unassigned ticket (priority wins, ties broken by whoever's been waiting longest). Once assigned, it's no longer available to hand out to anyone else.

Part 3 — escalate_ticket(ticket_id)
A ticket's priority gets bumped up one level (e.g. medium → high) — maybe the customer complained again, or an SLA timer tripped. This needs to change where the ticket sits in line for Part 2, without anyone having to re-scan the whole backlog.

Part 4 — get_ticket_history(customer_id)
Return every ticket a given customer has ever opened, most recent first — including ones already resolved/assigned, not just pending ones.

Part 5 — reassign_ticket(ticket_id, new_agent_id)
A ticket already assigned to one agent gets handed to someone else (agent went on PTO, etc.) — without touching anything about the ticket's history or customer association.
"""

import heapq

class ticket:

    def __init__(self, customer_id, ticket_id, subject, priority):
        self.customer_id = customer_id
        self.ticket_id = ticket_id
        self.subject = subject
        self.priority = priority
        self.agent = None
        self.status = "pending"

# an agent can have 0 or more tickets assigned to them at once
class agent:

    def __init__(self, agent_id):
        self.agent_id = agent_id


class ticket_system: # I think we can use a heap for this

    def __init__(self):
        self.agent_id_to_tickets = {} # to quickly get the tickets assigned to a specific agent
        self.ticket_id_to_ticket = {} # to quickly access a specific ticket to escalate its priority or reassign
        self.agent_id_to_agent = {}
        self.tickets = []
        self.count = 0
        self.customer_id_to_tickets = {}

    
    def create_ticket(self, customer_id, subject, priority):
        ticket_id = self.count + 1 # assign new ticket id, making sure it's unique
        int_priority = translate_severity(priority) # get the priority as an int to use in the heap
        new_ticket = ticket(customer_id, ticket_id, subject, int_priority) # create thew new ticket

        heapq.heappush(self.tickets, (-new_ticket.priority, ticket_id, new_ticket)) # add it to the priority queue
        self.ticket_id_to_ticket[new_ticket.ticket_id] = new_ticket # add the new ticket to the ticket registry

        # add ticket to customer's list of created tickets

        if customer_id not in self.customer_id_to_tickets:
            # print("customer id added: ", customer_id)
            self.customer_id_to_tickets[customer_id] = []

        self.customer_id_to_tickets[customer_id].append(new_ticket)
        # print("customer tickets: ", self.customer_id_to_tickets)
        self.count+=1

    
    def assign_next(self, agent_id):

        try:
        # use lazy deletion with hashmap
            if len(self.tickets) < 1:
                raise ValueError("there are no more tickets to assign")

            while True:

                _,_,next_ticket = heapq.heappop(self.tickets) # get next high priority ticket
                if next_ticket.priority != self.ticket_id_to_ticket[next_ticket.ticket_id].priority:
                    continue
                else:

                    if agent_id not in self.agent_id_to_agent: # check if the agent is in the agent registry
                        curr_agent = agent(agent_id) # if not, create a new agent and create them in registry
                        self.agent_id_to_agent[agent_id] = curr_agent
                        self.agent_id_to_tickets[agent_id] = []

                    else:
                        curr_agent = self.agent_id_to_agent[agent_id] # if the agent already exist, get the agent
                    
                    next_ticket.agent = curr_agent # assign the ticket to the agent
                    next_ticket.status = "assigned"
                    self.agent_id_to_tickets[agent_id].append(next_ticket) # add the new ticket to the agent's queue of tickets
                    self.ticket_id_to_ticket[next_ticket.ticket_id] = next_ticket # update the ticket in the ticket registry

                    break

        except ValueError as error:
            print(error)


    def escalate_ticket(self, ticket_id):
        try:

            if ticket_id not in self.ticket_id_to_ticket:
                raise ValueError("ticket doesn't exist")
            # get the ticket by id
            existing_ticket = self.ticket_id_to_ticket[ticket_id]
            existing_ticket.priority +=1
            self.ticket_id_to_ticket[ticket_id] = existing_ticket

        except ValueError as error:
            print(error)

    def get_customer_tickets(self, customer_id):

        return self.customer_id_to_tickets[customer_id]

    def reassign_ticket(self, ticket_id, agent_id):

        current_ticket = self.ticket_id_to_ticket[ticket_id] # get the current ticket
        old_agent = self.agent_id_to_agent[current_ticket.agent.agent_id]
        new_agent = self.agent_id_to_agent[agent_id] # get the new agent we will assign the ticket to
        current_ticket.agent = new_agent # assign the agent property to the new agent
        self.ticket_id_to_ticket[ticket_id] = current_ticket # update the ticket registry
        self.agent_id_to_tickets[agent_id].append(current_ticket) # add the ticket to the new agent's list

        # delete the ticket from the old agent
        old_tickets = self.agent_id_to_tickets[old_agent.agent_id]  # get the old list of tickets
        updated_tickets = self.delete_ticket_from_agent_queue(old_tickets, ticket_id) # delete the old ticket from the list of tickets and return teh new one

        self.agent_id_to_tickets[old_agent.agent_id] = updated_tickets

    def delete_ticket_from_agent_queue(self, tickets, ticket_id):

        for i in range(len(tickets)):

            if tickets[i].ticket_id == ticket_id:
                print("found")
                tickets.pop(i)
                break


        return tickets


def translate_severity(str_severity):
    if str_severity == "low":
        return 1

    elif str_severity == "medium":
        return 2

    elif str_severity== "high":
        return 3
    else:
        return 4

test = ticket_system()
test.create_ticket("23", "my laptop won't work", "medium")
test.create_ticket("19", "back up my data", "high")

test.create_ticket("15", "website front end is frozen", "low")
test.create_ticket("17", "data leak", "urgent")

test.assign_next("123")
test.assign_next("456")
test.assign_next("987")
test.escalate_ticket(9)


test.create_ticket("23", "scratched my screen", "low")

# print("ticket id: ", ticket_assigned.ticket_id, "--- ", "priority: ", ticket_assigned.priority)

customer_tickets = test.get_customer_tickets("23")

for ct in customer_tickets:
    print("ticket id: ", ct.ticket_id)

test.reassign_ticket(4, "987")

agent_tickets = test.agent_id_to_tickets["123"]

for a_t in agent_tickets:
    print("ticket: ", a_t.ticket_id)

print("-------------------------------")
agent_tickets = test.agent_id_to_tickets["456"]

for a_t in agent_tickets:
    print("ticket: ", a_t.ticket_id)
print("-------------------------------")

agent_tickets = test.agent_id_to_tickets["987"]

for a_t in agent_tickets:
    print("ticket: ", a_t.ticket_id)

print("-------------------------------")

test.reassign_ticket(4, "456")

agent_tickets = test.agent_id_to_tickets["456"]

for a_t in agent_tickets:
    print("ticket: ", a_t.ticket_id)

print("-------------------------------")

test.assign_next("123")
test.assign_next("123")




