# using it 
from decimal import Decimal
from datetime import date
from typing import List

class JournalVoucherEntry:
    def __init__(self, account_code: str, debit: float = 0.0, credit: float = 0.0, description: str = "Journal entry"):
        self.account_code = account_code
        self.debit = Decimal(str(debit))
        self.credit = Decimal(str(credit))
        self.description = description

class JournalVoucher:
    def __init__(self, jv_date: date = None, narration: str = ""):
        self.voucher_id = None
        self.date = jv_date or date.today()
        self.narration = narration
        self.entries: List[JournalVoucherEntry] = []
        self.total_credit = Decimal('0')
        self.total_debit = Decimal('0')

    def add_entry(self, entry: JournalVoucherEntry):
        self.entries.append(entry)
        self.update_totals()
    def remove_entry_by_index(self, index: int):
        if 0 <= index < len(self.entries):
            del self.entries[index]
        self.update_totals()

    def update_totals(self):
        """Recalculate and update totals without validation"""
        self.total_debit = sum(e.debit for e in self.entries)
        self.total_credit = sum(e.credit for e in self.entries)

    def validate_totals(self):
        """Ensure debits equal credits"""
        if self.total_debit != self.total_credit:
            raise ValueError(
                f"Debits ({self.total_debit}) and Credits ({self.total_credit}) must be equal"
            )
        return True
