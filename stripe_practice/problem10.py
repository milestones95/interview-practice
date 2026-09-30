"""
Problem: Checkout Funnel Abandonment

Stripe Checkout emits events as a customer moves through a checkout session. You're given a stream of events, each with:

{
  "session_id": "cs_123",
  "step": "cart" | "shipping" | "payment" | "confirmation",
  "timestamp": "2026-09-13T10:15:00Z"
}

The checkout flow always progresses in this fixed order: cart → shipping → payment → confirmation. A session is considered abandoned at step X if the last event recorded for that session is step X, and X is not confirmation.

Part 1: Given a list of these events (not necessarily in timestamp order, and a session's events may be interleaved with other sessions' events in the stream), write a function that returns a count of how many sessions were abandoned at each step.

That's the full spec for Part 1 — I'm intentionally not telling you what Part 2 will ask yet, since figuring out how to structure your solution so it could extend is part of the exercise. (There will be a Part 2 that asks for conversion rates between steps, in the spirit of your notes.)
"""

from datetime import datetime


class checkout_event:

    def __init__(self, session_id, step, timestamp):
        self.session_id = session_id
        self.step = step
        self.timestamp = datetime.fromisoformat(timestamp)

allowed_steps = {"cart", "shipping", "payment" , "confirmation"}

def parse_events(events):

    # make sure to sort events by timestamp

    # track the last step for each session id

    # also have a hashmap for each step to track the count

    valid_events = []
    invalid_events = []


    for evt in events:

        if evt["step"] not in allowed_steps:
            invalid_events.append(evt)
            continue

        new_event = checkout_event(evt["session_id"], evt["step"], evt["timestamp"])
        valid_events.append(new_event)

    
    sorted_valid_events = sorted(valid_events, key = lambda evt: evt.timestamp)

    return sorted_valid_events


def get_session_events(sorted_valid_events):

    session_to_event = {}

    for se in sorted_valid_events:

        if se.session_id not in session_to_event:
            session_to_event[se.session_id] = []

        session_to_event[se.session_id].append(se)

    return session_to_event


def get_step_map(session_events: dict[str, list[checkout_event]]):
    step_count = {}

    for k,v in session_events.items():

        if v[(len(v)-1)].step != "confirmation":
            step_count[v[(len(v)-1)].step] = step_count.get(v[(len(v)-1)].step,0) + 1



    return step_count



def get_results(events):

    sorted_valid_events = parse_events(events)

    session_events = get_session_events(sorted_valid_events)

    step_map = get_step_map(session_events)

    print("step map: ", step_map)

    return step_map





test_data = [
  {"session_id": "cs_123", "step": "cart", "timestamp": "2026-09-13T10:15:00Z"},
  {"session_id": "cs_456", "step": "shipping", "timestamp": "2026-09-13T10:16:00Z"},
  {"session_id": "cs_123", "step": "payment", "timestamp": "2026-09-13T10:17:00Z"},
    # {"session_id": "cs_456", "step": "payment", "timestamp": "2026-09-13T10:16:02Z"},
    # {"session_id": "cs_456", "step": "confirmation", "timestamp": "2026-09-13T10:16:03Z"}

  ]


# session_map, step_map = parse_events(test_data)
results = get_results(test_data)

# print("session_map: ", session_map)
print("step_map: ", results)

# took 21 mins