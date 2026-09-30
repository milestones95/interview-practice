"""
Parsing Drill: Order Status Transitions

Input format:

"<order_id>,<timestamp>,<status>"
order_id: string
timestamp: unix seconds (integer)
status: one of "placed", "shipped", "delivered", "canceled"

Allowed transitions (a status can only follow specific prior statuses):

An order's first-ever event must be "placed".
"shipped" can only follow "placed".
"delivered" can only follow "shipped".
"canceled" can follow "placed" or "shipped" (but not "delivered" — you can't cancel a delivered order).
Events for a given order_id are not guaranteed to arrive in order in the input.

Task:

python
def parse_order_events(rows: List[str]) -> Tuple[List[dict], List[str]]:
    ...

Return valid parsed records (as dicts) and the raw strings of any invalid rows — bad field count, bad timestamp, unknown status, or a status that violates the allowed-transition rule given the order's actual prior status.

Test data:

python
rows = [
    "ord_1,1000,placed",
    "ord_1,1010,shipped",
    "ord_1,1020,delivered",
    "ord_2,2000,placed",
    "ord_2,2010,canceled",
    "ord_3,3010,shipped",          # never placed first — invalid
    "ord_1,1005,shipped",          # out of order relative to ord_1's other rows
    "ord_4,4000,placed",
    "ord_4,4020,delivered",        # skips "shipped" — invalid
    "ord_5,5000,placed",
    "ord_5,notanumber,shipped",    # bad timestamp
    "ord_2,2020,shipped",          # order already canceled — invalid
]
"""
valid_statuses = {"shipped", "placed", "canceled", "delivered"}

from enum import IntEnum

class order_event:

    def __init__(self, order_number, timestamp, status):
        self.order_number = order_number
        self.timestamp = timestamp
        self.status = status


class Action(IntEnum):
    placed=1
    shipped=2
    delivered=3
    canceled=4

def parse_order_rows(rows: list[str]):

    cleaned_events = []
    order_status_map = {}
    invalid_parsed_evts = []
    invalid_order_types = []



    for row in rows:

        properties = row.split(",")

        if len(properties) !=3:
            invalid_parsed_evts.append(row)
            continue

        order_number, timestamp, status = properties

        if is_valid_properties(order_number, timestamp, status):

            new_evt = order_event(order_number, timestamp, status)

            cleaned_events.append(new_evt)

        else:
            invalid_parsed_evts.append(row)

    
    sorted_evts = sorted(cleaned_events, key=lambda evt: evt.timestamp)
    # make sure order is correct


    valid_evts = []

    for evt in sorted_evts:

        if evt.order_number not in order_status_map:

            if evt.status != "placed":
                invalid_order_types.append(evt)
                continue

            order_status_map[evt.order_number] = evt.status
            valid_evts.append(evt)

        else:

            if evt.status == "canceled" and (order_status_map[evt.order_number] == "placed" or order_status_map[evt.order_number] == "shipped"):

                valid_evts.append(evt)
                order_status_map[evt.order_number] = "canceled"

            elif not Action[evt.status] > Action[order_status_map[evt.order_number]] or  not Action[evt.status]-Action[order_status_map[evt.order_number]] == 1:
                invalid_order_types.append(evt)
                continue

            else:
                valid_evts.append(evt)
                order_status_map[evt.order_number] = evt.status

    
    return valid_evts, invalid_order_types, invalid_parsed_evts


def is_valid_properties(order_number: str, timestamp: str, status: str) ->bool:

        # make sure timestamp is valid int

        if not timestamp.isdigit():
            return False
        # make sure status is valid

        if status not in valid_statuses:
            return False

        return True


test_data =  [
    "ord_1,1000,placed",
    "ord_1,1010,shipped",
    "ord_1,1020,delivered",
    "ord_2,2000,placed",
    "ord_2,2010,canceled",
    "ord_3,3010,shipped",          # never placed first — invalid
    "ord_1,1005,shipped",          # out of order relative to ord_1's other rows
    "ord_4,4000,placed",
    "ord_4,4020,delivered",        # skips "shipped" — invalid
    "ord_5,5000,placed",
    "ord_5,notanumber,shipped",    # bad timestamp
    "ord_2,2020,shipped",          # order already canceled — invalid
]

results, invalid_evts, malformed = parse_order_rows(test_data)

# print("results: ", results)

for res in results:

    print("order num: ", res.order_number, " timestamp: ", res.timestamp, " status: ", res.status)


# took me 30 mins to finish the parsing part 1