"""
Problem: Parse Checkout Session Events

Stripe checkout emits a stream of events as a session moves through checkout. You're given a list of raw event rows (as they'd come off a CSV or event log). Your job in Part 1 is just to parse and validate them into clean structured objects — later parts will use this output to analyze session flow.

Input format — each row is a string (comma-separated) like:

session_id,event_type,step,timestamp,amount
cs_A1,session_created,,2026-09-01T10:00:00Z,
cs_A1,step_viewed,contact_info,2026-09-01T10:00:05Z,
cs_A1,step_viewed,shipping,2026-09-01T10:00:20Z,
cs_A1,step_viewed,payment,2026-09-01T10:01:00Z,
cs_A1,session_completed,,2026-09-01T10:02:00Z,4999
cs_B2,session_created,,2026-09-01T11:00:00Z,
cs_B2,step_viewed,contact_info,2026-09-01T11:00:03Z,

event_type is one of: session_created, step_viewed, session_completed, session_expired
step is only populated for step_viewed events, and is one of: contact_info, shipping, payment
amount (in cents) is only populated for session_completed events
timestamp is ISO 8601

Task: Write a function that takes the list of raw rows (including a header row) and returns a list of parsed, validated event objects.

A row is invalid if:

it doesn't have exactly 5 fields
event_type isn't one of the known types
step is present when it shouldn't be (or missing/invalid when it should be)
timestamp fails to parse
amount is present when it shouldn't be, or is present but not a valid non-negative integer

Invalid rows should be collected separately rather than crashing the parse.
"""

from typing import Tuple, Dict, List
from datetime import datetime

allowed_event_types = {"session_created", "step_viewed", "session_completed", "session_expired"}

allowed_steps = {"contact_info", "shipping", "payment"}

class event:

    def __init__(self, session_id,event_type,step,timestamp,amount):
        self.session_id = session_id
        self.event_type = event_type
        self.step = step
        self.timestamp = timestamp
        self.amount = amount


class event_stream:

    def parse_events(self, rows: List[str])-> List[event]:

        invalid_events = []
        valid_events = []

        for row in rows:

            properties = row.split(",")
            print("properties: ", properties)

            if len(properties) < 4 or len(properties) > 5:

                invalid_events.append(invalid_events)
                continue

            elif len(properties) == 4:

            
                session_id, event_type, step, timestamp = properties

                amount = None

                
            else:
                session_id, event_type,step, timestamp, amount = properties



            if session_id == "cs_B2" and event_type == "session_created":
                print("hello")
                
            if not self.validate_timestamp(timestamp):
                continue

            if amount and event_type != "session_completed":
                continue

            if event_type == "session_completed" and amount is None:
                print("hi")

                continue

            if event_type not in allowed_event_types:
                continue

            if step and step not in allowed_steps:
                continue

            if step is None and event_type == "step_viewed":
                print("jk")
                continue

            if step and event_type!="step_viewed":
                print("duf")
                continue


            new_event = event(session_id, event_type,step, timestamp, amount)

            valid_events.append(new_event)


        return valid_events


            



    def validate_timestamp(self, timestamp):

        try:

            datetime.fromisoformat(timestamp)

            return True

        except ValueError:
            return False


rows = [
    "cs_A1,session_created,,2026-09-01T10:00:00Z", # no step or amount
"cs_A1,step_viewed,contact_info,2026-09-01T10:00:05Z", # no amount
"cs_A1,step_viewed,shipping,2026-09-01T10:00:20Z", # not amount
"cs_A1,step_viewed,payment,2026-09-01T10:01:00Z", # no amount
"cs_A1,session_completed,,2026-09-01T10:02:00Z,4999", # no step and yes amount
"cs_B2,session_created,,2026-09-01T11:00:00Z", # no amount or step
"cs_B2,step_viewed,contact_info,2026-09-01T11:00:03Z", # no amount, yes step
]


test = event_stream()
valid_result = test.parse_events(rows)
# result = test.validate_timestamp("2026-09-01T10:01:00Z")

print("---------------------")
for r in valid_result:
    print("session_id: ",r.session_id, " amount: ", r.amount, "step: ", r.step)

# finished first pass at 23 mins

# took another 20 mins so finished at 42 mins. I spent about 10 mins debugging an issue. I didn't have a clear understanding of what the properties looked like when pulling from the row string. Even though step is empty is is a string in the array. There is never a time when the length would be 3 and that got me stuck for a while