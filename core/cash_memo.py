# core/cash_memo.py
from decimal import Decimal
from datetime import date
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class CashMemoItem:
    product_id: str
    quantity: int
    purchase_rate: Decimal
    retail_rate: Decimal
    amount: Decimal

    def __post_init__(self):
        # Convert to Decimal if needed
        if not isinstance(self.purchase_rate, Decimal):
            self.purchase_rate = Decimal(str(self.purchase_rate))
        if not isinstance(self.retail_rate, Decimal):
            self.retail_rate = Decimal(str(self.retail_rate))
        if not isinstance(self.amount, Decimal):
            self.amount = Decimal(str(self.amount))

class CashMemo:
    def __init__(self, memo_date: Optional[date] = None):
        self.memo_no: Optional[int] = None
        self.memo_date: date = memo_date or date.today()
        self.customer_name: Optional[str] = None
        self.contact_no: Optional[str] = None
        self.total_amount: Decimal = Decimal('0')
        self.amount_paid: Decimal = Decimal('0')
        self.change_amount: Decimal = Decimal('0')
        self.items: List[CashMemoItem] = []

    def add_item(self, item: CashMemoItem):
        """Add item to cash memo and update totals"""
        self.items.append(item)
        self.calculate_totals()

    def remove_item_by_index(self, index: int):
        """Remove item by index"""
        if 0 <= index < len(self.items):
            self.items.pop(index)
            self.calculate_totals()

    def calculate_totals(self):
        """Calculate total amount and update change"""
        self.total_amount = sum(item.amount for item in self.items)
        self.calculate_change()

    def calculate_change(self):
        """Calculate change amount based on amount paid"""
        self.change_amount = self.amount_paid - self.total_amount
        if self.change_amount < Decimal('0'):
            self.change_amount = Decimal('0')