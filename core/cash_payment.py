# using it 
# core/cash_payable.py
from decimal import Decimal
from datetime import date
from typing import List

class CashPayableEntry:
    def __init__(self, account_code: str, amount: float, description: str = "Payment made to supplier"):
        self.account_code = account_code
        # Use Decimal(str(value)) for proper conversion to avoid float precision issues
        self.amount = Decimal(str(amount))
        self.description = description

class CashPayable:
    def __init__(self, account_code: str = "10000001", cp_date: date = None):
        self.voucher_id = None  # assigned by DB
        self.account_code = account_code  # Default Cash/Bank account code
        self.date = cp_date or date.today()
        self.entries: List[CashPayableEntry] = []
        # Initialize as Decimal('0') instead of Decimal(0)
        self.total_amount = Decimal('0')

    def add_entry(self, entry: CashPayableEntry):
        self.entries.append(entry)
        self.calculate_totals()

    def remove_entry_by_index(self, index):
        if 0 <= index < len(self.entries):
            del self.entries[index]
            self.calculate_totals()

    def calculate_totals(self):
        # Use entry.amount to maintain consistency with Decimal values
        self.total_amount = sum(entry.amount for entry in self.entries)