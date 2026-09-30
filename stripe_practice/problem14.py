"""
Problem: Webhook Delivery Monitoring

You're given raw log lines, pipe-delimited, fixed field order:

timestamp|endpoint_id|event_id|attempt_number|status

Example:

2026-09-13T10:00:00Z|we_1|evt_1|1|failed
2026-09-13T10:01:00Z|we_1|evt_1|2|delivered
2026-09-13T10:02:00Z|we_1|evt_2|1|failed
2026-09-13T10:03:00Z|we_1|evt_2|2|failed
2026-09-13T10:04:00Z|we_2|evt_3|1|delivered

status is one of: delivered, failed, timed_out.

Part 1 — Parse & validate
Return valid parsed records and invalid ones (paired with a reason). A line is valid if:

Exactly 5 pipe-delimited fields
endpoint_id non-empty, starts with we_
event_id non-empty, starts with evt_
attempt_number is a positive integer (≥ 1, not 0)
status is one of the 3 allowed values

Part 2 — Delivery success rate per endpoint
The same (endpoint_id, event_id) pair can appear multiple times — one row per delivery attempt for that event. For each distinct event, its final outcome is the status of its highest attempt_number (i.e., the last attempt made). Using final outcomes only, compute per endpoint: delivery_success_rate = (distinct events whose final outcome is delivered) / (total distinct events for that endpoint). Return endpoint_id → delivery_success_rate.

Part 3 — Flag at-risk endpoints and wasted attempts
An endpoint is "at risk" if delivery_success_rate < 0.5. For at-risk endpoints only, compute wasted attempts: the total count of all attempt rows (not just the final one) belonging to events whose final outcome was not delivered. Return endpoint_id → wasted_attempts, including only at-risk endpoints where wasted_attempts > 0.

Assumptions, OA-style:

Lines may arrive out of order — both across endpoints/events and in attempt_number order within the same event.
Assume no two rows for the same (endpoint_id, event_id) share the same attempt_number.
No | characters inside field values.
"""

from datetime import datetime

allowed_statuses = {"delivered", "failed", "timed_out"}

class event:

    def __init__(self, timestamp, endpoint_id, event_id, attempt_number, status): 
        self.timestamp = datetime.fromisoformat(timestamp)
        self.endpoint_id = endpoint_id
        self.event_id = event_id
        self.attempt_number = int(attempt_number)
        self.status = status



def parse_events(rows: list[str]): 

    valid_events = []
    invalid_events = []


    for row in rows:

        properties = row.split("|")
        if len(properties) != 5:
            invalid_events.append((row, "row does not have 5 values"))
            continue

        timestamp, endpoint_id, event_id, attempt_number, status = properties

        if not endpoint_id or  endpoint_id == '' or not endpoint_id.startswith("we_"):
            invalid_events.append((row, "invalid endpoint id"))
            continue

        if not event_id or  event_id == '' or not event_id.startswith("evt_"):
            invalid_events.append((row, "invalid event id"))
            continue

        if not is_valid_int(attempt_number):
            invalid_events.append((row, "attempt number is not an int"))
            continue

        if not int(attempt_number) >= 1:
            invalid_events.append((row, "attempt number is not positive integer"))
            continue

        if status not in allowed_statuses:
            invalid_events.append((row, "invalid status type"))
            continue

        new_event = event(timestamp, endpoint_id, event_id, attempt_number, status)

        valid_events.append(new_event)


    return valid_events, invalid_events



"""
Part 2 — Delivery success rate per endpoint
The same (endpoint_id, event_id) pair can appear multiple times — one row per delivery attempt for that event. For each distinct event, its final outcome is the status of its highest attempt_number (i.e., the last attempt made). Using final outcomes only, compute per endpoint: delivery_success_rate = (distinct events whose final outcome is delivered) / (total distinct events for that endpoint). Return endpoint_id → delivery_success_rate.

"""
def get_delivery_success(valid_events: list[event]):

    endpoint_event_to_last_event = {}
    endpoint_to_success_rate = {}
    endpoint_to_event_count = {}
    endpoint_to_success_count = {}
    endpoint_to_all_events = {}

    for evt in valid_events:

        if evt.endpoint_id not in endpoint_to_all_events:
            endpoint_to_all_events[evt.endpoint_id] = []

        endpoint_to_all_events[evt.endpoint_id].append(evt)

        # we need to get the last attempt for each endpoint event combo. Use a tuple of (endpoint, event_id)
        # if the attempt number is greater than the current attempt number, then set the event the be the last event

        # if the k-v pair doesn't exist yet, consider it to be the latest
        key = (evt.endpoint_id, evt.event_id)
        print("key: ", key)
        if key not in endpoint_event_to_last_event:
            endpoint_event_to_last_event[key] = evt


        # otherwise, we need to compare the attempt number to know if it happened later than the current
        else:
            print("attempt number: ", evt.attempt_number)
            print("existing  number: ", endpoint_event_to_last_event[(evt.endpoint_id, evt.event_id)].attempt_number)


            if  evt.attempt_number > endpoint_event_to_last_event[(evt.endpoint_id, evt.event_id)].attempt_number:
                endpoint_event_to_last_event[(evt.endpoint_id, evt.event_id)] = evt

        print("len of endpoint_event_to_last_event: ", len(endpoint_event_to_last_event))


        for k,v in endpoint_event_to_last_event.items():
            ep1, ev1 = k
            print("endpoint: ", ep1, " event id: ", ev1, " attempt: ", v.attempt_number, " status: ", v.status)


        # get delivery success rate

        for endpoint_event, final_event in endpoint_event_to_last_event.items():

            ep_id, ev_id = endpoint_event

            if final_event.status =="delivered":
                endpoint_to_success_count[ep_id] = endpoint_to_success_count.get(ep_id, 0) + 1

            endpoint_to_event_count[ep_id] = endpoint_to_event_count.get(ep_id, 0) + 1


        
        for endpoint_id, count in endpoint_to_event_count.items():

            if endpoint_id not in endpoint_to_success_count:
                endpoint_to_success_rate[endpoint_id] = 0.0

            else:
                endpoint_to_success_rate[endpoint_id] = endpoint_to_success_count[endpoint_id] / endpoint_to_event_count[endpoint_id]


    return endpoint_to_success_rate, endpoint_event_to_last_event, endpoint_to_event_count



        



"""
Part 3 — Flag at-risk endpoints and wasted attempts
An endpoint is "at risk" if delivery_success_rate < 0.5. For at-risk endpoints only, compute wasted attempts: the total count of all attempt rows (not just the final one) belonging to events whose final outcome was not delivered. Return endpoint_id → wasted_attempts, including only at-risk endpoints where wasted_attempts > 0.
"""

def at_risk_endpoints(endpoint_to_success_rate, endpoint_event_to_last_event):

    at_risk_endpoint_to_wasted_attempts = {}

    for k,v in endpoint_to_success_rate.items():

        if v < 0.5:
            at_risk_endpoint_to_wasted_attempts[k] = at_risk_endpoint_to_wasted_attempts.get(k, 0) + endpoint_event_to_last_event[k].attempt_number


    return at_risk_endpoint_to_wasted_attempts




def is_valid_int(number):

    try:
        int(number)
        return True

    except ValueError:
        return False



test_data = [
    "2026-09-13T10:00:00Z|we_1|evt_1|1|failed",
"2026-09-13T10:01:00Z|we_1|evt_1|2|delivered",
"2026-09-13T10:02:00Z|we_1|evt_2|1|failed",
"2026-09-13T10:03:00Z|we_1|evt_2|2|failed",
"2026-09-13T10:03:01Z|we_1|evt_2|abc|failed",
"2026-09-13T10:04:00Z|we_2|evt_3|1|delivered"
]

valid, invalid = parse_events(test_data)

for v in valid:

    print("endpoint: ", v.endpoint_id, " eventid: ", v.event_id, " attempt: ", v.attempt_number)


endpoint_to_success_rate, endpoint_event_to_last_event = get_delivery_success(valid)

print("success rate: ", endpoint_to_success_rate)


# finished part 1 in 18 mins

# starting part 2 at 18 min mark

# finished part 2 at 40 min mark
# wasted a lot of time debugging because my return statement was indented and exited early