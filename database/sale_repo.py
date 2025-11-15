# database/sale_repo.py
from database.db_config import get_connection
from core.sale import SaleInvoice, SaleItem

class SaleRepo:

    @staticmethod
    def add_invoice(invoice: SaleInvoice):
        """Insert a new invoice and its items."""
        conn = get_connection()
        cursor = conn.cursor()

        # Insert invoice header
        cursor.execute(
            "INSERT INTO sales_invoice (date, account_code, advance, total_amount, remaining_balance) "
            "VALUES (%s, %s, %s, %s, %s)",
            (invoice.date, invoice.account_code, invoice.advance, invoice.total_amount, invoice.remaining_balance)
        )
        invoice.invoice_no = cursor.lastrowid

        # Insert invoice items
        for item in invoice.items:
            cursor.execute(
                "INSERT INTO sales_items (invoice_no, product_id, quantity, purchase_rate, retail_price) "
                "VALUES (%s, %s, %s, %s, %s)",
                (invoice.invoice_no, item.product_id, item.quantity, item.purchase_rate, item.retail_price)
            )

        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def update_invoice(invoice):
        """Update an existing sale invoice"""
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            # Update invoice header
            sql = """
                UPDATE sales_invoice 
                SET account_code=%s, date=%s, total_amount=%s, advance=%s
                WHERE invoice_no=%s
            """
            cursor.execute(sql, (
                invoice.account_code, invoice.date, 
                invoice.total_amount, invoice.advance, 
                invoice.invoice_no
            ))
            
            # Delete existing items
            sql_delete = "DELETE FROM sales_items WHERE invoice_no=%s"
            cursor.execute(sql_delete, (invoice.invoice_no,))
            
            # Insert updated items
            for item in invoice.items:
                sql_item = """
                    INSERT INTO sales_items 
                    (invoice_no, product_id, quantity, purchase_rate, retail_price)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(sql_item, (
                    invoice.invoice_no, item.product_id, item.quantity,
                    item.purchase_rate, item.retail_price
                ))
            
            conn.commit()
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_invoice(invoice_no: int) -> SaleInvoice:
        """Fetch a single invoice with items."""
        conn = get_connection()
        cursor = conn.cursor()

        # Fetch invoice header
        cursor.execute(
            "SELECT account_code, date, advance, total_amount, remaining_balance "
            "FROM sales_invoice WHERE invoice_no=%s",
            (invoice_no,)
        )
        row = cursor.fetchone()
        if not row:
            cursor.close()
            conn.close()
            return None

        invoice = SaleInvoice(account_code=row[0], invoice_date=row[1], advance=row[2])
        invoice.invoice_no = invoice_no
        invoice.total_amount = row[3]
        invoice.remaining_balance = row[4]

        # Fetch items
        cursor.execute(
            "SELECT product_id, quantity, purchase_rate, retail_price FROM sales_items WHERE invoice_no=%s",
            (invoice_no,)
        )
        items = cursor.fetchall()
        for i in items:
            invoice.add_item(SaleItem(*i))

        cursor.close()
        conn.close()
        return invoice

    @staticmethod
    def get_all_invoices():
        """Return a list of all invoice numbers, newest first."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT invoice_no FROM sales_invoice ORDER BY invoice_no DESC")
        invoices = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return invoices

    @staticmethod
    def get_next_invoice_no():
        """Return next invoice number for auto-increment."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(invoice_no) FROM sales_invoice")
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return (row[0] or 0) + 1
