
from database.db_config import get_connection
from core.product import Product

class ProductRepo:

    @staticmethod
    def add_product(product: Product):
        conn = get_connection()
        cursor = conn.cursor()
        query = "INSERT INTO products (company, name, status) VALUES (%s, %s, %s)"
        cursor.execute(query, (product.company, product.name, product.status))
        product_id = cursor.lastrowid  # Get the auto-generated ID
        conn.commit()
        cursor.close()
        conn.close()
        return product_id

    @staticmethod
    def update_product(product: Product):
        conn = get_connection()
        cursor = conn.cursor()
        query = "UPDATE products SET company=%s, name=%s, status=%s WHERE product_id=%s"
        cursor.execute(query, (product.company, product.name, product.status, product.product_id))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def search_product_by_name(name: str):
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT product_id, company, name, status FROM products WHERE name LIKE %s"
        cursor.execute(query, (f"%{name}%",))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return [Product(*row) for row in results]

    @staticmethod
    def get_all_products():
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT product_id, company, name, status FROM products"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return [Product(*row) for row in results]

    @staticmethod
    def get_product_by_id(product_id: int):
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT product_id, company, name, status FROM products WHERE product_id = %s"
        cursor.execute(query, (product_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return Product(*result) if result else None

    @staticmethod
    def delete_product(product_id: int):
        conn = get_connection()
        cursor = conn.cursor()
        query = "DELETE FROM products WHERE product_id = %s"
        cursor.execute(query, (product_id,))
        conn.commit()
        cursor.close()
        conn.close()