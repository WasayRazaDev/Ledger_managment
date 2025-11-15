# in use 
# core/purchase.py
from typing import List
from datetime import date
from decimal import Decimal

class PurchaseItem:
    def __init__(self, product_id: int, quantity: int, purchase_rate: float):
        self.product_id = product_id
        self.quantity = quantity
        # CHANGED: Use Decimal(str(value)) for proper conversion to avoid float precision issues
        self.purchase_rate = Decimal(str(purchase_rate))  # Changed from Decimal(purchase_rate)
        # CHANGED: Calculate amount using Decimal values
        self.amount = Decimal(self.quantity) * self.purchase_rate  # Changed from quantity * purchase_rate

class PurchaseInvoice:
    def __init__(self, account_code: str, purchase_date: date):
        self.purchase_id = None  # assigned by DB
        self.account_code = account_code
        self.date = purchase_date
        self.items: List[PurchaseItem] = []
        # CHANGED: Initialize as Decimal('0') instead of Decimal(0)
        self.total_amount = Decimal('0')  # Changed from Decimal(0)

    def add_item(self, item: PurchaseItem):
        self.items.append(item)
        self.calculate_totals()

    def remove_item_by_index(self, index):
        if 0 <= index < len(self.items):
            del self.items[index]
            self.calculate_totals()

    def calculate_totals(self):
        # CHANGED: Use item.amount instead of recalculating to maintain consistency
        # and avoid mixing Decimal with float operations
        self.total_amount = sum(item.amount for item in self.items)  # Changed from sum(item.quantity * item.purchase_rate for item in self.items)
        
        # REMOVED: This line is redundant since we're already using Decimal throughout
        # self.total_amount = Decimal(self.total_amount)  # Remove this line