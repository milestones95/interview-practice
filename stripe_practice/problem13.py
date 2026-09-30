"""
Problem: Dispute Risk Monitoring

You're given a list of raw log lines, space-separated key=value pairs (order not guaranteed):

ts=2026-09-13T10:00:00Z merchant_id=acct_1 charge_id=ch_1 amount_cents=5000 event_type=charge_succeeded
ts=2026-09-13T10:05:00Z merchant_id=acct_1 charge_id=ch_2 amount_cents=3000 event_type=charge_succeeded
ts=2026-09-14T09:00:00Z merchant_id=acct_1 charge_id=ch_1 amount_cents=5000 event_type=charge_disputed
ts=2026-09-15T09:00:00Z merchant_id=acct_1 charge_id=ch_1 amount_cents=5000 event_type=dispute_lost
ts=2026-09-13T11:00:00Z merchant_id=acct_2 charge_id=ch_3 amount_cents=2000 event_type=charge_succeeded

Every line must have exactly these 5 keys: ts, merchant_id, charge_id, amount_cents, event_type.

Valid event_type values: charge_succeeded, charge_disputed, dispute_won, dispute_lost.

Part 1 — Parse & validate
Return valid parsed records and invalid ones (paired with a reason). A line is valid if:

Exactly 5 key=value pairs, keys are exactly the required set, no duplicate keys
merchant_id non-empty, starts with acct_
charge_id non-empty, starts with ch_
amount_cents is a non-negative integer
event_type is one of the 4 allowed values

Part 2 — Dispute rate per merchant
For each merchant, compute: total_charges = count of charge_succeeded events, total_disputes = count of charge_disputed events, and dispute_rate = total_disputes / total_charges (0.0 if no charges). Return a dict of merchant_id → dispute_rate.

Part 3 — Flag high-risk merchants with net loss
A merchant is "high-risk" if dispute_rate > 0.2. For each high-risk merchant only, compute their net loss from disputes: sum of amount_cents for every dispute_lost event belonging to that merchant. Return a dict of merchant_id → net_loss_cents, including only high-risk merchants, and only if their net loss is greater than 0 (a high-risk merchant with zero lost disputes shouldn't appear).

Assumptions, OA-style:

Lines may arrive in any order.
The same charge_id can legitimately appear in multiple events (succeeded → disputed → won/lost) — that's expected, not a duplicate to dedupe.
No = or spaces inside values.
Duplicate keys within one line = invalid line.
"""

from datetime import datetime

allowed_event_types = {"charge_succeeded", "charge_disputed", "dispute_won", "dispute_lost"}



class dispute:

    def __init__(self, timestamp, merchant_id, charge_id, amount_cents, event_type):
        self.timestamp = datetime.fromisoformat(timestamp)
        self.merchant_id = merchant_id
        self.charge_id = charge_id
        self.amount_cents = int(amount_cents)
        self.event_type = event_type


def parse_dispute_rows(rows: list[str]) -> tuple[list[dispute], list[tuple[str,str]]]:

    valid_events = []
    invalid_events = []

    for row in rows:
        split_row_properties = get_split_row_properties(row)
        if split_row_properties is None:
            invalid_events.append(("row either has duplicate keys or does not have 5 columns", row))
            continue

        timestamp, merchant_id, charge_id, amount_cents, event_type = split_row_properties

        if merchant_id == "" or not merchant_id.startswith("acct_"):
            invalid_events.append(("invalid merchant id", row))
            continue

        if charge_id == "" or not charge_id.startswith("ch_"):
            invalid_events.append(("invalid charge_id", row))
            continue


        if event_type not in allowed_event_types:
            invalid_events.append(("event type is invalid", row))
            continue

        if not validate_int(amount_cents):
            invalid_events.append(("invalid amount cents", row))
            continue

        
        new_dispute = dispute(timestamp, merchant_id, charge_id, amount_cents, event_type)

        valid_events.append(new_dispute)

    return valid_events, invalid_events



def validate_int(number):

    try:
        int(number)

        if int(number) >=0:
            return True

        return False

    except ValueError:
        print("invalid amount cents")
        return False

def get_split_row_properties(row: list[str]):

    properties = row.split()
    seen_keys = set()

    values = []

    if len(properties) != 5:
        return None

    for p in properties:

        left,right = p.split("=")

        if left in seen_keys:
            return None

        if right and right!="":
            values.append(right)

        seen_keys.add(left)

    if len(values) != 5: # if there were not 5 values provided
        return None

    return values


### part 2

def get_merchant_disputes(valid_events: list[dispute]):

    merchant_to_lost_disputes = {}
    merchant_to_charges_disputed = {}
    merchant_to_charges_succeeded = {}
    merchant_to_dispute_rate = {}
    for evt in valid_events:

        if evt.event_type == "charge_succeeded": # track number of successful charges
            merchant_to_charges_succeeded[evt.merchant_id] = merchant_to_charges_succeeded.get(evt.merchant_id, 0) + 1

        if evt.event_type == "charge_disputed": # track number of disputed charges
            merchant_to_charges_disputed[evt.merchant_id] = merchant_to_charges_disputed.get(evt.merchant_id, 0) + 1

        if evt.event_type == "dispute_lost":

            if evt.merchant_id not in merchant_to_lost_disputes:
                merchant_to_lost_disputes[evt.merchant_id] = []

            merchant_to_lost_disputes[evt.merchant_id].append(evt)


    merchant_to_dispute_rate = calculate_dispute_rate(merchant_to_charges_succeeded, merchant_to_charges_disputed)

    return merchant_to_lost_disputes, merchant_to_dispute_rate


def calculate_dispute_rate(merchant_to_charges_succeeded, merchant_to_charges_disputed) -> dict[str,float]:

    merchant_to_dispute_rate = {}

    for merchant_id, charge_succeeded_count in merchant_to_charges_succeeded.items():

        if merchant_id not in merchant_to_charges_disputed:
            merchant_to_dispute_rate[merchant_id] = 0.0

        else:
            merchant_to_dispute_rate[merchant_id] = merchant_to_charges_disputed[merchant_id] / charge_succeeded_count


    ## could also handle the edge case if somehow there was a charge dispute or charge lost but not a charge succeeded for the merchant. the rate would need to be zero still because they technically had no charges to begin with

    return merchant_to_dispute_rate


# Part 3 — Flag high-risk merchants with net loss
# A merchant is "high-risk" if dispute_rate > 0.2. For each high-risk merchant only, compute their net loss from disputes: sum of amount_cents for every dispute_lost event belonging to that merchant. Return a dict of merchant_id → net_loss_cents, including only high-risk merchants, and only if their net loss is greater than 0 (a high-risk merchant with zero lost disputes shouldn't appear).

def get_net_losses(merchant_to_dispute_rate: dict[str,float], merchant_to_lost_disputes: dict[str, list[dispute]]):

    merchant_to_net_loss = {}

    for merchant_id, dispute_rate in merchant_to_dispute_rate.items():

        if dispute_rate > 0.2:

            lost_disputes = merchant_to_lost_disputes[merchant_id]

            for d in lost_disputes:
                if d.amount_cents >0:
                    merchant_to_net_loss[merchant_id] = merchant_to_net_loss.get(merchant_id, 0 ) + d.amount_cents


    return merchant_to_net_loss








test_data = [
    "ts=2026-09-13T10:00:00Z merchant_id=acct_1 charge_id=ch_1 amount_cents=5000 event_type=charge_succeeded",
"ts=2026-09-13T10:05:00Z merchant_id=acct_1 charge_id=ch_2 amount_cents=3000 event_type=charge_succeeded",
"ts=2026-09-14T09:00:00Z merchant_id=acct_1 charge_id=ch_1 amount_cents=5000 event_type=charge_disputed",
"ts=2026-09-15T09:00:00Z merchant_id=acct_1 charge_id=ch_1 amount_cents=5000 event_type=dispute_lost",
"ts=2026-09-13T11:00:00Z merchant_id=acct_2 charge_id=ch_3 amount_cents=2000 event_type=charge_succeeded"
]


valid, invalid = parse_dispute_rows(test_data)

print("len valid: ", len(valid))

merchant_to_lost_disputes, merchant_to_dispute_rate = get_merchant_disputes(valid)

merchant_to_net_loss = get_net_losses(merchant_to_dispute_rate, merchant_to_lost_disputes)

print("merchant_to_net_loss: ", merchant_to_net_loss)

# finished part 1 at 23 mins

# finished part 2 at 41 mins so 19 mins left

# finished part 3 at 50 min mark
# spent the last 9 mins checking my work

# turns out i had some bugs. I didn't account for if the column values were in the wrong order i also didn't account for events where there wasn't a charge but there was a dispute. Those got dropped