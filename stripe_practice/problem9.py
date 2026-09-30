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

import csv
from datetime import datetime

allowed_event_types = {"session_created", "step_viewed", "session_completed", "session_expired"}

allowed_steps = {"contact_info", "shipping", "payment"}

class checkout_event:

    def __init__(self, session_id,event_type,step,timestamp,amount):
        self.session_id = session_id
        self.event_type = event_type
        self.step = step
        self.timestamp = datetime.fromisoformat(timestamp)
        self.amount = int (amount) if amount else None

class checkout_stream:

    def read_file(self, file_name: str):
        with open(file_name, mode='r') as file:
            reader = csv.reader(file)
            next(reader)

            valid_rows, invalid_rows = self.parse_checkout_events(reader)

        print("valid rows: ", len(valid_rows))
        print("invalid rows: ", invalid_rows)
        return valid_rows, invalid_rows

    def parse_checkout_events(self, rows: list[list[str]]):

        valid_events = []
        invalid_events = []



        for row in rows:

            if len(row) != 5:
                invalid_events.append(row)
                continue

            session_id,event_type,step,timestamp,amount = row
            print("amount: ", amount)

            if event_type not in allowed_event_types:
                invalid_events.append(row)
                continue

            if step and event_type != "step_viewed":
                invalid_events.append(row)
                continue

            if event_type == "step_viewed" and step == '':
                invalid_events.append(row)
                continue

            if not is_valid_timestamp(timestamp):
                invalid_events.append(row)
                continue

            if amount and event_type != "session_completed":
                invalid_events.append(row)
                continue

            if amount == '' and event_type == "session_completed":
                invalid_events.append(row)
                continue

            if amount and event_type == "session_completed":
                if not amount.isdigit():
                    invalid_events.append(row)
                    continue

                if not ( int (amount) >= 0):
                    invalid_events.append(row)
                    continue

            new_event = checkout_event(session_id,event_type,step,timestamp,amount)

            valid_events.append(new_event)

            # validate event type
            # validate step

            # validate valid timestamp
            # validate amount

        return valid_events, invalid_events


def is_valid_timestamp(timestamp):

    try:

        datetime.fromisoformat(timestamp)
        return True

    except ValueError:
        print("not valid timestamp")
        return False


test = checkout_stream()
test.read_file("test_data/checkout_events.csv")
# valid, invalid = test.parse_checkout_events()

# for v in valid:

#     print("id: ", v.session_id, " step: ", v.step, " event type: ", v.event_type, " amount: ", v.amount)


# print("len of valid: ", len(valid))
# print("len of invalid: ", len(invalid))

# print("invalid: ", invalid)
# at 20 min mark and still debugging. finished main pass. chekcing against test cases