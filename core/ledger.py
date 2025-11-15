# core/ledger.py
from database.ledger_repo import LedgerRepo
from datetime import date
from decimal import Decimal

class Ledger:
    def __init__(self, acc_id):
        self.acc_id = acc_id

    def add_entry(self, voucher_type, voucher_id, entry_date, debit=0.0, credit=0.0, description=""):
        """
        Add a new ledger entry for this account.
        Updates running balance automatically.
        """
        current_balance = LedgerRepo.get_balance(self.acc_id)

        # Ensure values are Decimal
        debit = Decimal(str(debit))
        credit = Decimal(str(credit))
        current_balance = Decimal(str(current_balance))

        new_balance = current_balance + debit - credit

        entry = {
            "acc_id": self.acc_id,
            "voucher_type": voucher_type,
            "voucher_id": voucher_id,
            "date": entry_date,
            "debit": debit,
            "credit": credit,
            "balance": new_balance,
            "description": description
        }

        LedgerRepo.insert_entry(entry)
        return new_balance


    def get_balance(self):
        """
        Return current balance for this account.
        """
        return LedgerRepo.get_balance(self.acc_id)
    
    def get_ledger(self, from_date=None, to_date=None):
        """
        Fetch all ledger entries for this account.
        """
        return LedgerRepo.get_ledger_by_account(self.acc_id, from_date, to_date)


    def print_statement(self, start_date=None, end_date=None):
        """
        Returns ledger entries filtered by date range.
        """
        if start_date and end_date:
            return LedgerRepo.fetch_entries_by_date(self.acc_id, start_date, end_date)
        else:
            return self.get_ledger()
