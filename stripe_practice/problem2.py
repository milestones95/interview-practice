"""
Webhook Delivery Log Analyzer

Background: Stripe delivers webhook events to merchant endpoints. If a delivery attempt fails, Stripe retries it. Each attempt gets logged as a row.

Input format: A list of strings, each formatted as:

"<endpoint_id>,<event_id>,<attempt_number>,<timestamp>,<result>"
endpoint_id: alphanumeric string identifying the merchant's webhook URL
event_id: alphanumeric string; the same event_id may appear multiple times (one row per retry attempt) if delivery to that endpoint keeps failing
attempt_number: positive integer, starts at 1 and increments with each retry for that event
timestamp: unix seconds (integer)
result: one of "success", "failure", "timeout"

Business rule: Stripe retries a failed/timed-out delivery up to 3 attempts total. If attempt 3 still isn't "success", the event is permanently failed for that endpoint.

Example rows:

"ep_1,evt_a,1,1000,failure"
"ep_1,evt_a,2,1010,success"
"ep_1,evt_b,1,1005,failure"
"ep_1,evt_b,2,1015,failure"
"ep_1,evt_b,3,1025,failure"
"ep_2,evt_c,1,2000,success"
"ep_1,evt_d,1,3000,timeout"
Part 1

Write parse_delivery_rows(rows: List[str]) -> Tuple[List[dict], List[str]] — parse and validate, splitting into valid records and the raw strings of invalid ones (bad field count, non-integer attempt_number, attempt_number outside 1–3, unknown result, etc.). As before, structure your validation so a new rule is cheap to add later.

Part 2

Write find_final_outcomes(rows: List[str]) -> Dict[str, str] — for each event_id, determine its final outcome as one of "delivered" (some attempt succeeded), "failed" (reached attempt 3 without success), or "pending" (fewer than 3 attempts logged so far, none successful yet). Only use valid rows.

Part 3

Write endpoint_success_rate(rows: List[str]) -> Dict[str, float] — for each endpoint_id, what fraction of its distinct events ended up "delivered"? ("pending" events count in the denominator but not the numerator — they haven't succeeded yet.)
"""


class event:

    def __init__(self, ep, evt_id, attempt_number,timestamp,status):
        self.timestamp = timestamp
        self.id = evt_id
        self.attempt_number = attempt_number
        self.status = status
        self.endpoint = ep


class logging_system:

    def parse_events(self, rows: list[str]):
        
        valid_events = []
        for evt in rows:

            if not self.is_valid_event(evt):
                print("not valid event: ")
                continue

            valid_events.append(evt)

        return valid_events

    
    def find_final_outcomes(self, rows: list[str]):

        event_count = {}
        event_status = {}
        for row in rows:
            properties = row.split(",")
            print("row: ", row)
            ep, evt_id, attempt_number, timestamp, status = properties
            if status == "success":
                event_status[evt_id] = "delivered"
                event_count[evt_id] = event_count.get(evt_id, 0) + 1

            if evt_id not in event_status:
                event_status[evt_id] = "pending"
                event_count[evt_id] = event_count.get(evt_id, 0) + 1
            # if the event is not already successful then increment the count
            else:
                if not event_status.get(evt_id) == "delivered" and event_count.get(evt_id) < 3:
                    event_count[evt_id] = event_count.get(evt_id, 0) + 1

                    if event_count[evt_id] == 3:
                        event_status[evt_id] = "failed"


        print("event status: ", event_status)

        return event_status


    def endpoint_success_rate(self,rows: list[str], event_status) -> dict[str, float]:

        endpoint_map = {}

        success_map = {}

        for row in rows:

            properties = row.split(",")
            ep, evt_id, attempt_number, timestamp, status = properties

            if ep not in endpoint_map:
                endpoint_map[ep] = set()

            endpoint_map[ep].add(evt_id)



        for ep, events in endpoint_map.items():

            num_of_unique_events = len(events)
            count_successes = 0

            for evt_id in events:

                if event_status[evt_id] == "delivered":
                    count_successes+=1

            

            success_map[ep] = count_successes / num_of_unique_events

        
        print("success map: ", success_map)

        return success_map




    
    def is_valid_event(self, evt: str):

        properties = evt.split(",")

        if len(properties) != 5:
            return False
        ep, evt_id, attempt_number, timestamp, status = properties

        if "_" in ep:
            ep_left, ep_right = ep.split("_",1)
            # do validation

            # if not alnum
            if not ep_left.isalnum() or not ep_right.isalnum():
                print("hi")
                return False

        else:
            return False

        if "_" in evt_id:
            evt_id_left, evt_id_right = evt_id.split("_",1)
            # do validation

            # if not alnum
            if not evt_id_left.isalnum() or not evt_id_right.isalnum():
                print("hi")
                return False

        if not self.is_valid_number(attempt_number):
            print("hola")

            return False

        return True


    def is_valid_number(self, attempt_num):

        try:

            new_num = int(attempt_num)
            isinstance(new_num, int)

            if new_num >0 and new_num<4:
                return True

            return False

        except ValueError:
            print("attempt num is not a valid number")

            return False

        


test_data = [
    "ep_1,evt_a,1,1000,failure",
    "ep_1,evt_a,2,1010,success",
    "ep_1,evt_b,1,1005,failure",
    "ep_1,evt_b,2,1015,failure",
    "ep_1,evt_b,3,1025,failure",
    "ep_2,evt_c,1,2000,success",
    "ep_1,evt_d,1,3000,timeout",
    "ep_3,evt_g,1,1000",
    "*#f,evt_g,1,1000",
    "*#f,k[2,1,1000,timeout",
    "ep_3,evt_g,3,1000,success",
    "ep_1,evt_d,4,3000,timeout"
]

test = logging_system()
valid_evts = test.parse_events(test_data)

print("valid events: ", valid_evts)
event_status_map = test.find_final_outcomes(valid_evts)

results = test.endpoint_success_rate(valid_evts, event_status_map)

# took 13 mins to plan and then it took me until 37 min mark to finish the parsing and debug for part 1
# did part 1 and part 2 and finished at 1 hour and 6 mins
# did part 3 at 1 hour 20