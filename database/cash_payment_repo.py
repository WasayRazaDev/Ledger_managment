
from database.db_config import get_connection
from core.cash_payment import CashPayable, CashPayableEntry


class CashPayableRepo:

    @staticmethod
    def add_cash_payable(cp: CashPayable):
        conn = get_connection()
        cursor = conn.cursor()

        # Insert cash payable header
        cursor.execute(
            "INSERT INTO cash_payment_vouchers (date) VALUES (%s)",
            (cp.date,)
        )
        cp.voucher_id = cursor.lastrowid

        # Insert cash payable entries
        for entry in cp.entries:
            cursor.execute(
                "INSERT INTO cash_payment_entries (voucher_id, account_code, amount, description) "
                "VALUES (%s, %s, %s, %s)",
                (cp.voucher_id, entry.account_code, entry.amount, entry.description)
            )

        conn.commit()
        cursor.close()
        conn.close()
        return cp.voucher_id  # ✅ return the assigned ID

    @staticmethod
    def update_cash_payable(cp: CashPayable):
        conn = get_connection()
        cursor = conn.cursor()

        # Update header
        cursor.execute(
            "UPDATE cash_payment_vouchers SET date=%s WHERE voucher_id=%s",
            (cp.date, cp.voucher_id)
        )

        # Clear old entries
        cursor.execute("DELETE FROM cash_payment_entries WHERE voucher_id=%s", (cp.voucher_id,))

        # Insert fresh entries
        for entry in cp.entries:
            cursor.execute(
                "INSERT INTO cash_payment_entries (voucher_id, account_code, amount, description) "
                "VALUES (%s, %s, %s, %s)",
                (cp.voucher_id, entry.account_code, entry.amount, entry.description)
            )

        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_cash_payable(voucher_id: int) -> CashPayable:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT date FROM cash_payment_vouchers WHERE voucher_id=%s",
            (voucher_id,)
        )
        row = cursor.fetchone()
        if not row:
            cursor.close()
            conn.close()
            return None

        cp = CashPayable(account_code="10000001", cp_date=row[0])
        cp.voucher_id = voucher_id

        cursor.execute(
            "SELECT account_code, amount, description FROM cash_payment_entries WHERE voucher_id=%s",
            (voucher_id,)
        )
        entries = cursor.fetchall()
        for entry in entries:
            cp.add_entry(CashPayableEntry(*entry))

        cursor.close()
        conn.close()
        return cp

    @staticmethod
    def get_all_cash_payables():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT voucher_id FROM cash_payment_vouchers ORDER BY voucher_id DESC")
        vouchers = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return vouchers

    @staticmethod
    def get_next_voucher_no():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(voucher_id) FROM cash_payment_vouchers")
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