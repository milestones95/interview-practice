"""
Problem: Subscription Event Log

You're given a list of raw log lines, semicolon-delimited, in this format:

timestamp;customer_id;event_type;plan;amount_cents

Example:

2026-09-13T10:00:00Z;cus_1;subscription_created;pro;0
2026-09-13T10:01:00Z;cus_1;payment_succeeded;pro;2000
2026-09-13T10:05:00Z;cus_2;subscription_created;basic;0
2026-09-13T10:06:00Z;cus_2;payment_succeeded;basic;500
2026-09-14T09:00:00Z;cus_1;payment_succeeded;pro;2000
2026-09-15T11:00:00Z;cus_2;subscription_canceled;basic;0

Valid event_type values: subscription_created, subscription_updated, subscription_canceled, payment_succeeded.

Part 1 — Parse & validate
Return valid parsed records and invalid ones (paired with a reason string). A row is valid if: exactly 5 fields, customer_id non-empty, event_type is one of the allowed values, plan non-empty, amount_cents is a non-negative integer.

Part 2 — Current plan per customer
For each customer, find their current plan: the plan value from their most recent (subscription_created or subscription_updated) event. Return a count of customers per plan. If a customer's most recent relevant event was subscription_canceled, they should not be counted toward any plan.

Part 3 — Revenue by plan, active customers only
For each plan, sum amount_cents from all payment_succeeded events, but only count payments from customers who are currently active (per the Part 2 definition — their latest lifecycle event isn't subscription_canceled). Return a dict of plan → total revenue.

part 3 needs the plan and the list of event objects for that plan. if the plan is active. that means there's no event for that customer where they had a cancelation

Assumptions, stated OA-style:

Lines may arrive out of timestamp order in the input list.
A customer can have multiple events of the same type.
amount_cents on non-payment events is typically 0 but isn't otherwise constrained.
No embedded semicolons in field values — plain split(";") is fine.
"""

from datetime import datetime

class payment_event:

    def __init__(self, timestamp,customer_id,event_type,plan,amount_cents):
        self.timestamp = datetime.fromisoformat(timestamp)
        self.customer_id = customer_id
        self.event_type = event_type
        self.plan = plan
        self.amount_cents = int(amount_cents)


valid_event_types = {"subscription_created", "subscription_updated", "subscription_canceled", "payment_succeeded"}

def parse_event_rows(rows: list[str])->tuple[list[payment_event],list[tuple[str,str]]]:

    invalid_rows = []
    valid_rows = []

    for row in rows:

        properties = row.split(";")

        if len(properties) !=5:
            invalid_rows.append((row, "row does not have 5 columns"))
            continue

        timestamp, customer_id, event_type, plan, amount_cents = properties

        if customer_id is None or customer_id == '':
            invalid_rows.append((row, "customer id is invalid"))
            continue

        if not event_type in valid_event_types:
            invalid_rows.append((row, "event type does not exist"))
            continue

        if plan is None or plan == '':
            invalid_rows.append((row, "plan is invalid"))
            continue

        if amount_cents is None or amount_cents == '':
            invalid_rows.append((row, "amount_cents is invalid"))
            continue

        if not is_valid_integer(amount_cents):
            invalid_rows.append((row, "amount_cents is invalid"))
            continue


        new_payment = payment_event(timestamp, customer_id, event_type, plan, amount_cents)

        valid_rows.append(new_payment)


    return valid_rows, invalid_rows


def is_valid_integer(number):

    try:
        int(number)
        return True

    except ValueError:
        print("not valid number")
        return False


def plan_per_customer(payment_events: list[payment_event]):

    sorted_payment_events = sorted(payment_events, key=lambda evt: evt.timestamp)

    customer_to_event = {}
    plan_to_count = {}
    plan_to_events = {}


    # have a hashmap for customer to their list of events

    # have another dict for the plan and their list of events. we need to know the amounts

    for pe in sorted_payment_events:
        if pe.event_type == "subscription_canceled" and pe.customer_id in customer_to_event:
            del customer_to_event[pe.customer_id]
            continue

        if pe.event_type == "subscription_created" or pe.event_type == "subscription_updated":
            customer_to_event[pe.customer_id] = pe.plan # gets their latest payment plan

    
    for k,v in customer_to_event.items():
        plan_to_count[v] = plan_to_count.get(v, 0) + 1


    for pe in sorted_payment_events:

        if pe.customer_id in customer_to_event:
            resolved_plan = customer_to_event[pe.customer_id]

            if resolved_plan not in plan_to_events:
                plan_to_events[resolved_plan] = []
            plan_to_events[resolved_plan].append(pe)
            


    
    return customer_to_event, plan_to_events, plan_to_count



def revenue_by_plan(customer_to_event, plan_to_events):

    plan_to_revenue = {}

    for plan, events in plan_to_events.items(): # go through each plan

        for evt in events: # get each event for the plan

            if evt.event_type == "payment_succeeded" and evt.customer_id in customer_to_event: # check to see if the customer is active, and if it's a payment succeeded event
                plan_to_revenue[plan] = plan_to_revenue.get(plan, 0) + evt.amount_cents


    return plan_to_revenue














test_data = [
    "2026-09-13T10:00:00Z;cus_1;subscription_created;pro;0",
"2026-09-13T10:01:00Z;cus_1;payment_succeeded;pro;2000",
"2026-09-13T10:05:00Z;cus_2;subscription_created;basic;0",
"2026-09-13T10:06:00Z;cus_2;payment_succeeded;basic;500",
"2026-09-14T09:00:00Z;cus_1;payment_succeeded;pro;2000",
"2026-09-15T11:05:00Z;cus_2;subscription_canceled;basic;0",
"2026-09-15T11:01:00Z;cus_2;payment_succeeded;;0",
"2026-09-15T11:02:00Z;;payment_succeeded;;0",
"2026-09-15T11:03:00Z;payment_succeeded;0"
]

valid_rows, invalid_rows = parse_event_rows(test_data)

# print("valid rows: ", len(valid_rows))
# print("invalid rows: ", len(invalid_rows))


# for i in invalid_rows:
#     print(i)

customer_to_event, plan_to_event, plan_to_count = plan_per_customer(valid_rows)

print("plan events: ", plan_to_event)

# print("plan to count: ", plan_to_count)



plan_by_revenue = revenue_by_plan(customer_to_event, plan_to_event)

print("plan by revenue: ", plan_by_revenue)

# did all parts in 60 mins but had 4 bugs.
# i had a empty for loop that would've stopped things from running
# i didn't completely follow instructions and counted events that weren't update or create event types
# i didn't count plans by looking at what each customer's plan is and instead counted by each time i saw an event i counted the plan. that could potentially cause bugs.
# i finished part 3 with basically 30 seconds to spare so these bugs would've slipped through even if i had tests to run against