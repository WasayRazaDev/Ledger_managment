
from database.db_config import get_connection
from core.journal_voucher import JournalVoucher, JournalVoucherEntry

class JournalVoucherRepo:

    @staticmethod
    def add_journal_voucher(jv: JournalVoucher):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO journal_vouchers (date, narration) VALUES (%s, %s)",
            (jv.date, jv.narration)
        )
        jv.voucher_id = cursor.lastrowid
        # Insert jv
        for entry in jv.entries:
            cursor.execute(
                "INSERT INTO journal_entries (voucher_id, account_code, debit, credit, description) "
                "VALUES (%s, %s, %s, %s, %s)",
                (jv.voucher_id, entry.account_code, entry.debit, entry.credit, entry.description)
            )

        conn.commit()
        cursor.close()
        conn.close()
        return jv.voucher_id

    @staticmethod
    def update_journal_voucher(jv: JournalVoucher):
        conn = get_connection()
        cursor = conn.cursor()
        #update header
        cursor.execute(
            "UPDATE journal_vouchers SET date=%s, narration=%s WHERE voucher_id=%s",
            (jv.date, jv.narration, jv.voucher_id)
        )
    # clear old entries
        cursor.execute("DELETE FROM journal_entries WHERE voucher_id=%s", (jv.voucher_id,))
    # insert fresh entries
        for entry in jv.entries:
            cursor.execute(
                "INSERT INTO journal_entries (voucher_id, account_code, debit, credit, description) "
                "VALUES (%s, %s, %s, %s, %s)",
                (jv.voucher_id, entry.account_code, entry.debit, entry.credit, entry.description)
            )

        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_journal_voucher(voucher_id: int):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM journal_vouchers WHERE voucher_id=%s", (voucher_id,))
        header = cursor.fetchone()
        if not header:
            cursor.close()
            conn.close()
            return None

        jv = JournalVoucher(jv_date=header["date"], narration=header["narration"])
        jv.voucher_id = header["voucher_id"]

        cursor.execute("SELECT * FROM journal_entries WHERE voucher_id=%s", (voucher_id,))
        for row in cursor.fetchall():
            entry = JournalVoucherEntry(
                account_code=row["account_code"],
                debit=row["debit"],
                credit=row["credit"],
                description=row["description"]
            )
            jv.add_entry(entry)

        cursor.close()
        conn.close()
        return jv

    @staticmethod
    def get_next_voucher_no():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT IFNULL(MAX(voucher_id), 0) + 1 FROM journal_vouchers")
        next_no = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return next_no
