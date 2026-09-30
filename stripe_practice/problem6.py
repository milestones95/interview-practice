"""
Parsing Drill: Card Authorization Row Validator

Input format:

"<txn_id>,<amount_cents>,<currency>,<country>,<cvv_result>,<avs_result>,<card_type>"

Field rules:

txn_id: must start with the literal prefix "txn_" followed by at least one more character
amount_cents: integer (as a string in the row)
currency: exactly 3 uppercase letters, and must be one of {"USD", "EUR", "GBP", "CAD", "JPY"}
country: exactly 2 uppercase letters
cvv_result: one of "pass", "fail", "unavailable"
avs_result: one of "pass", "fail", "unavailable", "partial"
card_type: one of "charge", "refund"

Cross-field rules (this is the "tricky" part — these check one field against another, not just one field in isolation):

If card_type is "refund", amount_cents must be negative. If card_type is "charge", amount_cents must be positive.
If card_type is "refund", both cvv_result and avs_result must be "unavailable" (refunds don't re-run card checks).
If currency is "JPY", amount_cents must be evenly divisible by 100 (JPY is a special case here for this exercise).

Task:

python
def parse_transaction_rows(rows: List[str]) -> Tuple[List[dict], List[str]]:
    ...

Test data:

python
rows = [
    "txn_a1,500,USD,US,pass,pass,charge",
    "txn_b2,-500,USD,US,unavailable,unavailable,refund",
    "txn_c3,1000,JPY,JP,pass,pass,charge",
    "txn_d4,500,usd,US,pass,pass,charge",          # lowercase currency
    "txn_e5,500,USD,USA,pass,pass,charge",          # 3-letter country
    "txn_f6,abc,USD,US,pass,pass,charge",           # non-numeric amount
    "txn_g7,500,USD,US,maybe,pass,charge",          # invalid cvv_result
    "txn_h8,500,USD,US,pass,perhaps,charge",        # invalid avs_result
    "txn_i9,500,USD,US,pass,pass,lease",            # invalid card_type
    "txn_j10,500,USD,US,pass,pass,refund",          # refund with positive amount
    "txn_k11,-500,USD,US,pass,pass,refund",         # refund but cvv/avs not unavailable
    "txn_l12,150,JPY,JP,pass,pass,charge",          # JPY not divisible by 100
    "missing_fields,500,USD",                       # too few fields
    "txn_m13,500,EUR,fr,pass,pass,charge",           # lowercase country
    "tx_n14,500,USD,US,pass,pass,charge",           # doesn't start with txn_
]
"""


# class transaction:

#     # def __init__(self, transaction_id, amount, currency, country, cvv_result, avs_result, card_type):



class transaction_check:

    def parse_transactions(self,rows: list[str]):

        valid_txns = []
        invalid_txns = []

        for row in rows:

            properties = row.split(",")

            if len(properties) != 7:
                # invalid txn
                invalid_txns.append(txn_id)
                continue

            txn_id, amount, currency, country, cvv, avs, card_type = properties

            # check transaction id format

            if "txn" not in txn_id:
                # invalid ticket
                invalid_txns.append(txn_id)
                continue

            left, right = txn_id.split("_")
            print("left: ", left, " right: ", right)

            if left != "txn" or right is None:
                # invalid ticket
                invalid_txns.append(txn_id)
                continue
            print("his")

            if not is_number(amount):
                # invalid ticket
                # print("not valid t icket: ", txn_id)
                invalid_txns.append(txn_id)
                continue
            if currency not in {"USD", "EUR", "GBP", "CAD", "JPY"}:
                # invalid ticket
                invalid_txns.append(txn_id)
                continue

            if currency == "JPY" and int(amount) % 100 != 0:
                 # invalid ticket
                invalid_txns.append(txn_id)
                continue

            if len(country) !=2 or not country.isupper():
                # invalid ticket
                invalid_txns.append(txn_id)
                continue

            if cvv not in {"pass", "fail", "unavailable"}:
                # invalid ticket
                invalid_txns.append(txn_id)
                continue

            if avs not in {"pass", "fail", "unavailable", "partial"}:
                # invalid ticket
                invalid_txns.append(txn_id)
                continue

            if card_type not in {"charge", "refund"}:
                # invalid ticket
                invalid_txns.append(txn_id)
                continue

            if (card_type == "charge" and not int(amount)>0) or (card_type == "refund" and not int(amount)<0) or (card_type == "refund" and cvv !="unavailable") or (card_type == "refund" and avs !="unavailable"):
                invalid_txns.append(txn_id)
                continue


            valid_txns.append(txn_id)

        return valid_txns, invalid_txns



def is_number(number: str):

    try:

        int(number)

        return True

    except ValueError:
        print("not a number")

        return False

rows = [
    "txn_a1,500,USD,US,pass,pass,charge",
    "txn_b2,-500,USD,US,unavailable,unavailable,refund",
    "txn_c3,1000,JPY,JP,pass,pass,charge",
    "txn_d4,500,usd,US,pass,pass,charge",          # lowercase currency
    "txn_e5,500,USD,USA,pass,pass,charge",          # 3-letter country
    "txn_f6,abc,USD,US,pass,pass,charge",           # non-numeric amount
    "txn_g7,500,USD,US,maybe,pass,charge",          # invalid cvv_result
    "txn_h8,500,USD,US,pass,perhaps,charge",        # invalid avs_result
    "txn_i9,500,USD,US,pass,pass,lease",            # invalid card_type
    "txn_j10,500,USD,US,pass,pass,refund",          # refund with positive amount
    "txn_k11,-500,USD,US,pass,pass,refund",         # refund but cvv/avs not unavailable
    "txn_l12,150,JPY,JP,pass,pass,charge",          # JPY not divisible by 100
    "missing_fields,500,USD",                       # too few fields
    "txn_m13,500,EUR,fr,pass,pass,charge",           # lowercase country
    "tx_n14,500,USD,US,pass,pass,charge",           # doesn't start with txn_
]


test = transaction_check()
valid_txns, invalid_txns = test.parse_transactions(rows)


print("result: ", valid_txns)
print("invalid: ", invalid_txns)
        
# took 30 mins