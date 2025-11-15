

from database.db_config import get_connection
from core.cash_receivable import CashReceivable, CashReceivableEntry


class CashReceivableRepo:

    @staticmethod
    def add_cash_receivable(cr: CashReceivable):
        conn = get_connection()
        cursor = conn.cursor()

        # Insert cash receivable header
        cursor.execute(
            "INSERT INTO cash_receivable_vouchers (date) VALUES (%s)",
            (cr.date,)
        )
        cr.voucher_id = cursor.lastrowid

        # Insert cash receivable entries
        for entry in cr.entries:
            cursor.execute(
                "INSERT INTO cash_receivable_entries (voucher_id, account_code, amount, description) "
                "VALUES (%s, %s, %s, %s)",
                (cr.voucher_id, entry.account_code, entry.amount, entry.description)
            )

        conn.commit()
        cursor.close()
        conn.close()
        return cr.voucher_id  # ✅ return the assigned ID

    @staticmethod
    def update_cash_receivable(cr: CashReceivable):
        conn = get_connection()
        cursor = conn.cursor()

        # Update header
        cursor.execute(
            "UPDATE cash_receivable_vouchers SET date=%s WHERE voucher_id=%s",
            ( cr.date, cr.voucher_id)
        )

        # Clear old entries
        cursor.execute("DELETE FROM cash_receivable_entries WHERE voucher_id=%s", (cr.voucher_id,))

        # Insert fresh entries
        for entry in cr.entries:
            cursor.execute(
                "INSERT INTO cash_receivable_entries (voucher_id, account_code, amount, description) "
                "VALUES (%s, %s, %s, %s)",
                (cr.voucher_id, entry.account_code, entry.amount, entry.description)
            )

        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_cash_receivable(voucher_id: int) -> CashReceivable:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT  date FROM cash_receivable_vouchers WHERE voucher_id=%s",
            (voucher_id,)
        )
        row = cursor.fetchone()
        if not row:
            cursor.close()
            conn.close()
            return None

        cr = CashReceivable(account_code="10000001", cr_date=row[0])
        cr.voucher_id = voucher_id
        

        cursor.execute(
            "SELECT account_code, amount, description FROM cash_receivable_entries WHERE voucher_id=%s",
            (voucher_id,)
        )
        entries = cursor.fetchall()
        for entry in entries:
            cr.add_entry(CashReceivableEntry(*entry))

        cursor.close()
        conn.close()
        return cr

    @staticmethod
    def get_all_cash_receivables():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT voucher_id FROM cash_receivable_vouchers ORDER BY voucher_id DESC")
        vouchers = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return vouchers

    @staticmethod
    def get_next_voucher_no():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(voucher_id) FROM cash_receivable_vouchers")
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return (row[0] or 0) + 1

    @staticmethod
    def get_account(account_code: str):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM accounts WHERE account_code = %s", (account_code,))
        account = cursor.fetchone()

        cursor.close()
        conn.close()
        return account