# in use 
# core/transaction_service.py
from database.ledger_repo import LedgerRepo
from utils.type_utils import to_decimal, to_float
class TransactionService:
    # core/transaction_service.py - ADD THESE METHODS

    @staticmethod
    def reverse_transaction(source, source_id):
        """Reverse/delete all transactions and ledger entries for a given source"""
        # Delete ledger entries first
        LedgerRepo.delete_entries_by_voucher(source, source_id)
        
        # Note: You might want to add transaction table cleanup if needed
        # TransactionRepo.delete_transactions_by_reference(source, source_id)

    @staticmethod
    def update_transaction(source, source_id, date, debit_account, credit_account, amount, description=""):
        """Update a transaction by first reversing then reposting"""
        # First reverse the old transaction
        TransactionService.reverse_transaction(source, source_id)
        
        # Then post the updated transaction
        TransactionService.post_transaction(
            source=source,
            source_id=source_id,
            date=date,
            debit_account=debit_account,
            credit_account=credit_account,
            amount=amount,
            description=description
        )


    @staticmethod
    def post_transaction(source, source_id, date, debit_account, credit_account, amount, description=""):
        # Convert amount to Decimal for consistent calculations
        amount_decimal = to_decimal(amount)
        
        # Prepare entries
        current_balance = to_decimal(LedgerRepo.get_balance(debit_account))
        new_balance = current_balance + amount_decimal

        debit_entry = {
            "account_code": debit_account,
            "voucher_type": source,
            "voucher_id": source_id,
            "date": date,
            "debit": to_float(amount_decimal),
            "credit": 0,
            "balance": to_float(new_balance),
            "description": description
        }

        LedgerRepo.insert_entry(debit_entry)

        # credit ledger
        current_balance = to_decimal(LedgerRepo.get_balance(credit_account))
        new_balance = current_balance - amount_decimal

        credit_entry = {
            "account_code": credit_account,
            "voucher_type": source,
            "voucher_id": source_id,
            "date": date,
            "debit": 0,
            "credit": to_float(amount_decimal),
            "balance": to_float(new_balance),
            "description": description
        }

        LedgerRepo.insert_entry(credit_entry)