"""
Subscription Plan Change Tracker

Background: Customers can upgrade or downgrade their Stripe subscription over time. Every plan change gets logged as an event.

Input format: A list of strings, each formatted as:

"<customer_id>,<subscription_id>,<timestamp>,<plan>,<action>"
customer_id, subscription_id: strings identifying the customer and their subscription
timestamp: unix seconds (integer)
plan: one of "basic", "pro", "enterprise" — tiers in that order, basic < pro < enterprise
action: one of "created", "upgraded", "downgraded", "canceled"

Business rules:

The first event for any subscription_id should be "created".
An "upgraded" event's plan must be a higher tier than that subscription's plan immediately before it; a "downgraded" event's plan must be lower. (A row where the action doesn't match the actual tier direction is invalid — e.g., an "upgraded" event whose plan is actually a downgrade from the prior tier.)
A "canceled" event has no meaningful plan change — the subscription is just done as of that timestamp.
Events for a given subscription are not guaranteed to arrive in chronological order in the input list.

Example rows:

"cus_1,sub_a,1000,basic,created"
"cus_1,sub_a,1010,pro,upgraded"
"cus_1,sub_a,1020,enterprise,upgraded"
"cus_2,sub_b,2000,pro,created"
"cus_2,sub_b,2010,basic,downgraded"
"cus_2,sub_b,2020,canceled"
"cus_1,sub_a,1015,pro,upgraded"

(Note: that last row is out of order relative to sub_a's other events, and note sub_b's cancel row only has 4 comma-separated fields, not 5 — a plan value is optional/blank on cancellation.)

Part 1

Write parse_plan_events(rows: List[str]) -> Tuple[List[dict], List[str]] — parse and validate. Decide how you'll handle the "canceled rows may have 4 fields instead of 5" wrinkle, and validate the upgrade/downgrade-direction-matches-action rule. Structure it so a new rule is cheap to add.

Part 2

Write current_plan_per_subscription(rows: List[str]) -> Dict[str, str] — for each subscription_id, return its plan as of its most recent event, or "canceled" if its latest event was a cancellation. Use only valid rows.

Part 3

Write plan_migration_counts(rows: List[str]) -> Dict[str, int] — across all subscriptions, count how many times each specific upgrade or downgrade transition happened, keyed like "basic->pro" or "enterprise->basic". (Don't count "created" or "canceled" events — only actual tier-to-tier moves.)"""

# for part 3 we likely need the events to be in order so we know what the source and destination were
# "cus_1,sub_a,1015,pro,upgraded"

from typing import Tuple, List, Dict

from enum import IntEnum

class Tier(IntEnum):
    basic=1
    pro=2
    enterprise=3

action_type_available = {"created", "upgraded", "downgraded", "canceled"}
tiers_available = {"basic", "pro", "enterprise"}



class change:

    def __init__(self, customer_id, subscription_id, timestamp, tier, action_type):
        self.customer_id = customer_id
        self.subscription_id = subscription_id
        self.timestamp = int(timestamp)
        self.tier = tier
        self.action_type = action_type

class subscription_events:


    def parse_events(self, rows: List[str]) -> Tuple[List[dict], List[str]]:

        subscription_status = {}
        unsorted_events = []

        for row in rows:

            properties = row.split(",")

            if len(properties) !=4 and len(properties) !=5:
                continue

            if len(properties) == 4:
                customer_id, sub_id, timestamp,action = properties

                if not timestamp.isdigit():
                    continue

                if action!="canceled":
                    continue

                print("valid event: ", properties)

                new_evt = change(customer_id, sub_id,timestamp,None, action)

                unsorted_events.append(new_evt)



            if len(properties) == 5:

                customer_id, sub_id, timestamp, tier,action = properties
                if not timestamp.isdigit():
                    continue

                if action not in action_type_available:
                    continue

                if tier not in tiers_available: 
                    continue

                print("valid event: ", properties)
                new_evt = change(customer_id, sub_id,timestamp,tier, action)

                unsorted_events.append(new_evt)


        sorted_events = sorted(unsorted_events, key=lambda evt: evt.timestamp)
        valid_events = []

        for evt in sorted_events:

            print("sub id: ", evt.subscription_id, " timestamp: ", evt.timestamp)

            if evt.subscription_id not in subscription_status:

                if evt.action_type != "created":
                    continue

                valid_events.append(evt)
                subscription_status[evt.subscription_id] = evt.tier

            
            else:

                if evt.action_type == "downgraded":

                    if Tier[subscription_status[evt.subscription_id]].value > Tier[evt.tier].value:
                        print("tier before: ", Tier[subscription_status[evt.subscription_id]], " current: ", Tier[evt.tier])
                        valid_events.append(evt)
                        subscription_status[evt.subscription_id] = evt.tier


                if evt.action_type == "upgraded": 
                    if Tier[subscription_status[evt.subscription_id]].value < Tier[evt.tier].value:
                        print("tier before: ", Tier[subscription_status[evt.subscription_id]], " current: ", Tier[evt.tier])

                        valid_events.append(evt)
                        subscription_status[evt.subscription_id] = evt.tier


                if evt.action_type == "canceled": 
                    valid_events.append(evt)
                    subscription_status[evt.subscription_id] = evt.tier

        print("sorted events: ", valid_events)

        for se in valid_events:

            print("sub id: ", se.subscription_id, " tier: ", se.tier, " action: ", se.action_type)
        return valid_events

    


test_data = [
    "cus_1,sub_a,1010,enterprise,upgraded",
    "cus_1,sub_a,1000,basic,created",
    "cus_1,sub_a,1020,pro,upgraded",
    "cus_2,sub_b,2000,pro,created",
    "cus_2,sub_b,2010,basic,downgraded",
    "cus_2,sub_b,2020,canceled",
    "cus_1,sub_a,9sd,pro,upgraded"
]

# spent 10 mins thinking


test = subscription_events()
test.parse_events(test_data)

# spent 50 mins just on the parsing and making sure actions were valid upgrades and downgrades