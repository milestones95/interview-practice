"""
Checkout Funnel Analyzer

Background: Stripe Checkout sessions emit events as users move through checkout. Each event is a string representing one step for one session.

Input format: A list of event strings, each formatted as:

"<session_id>,<step>,<timestamp>,<status>"
session_id: alphanumeric string
step: one of "cart", "shipping", "payment", "confirmation" — steps always occur in this order for a given session
timestamp: integer (unix seconds)
status: one of "started", "completed"

Example events:

"sess_1,cart,1000,started"
"sess_1,cart,1005,completed"
"sess_1,shipping,1006,started"
"sess_1,shipping,1010,completed"
"sess_1,payment,1012,started"
"sess_2,cart,2000,started"
"sess_2,cart,2003,completed"
"sess_2,shipping,2004,started"
"sess_3,cart,2000,started"
"sess_4,cart,2000,started"
"sess_4,cart,2000,completed"
"sess_4,shipping,1006,started"
"sess_4,shipping,1006,completed"
"sess_4,payment,1012,started"
"sess_4,payment,1012,completed"
"sess_4,confirmation,1012,started"
"sess_4,confirmation,1012,completed"








Part 1

Write a function parse_events(events: List[str]) -> ??? that parses the raw strings into a structured form of your choosing. (This is your chance to make a design decision — think about what shape will make Part 2 easy.)

Part 2

Write find_abandoned_sessions(events: List[str]) -> Dict[str, str] that returns a mapping of session_id -> step for every session that never reached "confirmation completed". The step returned should be the last step the session started but never completed (i.e., where they dropped off).

A session is only "abandoned" if it has no further activity after its last started-but-not-completed step.
Assume the event list is not necessarily in chronological or session-grouped order.
Part 3

Write conversion_rates(events: List[str]) -> Dict[str, float] that computes, for each step, what fraction of sessions that reached that step went on to complete it. Return something like:

python
{"cart": 0.95, "shipping": 0.88, "payment": 0.71, "confirmation": 0.99}
"""

# part 1 we need to parse the rows and create a adjacency list for graph
# we need to check to see where the last step that was reached
# we also need to keep checking to see if they go on to get that step completed

from enum import Enum 




class Event:

    def __init__(self, session_id, step: str, status: str, timestamp):
        self.session_id = session_id
        self.step = step
        self.status = status
        self.timestamp = int(timestamp)

class checkout_funnel:

    def __init__(self):
        self.event_map = {}


    def parse_events(self, events: list[str]):

        for evt in events:
            properties = evt.split(",")
            session_id, step, timestamp, status = properties
            print("timestamp: ", timestamp)

            new_event = Event(session_id, step, status, timestamp)

            if session_id not in self.event_map:
                self.event_map[session_id] = []


            self.event_map[session_id].append(new_event)


        for k,v in self.event_map.items():

            self.event_map[k] = sorted(self.event_map[k], key=lambda evt: evt.timestamp)

        print("events: ", self.event_map)


    def get_status_value(self, status): 

        if status == "cart":
            return 1

        elif status == "shipping":
            return 2
        elif status == "payment":
            return 3

        elif status == "confirmation":
            return 4

        else:
            return -1


    def find_abandoned_sessions(self):

        # we need to go through each session first
        # and look at the neighbors. 
        # we need to know what the largest value is that was completed and save that


        items = self.event_map.items()
        abandoned_sessions = {}
        for session_id, _ in items:
            print("session_id: " , session_id)
            latest_step = self.find_last_step(session_id)
            if latest_step:
                abandoned_sessions[session_id] = latest_step

        print("abandoned sessions: ", abandoned_sessions)
        return abandoned_sessions


    def find_conversion_rate(self):

        # need to know how many times the step was started
        # then need to know how many times the step was completed

        # map for steps
        step_initially_seen = {}
        steps = ["cart", "shipping", "payment", "confirmation"]

        steps_after_processed = {}

        for step in steps:
            step_initially_seen[step] = 0

        
        # how many times the step was seen
        for session_id, neighbors in self.event_map.items():
            
            for neighbor in neighbors:
                if neighbor.status == "started":
                    step_initially_seen[neighbor.step] = step_initially_seen.get(neighbor.step,0)+1


        


        print("steps seen: ",step_initially_seen)



        # how many times the step was completed

        abandoned_sessions = self.find_abandoned_sessions()

        for session, step in abandoned_sessions.items():
            steps_after_processed[step] = steps_after_processed.get(step, 0) + 1

        print("steps_after_processed: ", steps_after_processed)


        step_conversion = {}

        for step, count in step_initially_seen.items():
            print("count: ", count)
            if count == 0:
                step_conversion[step] = 0.0

            else:
                print("")
                step_conversion[step] = (count - steps_after_processed.get(step,0)) / count

        print("conversion: ", step_conversion)


    
    def find_last_step(self, session_id):
        latest_step_value = 0
        latest_step = "cart"
        evts = self.event_map[session_id]

        
        abandoned_map = {}
        print("session: ", session_id)
        for evt in evts:
            print("evt: ", evt.step, " status: ", evt.status)
            if evt.status =="completed" and evt.step == latest_step:
                latest_step = None

            if evt.status =="started" and self.get_status_value(evt.step) > latest_step_value:
                latest_step_value = self.get_status_value(evt.step)
                latest_step = evt.step


            if evt.step == "confirmation" and evt.status == "completed":
                return None

        
        return latest_step





test_list = ["sess_1,cart,1000,started",
"sess_1,cart,1005,completed",
"sess_1,shipping,1006,started",
"sess_1,shipping,1010,completed",
"sess_1,payment,1012,started",
"sess_2,cart,2000,started",
"sess_2,cart,2003,completed",
"sess_2,shipping,2004,started",
"sess_3,cart,2000,started",
"sess_4,cart,2000,started",
"sess_4,cart,2001,completed",
"sess_4,shipping,1006,started",
"sess_4,shipping,1009,completed",
"sess_4,payment,1012,started",
"sess_4,payment,1013,completed",
"sess_4,confirmation,1012,started",
"sess_4,confirmation,1014,completed",
"sess_5,cart,2000,started",
"sess_5,cart,2003,completed",
"sess_5,shipping,2004,started",
"sess_5,shipping,2004,completed",
"sess_6,cart,3000,completed",
"sess_6,cart,2003,started"]


test = checkout_funnel()
test.parse_events(test_list)
test.find_abandoned_sessions()

test.find_conversion_rate()

# struggling how to use enums properly
# also started off trying to use graph adjacent when not sure if i should have. Once i started trying to implement the graph data structure it didn't feel like it was working so i pivoted to interating over the array for each step
# did part 1 and part 2 in 57 mins
# part 3 where i'm at is 1 hour and 20 mins.