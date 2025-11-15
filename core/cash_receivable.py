# using it 
# core/cash_receivable.py
from decimal import Decimal
from datetime import date
from typing import List

class CashReceivableEntry:
    def __init__(self, account_code: str, amount: float, description: str = "Payment received from customer"):
        self.account_code = account_code
        # Use Decimal(str(value)) for proper conversion to avoid float precision issues
        self.amount = Decimal(str(amount))
        self.description = description

class CashReceivable:
    def __init__(self, account_code: "10000001", cr_date: date):
        self.voucher_id = None  # assigned by DB
        self.account_code = account_code  # Default Cash/Bank account code
        self.date = cr_date
        self.entries: List[CashReceivableEntry] = []
        # Initialize as Decimal('0') instead of Decimal(0)
        self.total_amount = Decimal('0')

    def add_entry(self, entry: CashReceivableEntry):
        self.entries.append(entry)
        self.calculate_totals()

    def remove_entry_by_index(self, index):
        if 0 <= index < len(self.entries):
            del self.entries[index]
            self.calculate_totals()

    def calculate_totals(self):
        # Use entry.amount to maintain consistency with Decimal values
        self.total_amount = sum(entry.amount for entry in self.entries)