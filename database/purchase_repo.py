from database.db_config import get_connection
from core.purchase import PurchaseInvoice, PurchaseItem


class PurchaseRepo:

    @staticmethod
    def add_purchase(purchase: PurchaseInvoice):
        conn = get_connection()
        cursor = conn.cursor()

        # Insert purchase header
        cursor.execute(
            "INSERT INTO purchases (date, account_code, total_amount) VALUES (%s, %s, %s)",
            (purchase.date, purchase.account_code, purchase.total_amount)
        )
        purchase.purchase_id = cursor.lastrowid

        # Insert purchase items (no retail_price anymore)
        for item in purchase.items:
            cursor.execute(
                "INSERT INTO purchase_items (purchase_id, product_id, quantity, purchase_rate) "
                "VALUES (%s, %s, %s, %s)",
                (purchase.purchase_id, item.product_id, item.quantity, item.purchase_rate)
            )

        conn.commit()
        cursor.close()
        conn.close()
        return purchase.purchase_id   # ✅ return the assigned ID

        


    @staticmethod
    def update_purchase(purchase: PurchaseInvoice):
        conn = get_connection()
        cursor = conn.cursor()

        # Update header
        cursor.execute(
            "UPDATE purchases SET account_code=%s, date=%s, total_amount=%s WHERE purchase_id=%s",
            (purchase.account_code, purchase.date, purchase.total_amount, purchase.purchase_id)
        )

        # Clear old items
        cursor.execute("DELETE FROM purchase_items WHERE purchase_id=%s", (purchase.purchase_id,))

        # Insert fresh items (no retail_price anymore)
        for item in purchase.items:
            cursor.execute(
                "INSERT INTO purchase_items (purchase_id, product_id, quantity, purchase_rate) "
                "VALUES (%s, %s, %s, %s)",
                (purchase.purchase_id, item.product_id, item.quantity, item.purchase_rate)
            )

        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_purchase(purchase_id: int) -> PurchaseInvoice:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT account_code, date, total_amount FROM purchases WHERE purchase_id=%s",
            (purchase_id,)
        )
        row = cursor.fetchone()
        if not row:
            cursor.close()
            conn.close()
            return None

        purchase = PurchaseInvoice(account_code=row[0], purchase_date=row[1])
        purchase.purchase_id = purchase_id
        purchase.total_amount = row[2]

        cursor.execute(
            "SELECT product_id, quantity, purchase_rate FROM purchase_items WHERE purchase_id=%s",
            (purchase_id,)
        )
        items = cursor.fetchall()
        for i in items:
            purchase.add_item(PurchaseItem(*i))

        cursor.close()
        conn.close()
        return purchase

    @staticmethod
    def get_all_purchases():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT purchase_id FROM purchases ORDER BY purchase_id DESC")
        purchases = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return purchases

    @staticmethod
    def get_next_purchase_no():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(purchase_id) FROM purchases")
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return (row[0] or 0) + 1


    @staticmethod
    def get_product(product_id: int):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
        product = cursor.fetchone()

        cursor.close()
        conn.close()
        return product