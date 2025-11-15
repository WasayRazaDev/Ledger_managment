from database.db_config import get_connection

try:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DATABASE();")
    result = cursor.fetchone()
    print(f"Connected to database: {result[0]}")
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Database connection failed: {e}")

