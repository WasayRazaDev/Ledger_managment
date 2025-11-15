from database.db_config import get_connection


class ReportRepo:

    @staticmethod
    def get_sale_profit_report(start_date, end_date):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                si.invoice_no,
                c.title AS customer,
                c.cell AS cell_no,
                p.name AS product_name,
                si.quantity,
                (si.quantity * si.retail_price) AS sale_amount,
                (si.quantity * si.purchase_rate) AS purchase_amount,
                ((si.quantity * si.retail_price) - (si.quantity * si.purchase_rate)) AS profit,
                inv.advance,
                (inv.total_amount - inv.advance) AS balance
            FROM sales_invoice inv
            JOIN accounts c ON inv.account_code = c.account_code
            JOIN sales_items si ON inv.invoice_no = si.invoice_no
            JOIN products p ON si.product_id = p.product_id
            WHERE inv.date BETWEEN %s AND %s
            ORDER BY inv.date, inv.invoice_no
        """

        cursor.execute(query, (start_date, end_date))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows


    @staticmethod
    def get_receivables_report():
        """
        Fetches receivables data by joining accounts, cash_receivable_entries, and ledger tables.
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            
       
            SELECT 
                a.account_code,
                a.title,
                a.cell,
                l.credit AS amount,
                l.date AS date,
                DATEDIFF(CURDATE(), l.date) AS days,
                COALESCE(b.balance, 0) AS balance,
                l.voucher_type
            FROM accounts a
            JOIN (
                /* Get the latest transaction for each account (any voucher type) */
                SELECT t.account_code, MAX(t.ledger_id) AS ledger_id
                FROM (
                    SELECT le.account_code, le.ledger_id
                    FROM ledger_entries le
                    JOIN (
                        SELECT account_code, MAX(date) AS max_date
                        FROM ledger_entries
                        GROUP BY account_code
                    ) latest ON le.account_code = latest.account_code
                            AND le.date = latest.max_date
                    ) t
                GROUP BY t.account_code
            ) ml ON ml.account_code = a.account_code
            JOIN ledger_entries l ON l.ledger_id = ml.ledger_id
            LEFT JOIN (
                /* Calculate current balance for each account */
                SELECT account_code, COALESCE(SUM(debit), 0) - COALESCE(SUM(credit), 0) AS balance
                FROM ledger_entries
                GROUP BY account_code
            ) b ON b.account_code = a.account_code
            WHERE a.status = 'ACTIVE'
            AND a.account_code LIKE '3%'  -- Only accounts starting with 3
            ORDER BY l.date ASC;

        """

        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows


    def get_cr_voucher_entries(voucher_id):
        query = """
        SELECT 
            cre.entry_id,
            cre.account_code,
            a.title,
            cre.amount AS entry_amount,
            COALESCE(l.total_debit, 0) AS total_debit,
            COALESCE(l.total_credit, 0) AS total_recoveries,
            COALESCE(l.balance, 0) AS balance
        FROM cash_receivable_entries cre
        JOIN accounts a 
            ON cre.account_code = a.account_code
        LEFT JOIN (
            SELECT 
                le.account_code,
                SUM(debit) AS total_debit,
                SUM(credit) AS total_credit,
                COALESCE(SUM(debit),0) - COALESCE(SUM(credit),0) AS balance
            FROM ledger_entries le
            GROUP BY le.account_code
        ) l
            ON cre.account_code = l.account_code
        WHERE cre.voucher_id = %s
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (voucher_id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
