# in use 
# core/sale.py
from typing import List
from datetime import date
from decimal import Decimal

class SaleItem:
    def __init__(self, product_id, quantity: int, purchase_rate: float, retail_price: float):
        self.product_id = product_id
        self.quantity = quantity
        self.purchase_rate = Decimal(str(purchase_rate))
        self.retail_price = Decimal(str(retail_price))
        self.amount = self.quantity * self.retail_price

class SaleInvoice:
    def __init__(self, account_code: str, invoice_date: date, advance: float = 0):
        self.invoice_no = None  # assigned by DB
        self.account_code = account_code
        self.date = invoice_date
        self.items: List[SaleItem] = []
        self.advance = Decimal(str(advance))  # Convert to Decimal
        self.total_amount = Decimal('0')
        self.remaining_balance = Decimal('0')

    def add_item(self, item: SaleItem):
        self.items.append(item)
        self.calculate_totals()
    
    def remove_item_by_index(self, index):
        if 0 <= index < len(self.items):
            del self.items[index]
            self.calculate_totals()

    def calculate_totals(self):
        self.total_amount = sum(item.amount for item in self.items)
        self.remaining_balance = self.total_amount - self.advance
        
    def to_float_dict(self):
        """Convert Decimal values to float for display and database operations"""
        return {
            'invoice_no': self.invoice_no,
            'account_code': self.account_code,
            'date': self.date,
            'total_amount': float(self.total_amount),
            'advance': float(self.advance),
            'remaining_balance': float(self.remaining_balance),
            'items': [
                {
                    'product_id': item.product_id,
                    'quantity': item.quantity,
                    'purchase_rate': float(item.purchase_rate),
                    'retail_price': float(item.retail_price),
                    'amount': float(item.amount)
                }
                for item in self.items
            ]
        }