# ui/cash_memo_ui.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QApplication,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QDateEdit, 
    QInputDialog, QDialog, QGroupBox
)
from PyQt5.QtCore import QDate
from database.cash_memo_repo import CashMemoRepo
from database.product_repo import ProductRepo
from core.cash_memo import CashMemo, CashMemoItem
from ui.product_search_dialog import ProductSearchDialog
from core.transaction_service import TransactionService
from utils.update_logger import log_update
from decimal import Decimal
import decimal
from ui.enter_navigation import EnterNavigationManager


class CashMemoUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cash Memo Management")
        self.resize(900, 600)
        
        # Stylesheet (same as before)
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 10pt;
                background-color: #f8f9fa;
            }
            QLabel {
                color: #2c3e50;
                font-weight: 500;
            }
            QLabel#titleLabel {
                font-size: 14pt;
                font-weight: bold;
                color: #2c3e50;
                padding: 5px;
                background-color: #e9ecef;
                border-radius: 6px;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 12px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px 0 8px;
                color: #495057;
            }
            QPushButton {
                background-color: #3498db;
                border: none;
                color: white;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
                color: #7f8c8d;
            }
            QPushButton#actionButton {
                background-color: #2ecc71;
            }
            QPushButton#actionButton:hover {
                background-color: #27ae60;
            }
            QPushButton#actionButton:pressed {
                background-color: #219653;
            }
            QPushButton#dangerButton {
                background-color: #e74c3c;
            }
            QPushButton#dangerButton:hover {
                background-color: #c0392b;
            }
            QPushButton#dangerButton:pressed {
                background-color: #a93226;
            }
            QPushButton#searchButton {
                background-color: #9b59b6;
            }
            QPushButton#searchButton:hover {
                background-color: #8e44ad;
            }
            QLineEdit, QComboBox, QDateEdit {
                padding: 8px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                background-color: white;
                selection-background-color: #3498db;
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
                border: 2px solid #3498db;
            }
            QLineEdit:disabled, QComboBox:disabled {
                background-color: #e9ecef;
                color: #6c757d;
            }
            QTableWidget {
                gridline-color: #dee2e6;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                background-color: white;
                alternate-background-color: #f8f9fa;
            }
            QTableWidget::item {
                padding: 6px;
                border-bottom: 1px solid #dee2e6;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            QHeaderView::section:checked {
                background-color: #2980b9;
            }
        """)

        # Initialize cash memo
        self.memo = CashMemo()

        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)
        self.setLayout(layout)

        # Title
        title_label = QLabel("Cash Memo Management")
        title_label.setObjectName("titleLabel")
        layout.addWidget(title_label)



        # --- Memo Info Group ---
        memo_group = QGroupBox("Memo Information")
        memo_layout = QVBoxLayout()
        memo_group.setLayout(memo_layout)
        layout.addWidget(memo_group)

        # First row: Memo number and Date
        memo_header_layout = QHBoxLayout()
        memo_header_layout.addWidget(QLabel("Memo #:"))
        self.memo_no_label = QLabel(str(CashMemoRepo.get_next_memo_no()))
        self.memo_no_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        memo_header_layout.addWidget(self.memo_no_label)
        memo_header_layout.addSpacing(20)

        memo_header_layout.addWidget(QLabel("Date:"))
        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setMinimumWidth(120)
        memo_header_layout.addWidget(self.date_edit)
        memo_header_layout.addStretch()
        memo_layout.addLayout(memo_header_layout)

        # Second row: Customer information
        customer_layout = QHBoxLayout()
        customer_layout.addWidget(QLabel("Customer Name:"))
        self.customer_name_input = QLineEdit()
        self.customer_name_input.setPlaceholderText("Enter customer name (optional)")
        self.customer_name_input.setMinimumWidth(200)
        customer_layout.addWidget(self.customer_name_input)

        customer_layout.addSpacing(20)
        customer_layout.addWidget(QLabel("Contact No:"))
        self.contact_input = QLineEdit()
        self.contact_input.setPlaceholderText("Enter contact number (optional)")
        self.contact_input.setMaximumWidth(150)
        customer_layout.addWidget(self.contact_input)
        customer_layout.addStretch()
        memo_layout.addLayout(customer_layout)

        # Third row: Product search
        product_search_layout = QHBoxLayout()
        product_search_layout.addWidget(QLabel("Product:"))
        self.product_label = QLabel("Select Product")
        self.product_label.setStyleSheet("background-color: #e9ecef; padding: 6px; border-radius: 4px;")
        product_search_layout.addWidget(self.product_label)
        product_search_layout.addSpacing(10)

        self.product_search_btn = QPushButton("Search Product")
        self.product_search_btn.setObjectName("searchButton")
        product_search_layout.addWidget(self.product_search_btn)
        self.product_search_btn.clicked.connect(self.open_product_search)
        product_search_layout.addStretch()
        memo_layout.addLayout(product_search_layout)

        # Fourth row: Product details and add button
        product_details_layout = QHBoxLayout()
        product_details_layout.addWidget(QLabel("Qty:"))
        self.qty_input = QLineEdit("1")
        self.qty_input.setMaximumWidth(60)
        product_details_layout.addWidget(self.qty_input)

        product_details_layout.addWidget(QLabel("Purchase Rate:"))
        self.purchase_rate_input = QLineEdit("0.0")
        self.purchase_rate_input.setMaximumWidth(80)
        product_details_layout.addWidget(self.purchase_rate_input)

        product_details_layout.addWidget(QLabel("Retail Rate:"))
        self.retail_rate_input = QLineEdit("0.0")
        self.retail_rate_input.setMaximumWidth(80)
        product_details_layout.addWidget(self.retail_rate_input)

        self.add_item_btn = QPushButton("Add Item")
        self.add_item_btn.setObjectName("actionButton")
        product_details_layout.addWidget(self.add_item_btn)
        self.add_item_btn.clicked.connect(self.add_item)
        memo_layout.addLayout(product_details_layout)

        # --- Items Table ---
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["Product ID", "Name", "Qty", "Purchase", "Retail", "Subtotal"]
        )
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)
        
        # --- Totals Display ---
        totals_group = QGroupBox("Amount Summary")
        totals_layout = QVBoxLayout()
        totals_group.setLayout(totals_layout)
        layout.addWidget(totals_group)

        # Totals row
        total_row_layout = QHBoxLayout()
        total_row_layout.addWidget(QLabel("Total Amount:"))
        self.total_label = QLabel("0.00")
        self.total_label.setStyleSheet("font-weight: bold; color: #27ae60; background-color: #e9ecef; padding: 6px; border-radius: 4px; min-width: 80px;")
        total_row_layout.addWidget(self.total_label)

        total_row_layout.addWidget(QLabel("Amount Paid:"))
        self.paid_input = QLineEdit("0.0")
        self.paid_input.setMaximumWidth(100)
        total_row_layout.addWidget(self.paid_input)

        total_row_layout.addWidget(QLabel("Change:"))
        self.change_label = QLabel("0.00")
        self.change_label.setStyleSheet("font-weight: bold; color: #e74c3c; background-color: #e9ecef; padding: 6px; border-radius: 4px; min-width: 80px;")
        total_row_layout.addWidget(self.change_label)
        total_row_layout.addStretch()
        totals_layout.addLayout(total_row_layout)

        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        layout.addLayout(button_layout)

        self.remove_item_btn = QPushButton("Remove Item")
        self.remove_item_btn.setObjectName("dangerButton")
        self.remove_item_btn.clicked.connect(self.remove_selected_item)
        button_layout.addWidget(self.remove_item_btn)

        self.load_btn = QPushButton("Load Memo")
        self.load_btn.clicked.connect(self.load_memo)
        button_layout.addWidget(self.load_btn)

        button_layout.addStretch()

        self.print_btn = QPushButton("Print Memo")
        self.print_btn.setObjectName("actionButton")
        self.print_btn.clicked.connect(self.print_memo)
        button_layout.addWidget(self.print_btn)

        self.save_btn = QPushButton("Save Memo")
        self.save_btn.setObjectName("actionButton")
        self.save_btn.clicked.connect(self.save_memo)
        button_layout.addWidget(self.save_btn)

        # ✅ Define Enter behavior per widget
        self._enter_nav = EnterNavigationManager(
            self,
            rules={
                self.customer_name_input: {"mode": "tab_only"},
                self.contact_input: {"mode": "tab_only"},
                self.date_edit: {"mode": "tab_only"},
                self.product_search_btn: {"mode": "both"},
                self.qty_input: {"mode": "tab_only"},
                self.purchase_rate_input: {"mode": "tab_only"},
                self.retail_rate_input: {"mode": "tab_only"},
                self.add_item_btn: {"mode": "both", "next": self.product_search_btn},
                self.paid_input: {"mode": "tab_only"},
            }
        )

        app = QApplication.instance()
        if app:
            app.installEventFilter(self._enter_nav)

        # Connect signals
        self.paid_input.textChanged.connect(self.calculate_change)

    def open_product_search(self):
        dialog = ProductSearchDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            prod = dialog.selected_product
            if prod:
                # Default values
                self.qty_input.setText("1")
                self.purchase_rate_input.setText(str(prod.get('purchase_rate', '0.0')))
                self.retail_rate_input.setText(str(prod.get('retail_rate', '0.0')))
                self.product_label.setText(f"{prod['product_id']} - {prod['name']}")

    def add_item(self):
        if self.product_label.text() == "Select Product":
            QMessageBox.warning(self, "Error", "Please select a product first")
            return

        product_id = self.product_label.text().split(" - ")[0]

        try:
            quantity = int(self.qty_input.text())
            purchase_rate = Decimal(self.purchase_rate_input.text())
            retail_rate = Decimal(self.retail_rate_input.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "Quantity and rates must be valid numbers")
            return

        if quantity <= 0 or purchase_rate <= 0 or retail_rate <= 0:
            QMessageBox.warning(self, "Error", "Quantity, Purchase Rate and Retail Rate must be greater than zero")
            return

        # Calculate amount
        amount = retail_rate * quantity

        # Create CashMemoItem
        item = CashMemoItem(
            product_id=product_id,
            quantity=quantity,
            purchase_rate=purchase_rate,
            retail_rate=retail_rate,
            amount=amount
        )
        
        self.memo.add_item(item)
        self.refresh_items_table()
        
        # Clear input fields
        self.product_label.setText("Select Product")
        self.qty_input.setText("1")
        self.purchase_rate_input.setText("0.0")
        self.retail_rate_input.setText("0.0")

    def remove_selected_item(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Please select an item to remove")
            return

        self.memo.remove_item_by_index(selected_row)
        self.refresh_items_table()

    def load_memo(self):
        memo_no, ok = QInputDialog.getInt(self, "Load Cash Memo", "Enter Memo #:")
        if not ok:
            return
        
        memo = CashMemoRepo.get_memo(memo_no)
        if not memo:
            QMessageBox.warning(self, "Error", f"Cash Memo #{memo_no} not found")
            return

        self.memo = memo
        self.memo_no_label.setText(str(memo.memo_no))
        
        # Convert datetime to QDate properly
        if hasattr(memo.memo_date, 'year'):
            self.date_edit.setDate(QDate(memo.memo_date.year, memo.memo_date.month, memo.memo_date.day))
        else:
            # Fallback to current date if there's an issue
            self.date_edit.setDate(QDate.currentDate())
            
        self.customer_name_input.setText(memo.customer_name or "")
        self.contact_input.setText(memo.contact_no or "")
        self.paid_input.setText(f"{float(memo.amount_paid):.2f}")

        self.refresh_items_table()

    def save_memo(self):
        if len(self.memo.items) == 0:
            QMessageBox.warning(self, "Error", "Add at least one product/item to memo")
            return

        # Set memo data
        self.memo.memo_date = self.date_edit.date().toPyDate()
        self.memo.customer_name = self.customer_name_input.text().strip() or None
        self.memo.contact_no = self.contact_input.text().strip() or None

        # Validate amount paid
        try:
            amount_paid = Decimal(self.paid_input.text())
        except (ValueError, decimal.InvalidOperation):
            QMessageBox.warning(self, "Error", "Amount paid must be a valid number")
            return

        if amount_paid <= 0:
            QMessageBox.warning(self, "Error", "Amount paid must be greater than zero")
            return

        if amount_paid < self.memo.total_amount:
            QMessageBox.warning(self, "Error", "Amount paid cannot be less than total amount")
            return

        self.memo.amount_paid = amount_paid
        self.memo.calculate_change()

        # Check if update or new
        is_update = self.memo.memo_no is not None

        if is_update:
            # Update existing memo
            CashMemoRepo.update_memo(self.memo)
            # Reverse previous ledger entries before reposting
            TransactionService.reverse_transaction("SALE", self.memo.memo_no)
            # Append update log (voucher updated)
            try:
                log_update(
                    voucher_type="SALE",
                    voucher_id=self.memo.memo_no,
                    details=f"date={self.memo.memo_date}, total={float(self.memo.total_amount):.2f}, customer={self.memo.customer_name or ''}"
                )
            except Exception:
                pass
            msg = "updated"
        else:
            # New memo
            self.memo.memo_no = CashMemoRepo.get_next_memo_no()
            CashMemoRepo.add_memo(self.memo)
            msg = "saved"

        # Post to ledger (cash transaction)
        description = (
            f"Cash Memo #{self.memo.memo_no} - {self.memo.customer_name}"
            if self.memo.customer_name else f"Cash Memo #{self.memo.memo_no}"
        )
        TransactionService.post_transaction(
            source="SALE",
            source_id=self.memo.memo_no,
            date=self.memo.memo_date,
            debit_account=10000001,  # Cash account
            credit_account=10000002, # Revenue account
            amount=float(self.memo.total_amount),
            description=description
        )

        QMessageBox.information(
            self, "Cash Memo", 
            f"Cash Memo #{self.memo.memo_no} {msg} successfully!\n"
            f"Total: {self.memo.total_amount:.2f}\n"
            f"Amount Paid: {self.memo.amount_paid:.2f}\n"
            f"Change: {self.memo.change_amount:.2f}"
        )

        if not is_update:
            self.reset_form()

    def print_memo(self):
        if len(self.memo.items) == 0:
            QMessageBox.warning(self, "Error", "No items to print")
            return

        QMessageBox.information(self, "Print", "Cash memo sent to printer")

    def reset_form(self):
        self.memo = CashMemo()
        self.table.setRowCount(0)
        self.memo_no_label.setText(str(CashMemoRepo.get_next_memo_no()))
        self.customer_name_input.clear()
        self.contact_input.clear()
        self.product_label.setText("Select Product")
        self.qty_input.setText("1")
        self.purchase_rate_input.setText("0.0")
        self.retail_rate_input.setText("0.0")
        self.paid_input.setText("0.0")
        self.update_total_display()

    def refresh_items_table(self):
        self.table.setRowCount(0)
        for item in self.memo.items:
            prod = ProductRepo.get_product_by_id(item.product_id)
            prod_name = prod['name'] if isinstance(prod, dict) else prod.name
            
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(item.product_id)))
            self.table.setItem(row, 1, QTableWidgetItem(prod_name))
            self.table.setItem(row, 2, QTableWidgetItem(str(item.quantity)))
            self.table.setItem(row, 3, QTableWidgetItem(f"{float(item.purchase_rate):.2f}"))
            self.table.setItem(row, 4, QTableWidgetItem(f"{float(item.retail_rate):.2f}"))
            self.table.setItem(row, 5, QTableWidgetItem(f"{float(item.amount):.2f}"))
        
        self.update_total_display()

    def update_total_display(self):
        self.total_label.setText(f"{float(self.memo.total_amount):.2f}")
        self.calculate_change()

    def calculate_change(self):
        try:
            amount_paid = Decimal(self.paid_input.text()) if self.paid_input.text().strip() else Decimal('0')
        except (ValueError, decimal.InvalidOperation):
            amount_paid = Decimal('0')

        change = amount_paid - self.memo.total_amount
        self.change_label.setText(f"{float(change):.2f}" if change > 0 else "0.00")

    def closeEvent(self, event):
        app = QApplication.instance()
        if app and hasattr(self, "_enter_nav"):
            app.removeEventFilter(self._enter_nav)
        super().closeEvent(event)