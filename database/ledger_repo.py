# database/ledger_repo.py

from database.db_config import get_connection

class LedgerRepo:

    @staticmethod
    def insert_entry(entry):
        conn = get_connection()
        cursor = conn.cursor()
        # 🔹 FIX: removed balance column, only insert debit/credit
        sql = """
        INSERT INTO ledger_entries
        (account_code, date, voucher_type, voucher_id, debit, credit, description)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            entry["account_code"], entry["date"], entry["voucher_type"], entry["voucher_id"],
            entry["debit"], entry["credit"], entry["description"]
        )
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def fetch_entries(account_code):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT * FROM ledger_entries WHERE account_code=%s ORDER BY date, ledger_id"
        cursor.execute(sql, (account_code,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    @staticmethod
    def fetch_entries_by_date(account_code, start_date, end_date):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = """
        SELECT * FROM ledger_entries 
        WHERE account_code=%s AND date BETWEEN %s AND %s
        ORDER BY date, ledger_id
        """
        cursor.execute(sql, (account_code, start_date, end_date))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    @staticmethod
    def get_balance(account_code):
        conn = get_connection()
        cursor = conn.cursor()
        # 🔹 FIX: balance is computed dynamically
        sql = "SELECT COALESCE(SUM(debit),0) - COALESCE(SUM(credit),0) FROM ledger_entries WHERE account_code=%s"
        cursor.execute(sql, (account_code,))
        balance = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return float(balance) if balance is not None else 0.0

    @staticmethod
    def delete_entries_by_source(voucher_type, voucher_id):
        """
        Delete all ledger entries related to a specific voucher (e.g., sale or purchase invoice)
        """
        # 🔹 FIX: use ledger_entries not ledger
        sql = "DELETE FROM ledger_entries WHERE voucher_type=%s AND voucher_id=%s"
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (voucher_type, voucher_id))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_ledger_by_account_code(account_code: str, from_date=None, to_date=None):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT ledger_id, account_code, date, voucher_type, voucher_id,
                description, debit, credit
            FROM ledger_entries
            WHERE account_code = %s
        """
        params = [account_code]

        if from_date and to_date:
            query += " AND date BETWEEN %s AND %s"
            params.extend([from_date, to_date])

        query += " ORDER BY date ASC, ledger_id ASC"

        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        # 🔹 FIX: compute running balance here dynamically
        balance = 0
        result = []
        for row in rows:
            balance += float(row["debit"]) - float(row["credit"])
            row["balance"] = balance
            result.append(row)

        return result

    @staticmethod
    def update_entries_by_source(voucher_type, voucher_id, entries):
        """
        Update ledger entries for a given source (voucher_type + voucher_id)
        `entries` is a list of dicts with debit, credit, description, date, etc.
        """
        conn = get_connection()
        cursor = conn.cursor()

        for entry in entries:
            # 🔹 FIX: removed balance, use ledger_entries
            sql = """
            UPDATE ledger_entries
            SET account_code=%s, date=%s, debit=%s, credit=%s, description=%s
            WHERE voucher_type=%s AND voucher_id=%s AND account_code=%s
            """
            values = (
                entry["account_code"], entry["date"], entry["debit"], entry["credit"],
                entry.get("description", ""),
                voucher_type, voucher_id, entry["account_code"]
            )
            cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def fetch_entry_by_source_acc(voucher_type, voucher_id, account_code):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        # 🔹 FIX: use ledger_entries not ledger
        cursor.execute(
            "SELECT * FROM ledger_entries WHERE voucher_type=%s AND voucher_id=%s AND account_code=%s",
            (voucher_type, voucher_id, account_code)
        )
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row

    @staticmethod
    def delete_entries_by_voucher(voucher_type, voucher_id):
        """Delete all ledger entries for a specific voucher"""
        conn = get_connection()
        cursor = conn.cursor()
        sql = "DELETE FROM ledger_entries WHERE voucher_type=%s AND voucher_id=%s"
        cursor.execute(sql, (voucher_type, voucher_id))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_entries_by_voucher(voucher_type, voucher_id):
        """Get all ledger entries for a specific voucher"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT * FROM ledger_entries WHERE voucher_type=%s AND voucher_id=%s"
        cursor.execute(sql, (voucher_type, voucher_id))
        entries = cursor.fetchall()
        cursor.close()
        conn.close()
        return entries

    @staticmethod
    def get_all_entries():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ledger")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    # database/ledger_repo.py

    def get_max_voucher_id(voucher_type):
        conn = get_connection()   # get a new connection
        cursor = conn.cursor(dictionary=True)
        query = "SELECT MAX(voucher_id) as max_id FROM ledger WHERE voucher_type = %s"
        cursor.execute(query, (voucher_type,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row and row["max_id"]:
            return int(row["max_id"])
        return 0


    # database/ledger_repo.py
    @staticmethod
    def get_max_voucher_id(voucher_type=None):
        """Get the maximum voucher ID for a specific voucher type or all types"""
        conn = get_connection()
        cursor = conn.cursor()
        
        if voucher_type:
            sql = "SELECT MAX(voucher_id) FROM ledger_entries WHERE voucher_type = %s"
            cursor.execute(sql, (voucher_type,))
        else:
            sql = "SELECT MAX(voucher_id) FROM ledger_entries"
            cursor.execute(sql)
        
        result = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return result if result is not None else 0