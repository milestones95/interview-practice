"""
Practice Problem: Validate a Transaction CSV

You're given a CSV string (rows separated by \n, fields by ,) representing payment transactions. The header row is:

transaction_id,amount,currency,status,customer_email

Write a function that parses the CSV and returns a list of valid transactions, plus a list of validation errors (row number + reason) for any invalid rows.

Validation rules:

transaction_id — must be non-empty, alphanumeric only
amount — must parse as a positive integer (represents cents; no decimals, no negative values, no leading zeros unless the value is exactly "0")
currency — must be exactly 3 uppercase letters (e.g. USD, EUR)
status — must be one of: succeeded, pending, failed, refunded
customer_email — must contain exactly one @ with non-empty content before and after it, and the part after @ must contain a .
A row with the wrong number of fields is invalid (report it, don't crash)
Fields may be wrapped in double quotes if they contain commas (basic CSV quoting) — e.g. "Smith, John" — handle this rather than naively splitting on ,
"""

import csv
from enum import Enum

class Status(Enum):
    SUCCEEDED = "succeeded"
    PENDING = "pending"
    FAILED = "failed"
    REFUNDED = "refunded"

class transaction_list:

    def __init__(self):
        self.header = []
        self.transaction_lines = []


    def is_valid_transaction_id(self, transaction_id):

        if transaction_id is None:
            return False

        for c in transaction_id:
            if not c.isalnum():
                return False

        return True

    def amount_is_valid(self, amount):

        try:
            int(amount)
            return True

        except ValueError:
            print("amount is not a valid int")
            return False

    def currency_is_valid(self, currency):

        if len(currency) != 3:
            return False

        if not currency.isupper():
            return False

        return True

    def is_valid_status(self, status):
        try:
            current_status = Status(status)
            return True

        except ValueError:
            print("status for this transaction not supported")
        return False

    def get_valid_transaction_list(self, file_name):

        file_obj = read_csv(file_name)
        header = file_obj.get("header")
        transaction_lines = file_obj.get("lines")
        valid_transactions = []

        for row in transaction_lines:

            if len(header) != len(row):
                continue
            if not self.is_valid_transaction_id(row[0]):
                continue

            transaction_id,amount,currency,status,customer_email = row

            if not self.amount_is_valid(amount): 
                continue

            if not self.currency_is_valid(currency):
                continue

            if not self.is_valid_status(status):
                continue

            valid_transactions.append(row)

        print(header)
        print("valid transactions: ",valid_transactions )



def read_csv(file_name):
    with open(file_name, mode='r', newline = '') as file:

        reader = csv.reader(file)
        # length_reader = len(reader)

        lines = list(reader)
        header = lines[0]
    
        return {
            "lines": lines[1:],
            "header": header
        }


test = transaction_list()
test.get_valid_transaction_list("test_data/transactions.csv")