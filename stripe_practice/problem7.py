"""
Parsing Drill: Payout Batch Validator

Input format:

"<payout_id>,<amount_cents>,<currency>,<destination_type>,<destination_last4>,<method>,<statement_descriptor>"

Field rules:

payout_id: must start with "po_" followed by at least one more character
amount_cents: integer, and must be strictly positive (zero or negative payouts are invalid)
currency: exactly 3 uppercase letters, one of {"USD", "EUR", "GBP"}
destination_type: one of "bank_account", "card"
destination_last4: exactly 4 characters, all digits
method: one of "standard", "instant"
statement_descriptor: 1–22 characters long, containing only letters, digits, and spaces (no other punctuation/symbols)

Cross-field rules:

If method is "instant", destination_type must be "card" (bank payouts can't be instant in this system).
If destination_type is "card", currency must be "USD" (cards only settle in USD here).
If method is "instant", amount_cents must be ≤ 500000 (instant payouts are capped at $5,000).

Task:

python
def parse_payout_rows(rows: List[str]) -> Tuple[List[dict], List[str]]:
    ...

Test data:

python
rows = [
    "po_a1,100000,USD,bank_account,1234,standard,Weekly payout",
    "po_b2,50000,USD,card,5678,instant,Instant cash out",
    "po_c3,-500,USD,bank_account,1234,standard,Bad amount",       # negative amount
    "po_d4,0,USD,bank_account,1234,standard,Zero amount",          # zero amount
    "po_e5,100000,eur,bank_account,1234,standard,lowercase cur",   # lowercase currency
    "po_f6,100000,USD,wallet,1234,standard,Bad dest type",         # invalid destination_type
    "po_g7,100000,USD,bank_account,12a4,standard,Bad last4",       # last4 has a letter
    "po_h8,100000,USD,bank_account,123,standard,Short last4",      # last4 only 3 digits
    "po_i9,100000,USD,bank_account,1234,overnight,Bad method",     # invalid method
    "po_j10,100000,USD,bank_account,1234,standard,",               # empty descriptor
    "po_k11,100000,USD,bank_account,1234,standard,This descriptor is way too long for the limit",  # >22 chars
    "po_l12,100000,USD,bank_account,1234,standard,Bad$Descriptor!", # special chars in descriptor
    "po_m13,100000,USD,bank_account,1234,instant,Instant on bank",  # instant + bank_account — invalid
    "po_n14,100000,EUR,card,1234,standard,Card needs USD",          # card + non-USD — invalid
    "po_o15,600000,USD,card,1234,instant,Too big for instant",      # instant over the cap
    "o_p16,100000,USD,bank_account,1234,standard,Missing prefix",   # doesn't start with po_
]
"""

from typing import Tuple, List

allowed_currencies = {"USD", "EUR", "GBP"}

class payout:

    def __init__(self, payout_id, amount, currency, destination_type, destination_last4, method, statement_descriptor):
        self.payout_id = payout_id
        self.amount = amount
        self.currency = currency
        self.destination_type = destination_type
        self.destination_last4 = destination_last4
        self.method = method
        self.statement_descriptor = statement_descriptor


class payout_validation:

    def parse_payout_rows(self, rows: List[str]) -> Tuple[List[dict], List[str]]:

        invalid_payout = []
        parsed_payouts = []

        for row in rows:

            properties = row.split(",")

            if len(properties) != 7:
                # invalid payout
                invalid_payout.append(row)
                continue

            payout_id, amount, currency, destination_type, destination_last4, method, statement_descriptor = properties

            # validate payout id

            if not (payout_id.startswith("po_") and len(payout_id) > 3):
                # invalid payout
                invalid_payout.append(row)
                continue

            if not self.is_number(amount):
                # invalid payout
                invalid_payout.append(row)
                continue

            if int(amount) <1:
                # invalid payout
                invalid_payout.append(row)
                continue

            if currency not in allowed_currencies:
                # invalid payout
                invalid_payout.append(row)
                continue

            if destination_type != "bank_account" and destination_type != "card":
                # invalid payout
                invalid_payout.append(row)
                continue

            if not destination_last4.isdigit() or len(destination_last4) !=4:
                # invalid payout
                invalid_payout.append(row)
                continue


            if not (method == "standard" or method == "instant"):
                # invalid payout
                invalid_payout.append(row)
                continue

            if method == "instant" and not destination_type == "card":
                # invalid payout
                invalid_payout.append(row)
                continue

            if method == "instant" and int(amount) > 500000:
                # invalid payout
                invalid_payout.append(row)
                continue

            if destination_type == "card" and not currency == "USD":
                # invalid payout
                invalid_payout.append(row)
                continue

            if not self.isvalid_descriptor(statement_descriptor):
                # invalid payout
                invalid_payout.append(row)
                continue

            
            parsed_payouts.append(row)

        return parsed_payouts, invalid_payout


            

    def is_number(self, num: str):

        try:

            integer_num = int(num)

            return True

        except ValueError:
            return False


    def isvalid_descriptor(self, statement_descriptor):

        if len(statement_descriptor) < 1 or len(statement_descriptor) > 22:
            return False

        for c in statement_descriptor:

            if c != ' ' and not c.isalnum():
                return False

        return True
            

rows = [
    "po_a1,100000,USD,bank_account,1234,standard,Weekly payout",
    "po_b2,50000,USD,card,5678,instant,Instant cash out",
    "po_c3,-500,USD,bank_account,1234,standard,Bad amount",       # negative amount
    "po_d4,0,USD,bank_account,1234,standard,Zero amount",          # zero amount
    "po_e5,100000,eur,bank_account,1234,standard,lowercase cur",   # lowercase currency
    "po_f6,100000,USD,wallet,1234,standard,Bad dest type",         # invalid destination_type
    "po_g7,100000,USD,bank_account,12a4,standard,Bad last4",       # last4 has a letter
    "po_h8,100000,USD,bank_account,123,standard,Short last4",      # last4 only 3 digits
    "po_i9,100000,USD,bank_account,1234,overnight,Bad method",     # invalid method
    "po_j10,100000,USD,bank_account,1234,standard,",               # empty descriptor
    "po_k11,100000,USD,bank_account,1234,standard,This descriptor is way too long for the limit",  # >22 chars
    "po_l12,100000,USD,bank_account,1234,standard,Bad$Descriptor!", # special chars in descriptor
    "po_m13,100000,USD,bank_account,1234,instant,Instant on bank",  # instant + bank_account — invalid
    "po_n14,100000,EUR,card,1234,standard,Card needs USD",          # card + non-USD — invalid
    "po_o15,600000,USD,card,1234,instant,Too big for instant",      # instant over the cap
    "o_p16,100000,USD,bank_account,1234,standard,Missing prefix",   # doesn't start with po_
]

test = payout_validation()
valid, invalid = test.parse_payout_rows(rows)

print("valid: ", valid)

print("invalid: ", invalid)

print("leng invalid: ", len(invalid))

# also took me 29 mins to finish the parsing