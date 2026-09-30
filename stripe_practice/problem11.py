"""
Validate Stripe Payout CSV Rows

You're given a list of raw CSV lines (strings) representing payout records. Each line has this format:

payout_id,merchant_id,amount_cents,currency,status

Example:

po_1001,acct_88,150000,usd,paid
po_1002,acct_12,-500,usd,failed
po_1003,,200000,eur,paid
po_1004,acct_55,abc,usd,pending

A row is valid if all of the following hold:

Exactly 5 fields (no more, no fewer)
payout_id is non-empty and starts with po_
merchant_id is non-empty and starts with acct_
amount_cents is a valid non-negative integer
currency is one of: usd, eur, gbp
status is one of: paid, pending, failed

Write a function that takes the list of raw lines and returns two lists: the valid rows (parsed into a clean structure of your choice) and the invalid rows (paired with a reason string for why each failed).
"""

from typing import Tuple, Dict

class payout:

    def __init__(self, payout_id,merchant_id,amount_cents,currency,status):
        self.payout_id = payout_id
        self.merchant_id = merchant_id
        self.amount_cents = int(amount_cents)
        self.currency = currency
        self.status = status

valid_currencies = {"usd", "eur", "gbp"}
valid_statuses = {"paid", "pending", "failed"}

def parse_csv_rows(rows: list[str])-> Tuple[list[payout], list[Tuple[str,str]]]:

    # parse the rows and return valid and invalid rows

    invalid_rows = []
    valid_rows = []

    for row in rows:

        properties = [p.strip() for p in row.split(",")]

        if len(properties) != 5:
            invalid_rows.append((row, "more than 5 columns in row"))
            continue

        payout_id,merchant_id,amount_cents,currency,status = properties

        if not (payout_id.startswith("po_") and len(payout_id) > 3):
            invalid_rows.append((row, "payout id is invalid"))
            continue

        if not (merchant_id.startswith("acct_") and len(merchant_id) > 5):
            invalid_rows.append((row, "merchant id is invalid"))
            continue

        if not is_valid_int(amount_cents):
            invalid_rows.append((row, "amount cents is not a int"))
            continue


        if not int(amount_cents) >=0:
            invalid_rows.append((row, "amount cents is negative"))
            continue

        if currency not in valid_currencies:
            invalid_rows.append((row, "invalid currency"))
            continue


        if status not in valid_statuses:
            invalid_rows.append((row, "invalid status"))
            continue


        new_payout = payout(payout_id,merchant_id,amount_cents,currency,status)

        valid_rows.append(new_payout)

    return valid_rows, invalid_rows


def is_valid_int(number):

    try:
        int(number)
        return True

    except ValueError:
        print("not valid number")
        return False
        


test_data = [
    "po_1001,acct_88,150000,usd,paid",
"po_1002,acct_12,-500,usd,failed",
"po_1003,,200000,eur,paid",
"po_1004,acct_55,abc,usd,pending"
]


valid, invalid = parse_csv_rows(test_data)

for v in valid:

    print("id: ", v.payout_id)


for k,v in invalid:
    print("k: ", k, " reason: ", v)


# finished at 17 mins and 30 seconds
# need to think about edge cases before i finish finish