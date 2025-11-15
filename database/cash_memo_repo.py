# database/cash_memo_repo.py
from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional
from core.cash_memo import CashMemo, CashMemoItem
from database.db_config import get_connection

class CashMemoRepo:
    @staticmethod
    def get_next_memo_no() -> int:
        """Get next available memo number"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COALESCE(MAX(memo_no), 0) + 1 FROM cash_memo")
            result = cursor.fetchone()
            return result[0] if result else 1
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def add_memo(memo: CashMemo) -> int:
        """Add new cash memo and return memo number"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Insert main memo record
            cursor.execute("""
                INSERT INTO cash_memo 
                (memo_no, memo_date, customer_name, contact_no, total_amount, amount_paid, change_amount)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                memo.memo_no,
                memo.memo_date,
                memo.customer_name,
                memo.contact_no,
                float(memo.total_amount),
                float(memo.amount_paid),
                float(memo.change_amount)
            ))

            # Insert items
            for item in memo.items:
                cursor.execute("""
                    INSERT INTO cash_memo_items 
                    (memo_no, product_id, quantity, purchase_rate, retail_rate, amount)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    memo.memo_no,
                    item.product_id,
                    item.quantity,
                    float(item.purchase_rate),
                    float(item.retail_rate),
                    float(item.amount)
                ))

            conn.commit()
            return memo.memo_no
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_memo(memo_no: int) -> Optional[CashMemo]:
        """Get cash memo by number"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Get main memo data
            cursor.execute("""
                SELECT memo_no, memo_date, customer_name, contact_no, 
                       total_amount, amount_paid, change_amount
                FROM cash_memo WHERE memo_no = %s
            """, (memo_no,))
            
            memo_data = cursor.fetchone()
            if not memo_data:
                return None

            memo = CashMemo()
            memo.memo_no = memo_data[0]
            
            # Handle date conversion properly
            if isinstance(memo_data[1], (date, datetime)):
                memo.memo_date = memo_data[1]  # Already a date/datetime object
            elif isinstance(memo_data[1], str):
                memo.memo_date = date.fromisoformat(memo_data[1])
            else:
                memo.memo_date = date.today()
                
            memo.customer_name = memo_data[2]
            memo.contact_no = memo_data[3]
            memo.total_amount = Decimal(str(memo_data[4]))
            memo.amount_paid = Decimal(str(memo_data[5]))
            memo.change_amount = Decimal(str(memo_data[6]))

            # Get items
            cursor.execute("""
                SELECT product_id, quantity, purchase_rate, retail_rate, amount
                FROM cash_memo_items WHERE memo_no = %s
            """, (memo_no,))
            
            for item_data in cursor.fetchall():
                item = CashMemoItem(
                    product_id=item_data[0],
                    quantity=item_data[1],
                    purchase_rate=Decimal(str(item_data[2])),
                    retail_rate=Decimal(str(item_data[3])),
                    amount=Decimal(str(item_data[4]))
                )
                memo.items.append(item)

            return memo
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_memo(memo: CashMemo) -> bool:
        """Update existing cash memo"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Update main memo
            cursor.execute("""
                UPDATE cash_memo 
                SET memo_date = %s, customer_name = %s, contact_no = %s,
                    total_amount = %s, amount_paid = %s, change_amount = %s
                WHERE memo_no = %s
            """, (
                memo.memo_date,
                memo.customer_name,
                memo.contact_no,
                float(memo.total_amount),
                float(memo.amount_paid),
                float(memo.change_amount),
                memo.memo_no
            ))

            # Delete existing items
            cursor.execute("DELETE FROM cash_memo_items WHERE memo_no = %s", (memo.memo_no,))

            # Insert new items
            for item in memo.items:
                cursor.execute("""
                    INSERT INTO cash_memo_items 
                    (memo_no, product_id, quantity, purchase_rate, retail_rate, amount)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    memo.memo_no,
                    item.product_id,
                    item.quantity,
                    float(item.purchase_rate),
                    float(item.retail_rate),
                    float(item.amount)
                ))

            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_memo(memo_no: int) -> bool:
        """Delete cash memo"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM cash_memo WHERE memo_no = %s", (memo_no,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_memos_by_date_range(start_date: date, end_date: date) -> List[CashMemo]:
        """Get cash memos by date range"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT memo_no FROM cash_memo 
                WHERE memo_date BETWEEN %s AND %s
                ORDER BY memo_date DESC, memo_no DESC
            """, (start_date, end_date))
            
            memos = []
            for row in cursor.fetchall():
                memo = CashMemoRepo.get_memo(row[0])
                if memo:
                    memos.append(memo)
            
            return memos
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_today_memos() -> List[CashMemo]:
        """Get today's cash memos"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT memo_no FROM cash_memo 
                WHERE memo_date = CURDATE()
                ORDER BY memo_no DESC
            """)
            
            memos = []
            for row in cursor.fetchall():
                memo = CashMemoRepo.get_memo(row[0])
                if memo:
                    memos.append(memo)
            
            return memos
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()