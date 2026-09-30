"""
Parsing Drill: Support Ticket Priority Escalation

Input format:

"<ticket_id>,<timestamp>,<priority>"
ticket_id: string
timestamp: unix seconds (integer)
priority: one of "low", "medium", "high", "critical", "closed"

Allowed transitions:

A ticket's first-ever event must be "low" or "medium" (tickets are never opened at "high"/"critical" directly).
Escalation must move exactly one level up at a time among low → medium → high → critical — you can't jump from "low" straight to "critical".
De-escalation (moving back down a level) is not allowed at all — priorities only ever go up or close.
"closed" can happen from any priority level (including immediately after the first event).
Once a ticket is "closed", no further events for that ticket_id are valid.
Events for a given ticket_id are not guaranteed to arrive in order in the input.

Task:

python
def parse_ticket_events(rows: List[str]) -> Tuple[List[dict], List[str]]:
    ...

Test data:

python
rows = [
    "tix_1,1000,low",
    "tix_1,1010,medium",
    "tix_1,1020,high",
    "tix_2,2000,medium",
    "tix_2,2010,closed",
    "tix_3,3000,high",              # never opened at low/medium — invalid
    "tix_1,1005,medium",            # out of order relative to tix_1's other rows
    "tix_4,4000,low",
    "tix_4,4020,high",              # skips "medium" — invalid
    "tix_5,5000,critical",          # opened directly at critical — invalid
    "tix_2,2020,high",              # ticket already closed — invalid
    "tix_6,6000,medium",
    "tix_6,6010,low",               # de-escalation — invalid
    "tix_7,7000,low",
    "tix_7,notanumber,medium",      # bad timestamp
]
"""

allowed_status = {"low", "medium", "high", "critical", "closed"}

from enum import IntEnum

class Status(IntEnum):
    low=1
    medium=2
    high=3
    critical=4
    closed=5

class ticket_object:

    def __init__(self, ticket_id, timestamp, status):
        self.ticket_id = ticket_id
        self.timestamp = int(timestamp)
        self.status = status


class ticket_system:

    # parse each row

    # validate each row if it has the correct # of columns

    # sort the results

    # then do further validation on the severity of each row

    # need to track last severity against the current severity and follow the rules


    def validate_parameters(self, ticket_id, timestamp, status):

        if not timestamp.isdigit():
            return False

        if status not in allowed_status:
            return False

        return True


    def get_valid_transactions(self, rows: list[str]):

        ticket_list = []
        invalid_tickets = []

        for row in rows:

            properties = row.split(",")

            ticket_id, timestamp, status = properties

            if not self.validate_parameters(ticket_id, timestamp, status):

                # invalid ticket
                invalid_tickets.append(row)
                continue

            new_ticket = ticket_object(ticket_id, timestamp, status)

            ticket_list.append(new_ticket)

        # print("ticket_list: ", ticket_list)


        sorted_list = sorted(ticket_list, key=lambda tick: tick.timestamp)

        ticket_map = {}
        valid_tickets = []

        for ticket in sorted_list:


            # if ticket doesn't exist
            if not ticket.ticket_id in ticket_map:

                if not (ticket.status == "low" or ticket.status =="medium"):
                    # invalid ticket
                    invalid_tickets.append(""+ ticket.ticket_id+"," + str(ticket.timestamp) + "," + ticket.status)
                    continue
                
                # add to valid transactions and update mapping
                ticket_map[ticket.ticket_id] = ticket.status
                valid_tickets.append(ticket)


            # if ticket does exist
            else:

                if ticket_map[ticket.ticket_id] == "closed":
                    # invalid_ticket
                    invalid_tickets.append(""+ ticket.ticket_id+"," + str(ticket.timestamp) + "," + ticket.status)
                    continue

                # if new status is closed
                elif ticket.status == "closed":
                    ticket_map[ticket.ticket_id] = "closed"
                    valid_tickets.append(ticket)


                # if new status is more than one level higher or      # if new status is less than the current severity
                elif Status[ticket.status] - Status[ticket_map[ticket.ticket_id]] !=1:
                    # invalid ticket
                    invalid_tickets.append(""+ ticket.ticket_id+"," + str(ticket.timestamp) + "," + ticket.status)
                    continue

                # otherwise, update the severity and add the ticket to the list of valid transactions
                # update mapping
                else:
                    ticket_map[ticket.ticket_id] = ticket.status
                    valid_tickets.append(ticket)

        # print("valid tickets: ", valid_tickets)
        return valid_tickets, invalid_tickets


rows = [
    "tix_1,1000,low",
    "tix_1,1010,medium",
    "tix_1,1020,high",
    "tix_2,2000,medium",
    "tix_2,2010,closed",
    "tix_3,3000,high",              # never opened at low/medium — invalid
    "tix_1,1005,medium",            # out of order relative to tix_1's other rows
    "tix_4,4000,low",
    "tix_4,4020,high",              # skips "medium" — invalid
    "tix_5,5000,critical",          # opened directly at critical — invalid
    "tix_2,2020,high",              # ticket already closed — invalid
    "tix_6,6000,medium",
    "tix_6,6010,low",               # de-escalation — invalid
    "tix_7,7000,low",
    "tix_7,notanumber,medium",      # bad timestamp
]

test = ticket_system()

results,invalid_tix = test.get_valid_transactions(rows)


for res in results:

    print("tick id: ", res.ticket_id, " timestamp: ", res.timestamp, " status: ", res.status)


print("invalid tix: ", invalid_tix)

# took 35 mins