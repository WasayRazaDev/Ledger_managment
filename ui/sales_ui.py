# ui/sales_ui.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,QApplication,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QDateEdit, QInputDialog, QDialog
)
from PyQt5.QtCore import QDate
from database.sale_repo import SaleRepo
from database.account_repo import AccountRepo
from database.product_repo import ProductRepo
from core.sale import SaleInvoice, SaleItem
from ui.account_search_dialog import AccountSearchDialog
from ui.product_search_dialog import ProductSearchDialog
from core.transaction_service import TransactionService
from utils.update_logger import log_update
from decimal import Decimal
import decimal
from ui.enter_navigation import EnterNavigationManager 


class SalesUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sales Module")
        self.resize(900, 600)
        

        # Enhanced custom stylesheet for Sales UI
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

        self.invoice = SaleInvoice(account_code=None, invoice_date=None)

        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)
        self.setLayout(layout)

        # Title
        title_label = QLabel("Sales Invoice Management")
        title_label.setObjectName("titleLabel")
        layout.addWidget(title_label)

        # --- Invoice Info ---
        info_layout = QHBoxLayout()
        info_layout.setSpacing(10)
        layout.addLayout(info_layout)

        info_layout.addWidget(QLabel("Invoice #:"))
        self.invoice_no_label = QLabel(str(SaleRepo.get_next_invoice_no()))
        info_layout.addWidget(self.invoice_no_label)
        info_layout.addSpacing(20)

        info_layout.addWidget(QLabel("Date:"))
        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setMinimumWidth(120)
        info_layout.addWidget(self.date_edit)
        info_layout.addStretch()

        info_layout.addWidget(QLabel("Advance:"))
        self.advance_input = QLineEdit("0.0")
        self.advance_input.setMaximumWidth(100)
        info_layout.addWidget(self.advance_input)
        # In __init__ after creating self.advance_input
        self.advance_input.textChanged.connect(self.on_advance_changed)

        # --- Account Selection ---
        account_layout = QHBoxLayout()
        account_layout.setSpacing(10)
        layout.addLayout(account_layout)

        account_layout.addWidget(QLabel("Account:"))
        self.account_label = QLabel("Select Account")
        self.account_label.setStyleSheet("background-color: #e9ecef; padding: 6px; border-radius: 4px;")
        account_layout.addWidget(self.account_label)
        account_layout.addSpacing(10)

        self.account_search_btn = QPushButton("Search Account")
        self.account_search_btn.setObjectName("searchButton")
        account_layout.addWidget(self.account_search_btn)
        self.account_search_btn.clicked.connect(self.open_account_search)
        account_layout.addStretch()

        # --- Product Inputs ---
        product_layout = QHBoxLayout()
        product_layout.setSpacing(10)
        layout.addLayout(product_layout)

        product_layout.addWidget(QLabel("Product:"))
        self.product_label = QLabel("Select Product")
        self.product_label.setStyleSheet("background-color: #e9ecef; padding: 6px; border-radius: 4px;")
        product_layout.addWidget(self.product_label)
        product_layout.addSpacing(10)

        self.product_search_btn = QPushButton("Search Product")
        self.product_search_btn.setObjectName("searchButton")
        product_layout.addWidget(self.product_search_btn)
        self.product_search_btn.clicked.connect(self.open_product_search)
        product_layout.addSpacing(20)

        product_layout.addWidget(QLabel("Qty:"))
        self.qty_input = QLineEdit("1")
        self.qty_input.setMaximumWidth(60)
        product_layout.addWidget(self.qty_input)

        product_layout.addWidget(QLabel("Purchase:"))
        self.purchase_rate_input = QLineEdit("0.0")
        self.purchase_rate_input.setMaximumWidth(80)
        product_layout.addWidget(self.purchase_rate_input)

        product_layout.addWidget(QLabel("Retail:"))
        self.retail_rate_input = QLineEdit("0.0")
        self.retail_rate_input.setMaximumWidth(80)
        product_layout.addWidget(self.retail_rate_input)

        self.add_item_btn = QPushButton("Add Item")
        self.add_item_btn.setObjectName("actionButton")
        product_layout.addWidget(self.add_item_btn)
        self.add_item_btn.clicked.connect(self.add_item)

        # --- Items Table ---
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["Product ID", "Name", "Qty", "Purchase", "Retail", "Subtotal"]
        )
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)
        
        # Add total display
        total_layout = QHBoxLayout()
        total_layout.setSpacing(20)
        layout.addLayout(total_layout)

        total_layout.addWidget(QLabel("Total Amount:"))
        self.total_label = QLabel("0.00")
        self.total_label.setStyleSheet("font-weight: bold; color: #2c3e50; background-color: #e9ecef; padding: 6px; border-radius: 4px; min-width: 80px;")
        total_layout.addWidget(self.total_label)

        total_layout.addWidget(QLabel("Advance:"))
        self.advance_display = QLabel("0.00")
        self.advance_display.setStyleSheet("font-weight: bold; color: #2c3e50; background-color: #e9ecef; padding: 6px; border-radius: 4px; min-width: 80px;")
        total_layout.addWidget(self.advance_display)

        total_layout.addWidget(QLabel("Balance Due:"))
        self.balance_label = QLabel("0.00")
        self.balance_label.setStyleSheet("font-weight: bold; color: #e74c3c; background-color: #e9ecef; padding: 6px; border-radius: 4px; min-width: 80px;")
        total_layout.addWidget(self.balance_label)
        total_layout.addStretch()

        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        layout.addLayout(button_layout)

        self.remove_item_btn = QPushButton("Remove Item")
        self.remove_item_btn.setObjectName("dangerButton")
        self.remove_item_btn.clicked.connect(self.remove_selected_item)
        button_layout.addWidget(self.remove_item_btn)

        self.load_btn = QPushButton("Load Invoice")
        self.load_btn.clicked.connect(self.load_invoice)
        button_layout.addWidget(self.load_btn)

        button_layout.addStretch()

        self.save_btn = QPushButton("Save Invoice")
        self.save_btn.setObjectName("actionButton")
        self.save_btn.clicked.connect(self.save_invoice)
        button_layout.addWidget(self.save_btn)

        # ✅ Define Enter behavior per widget
        self._enter_nav = EnterNavigationManager(
            self,
            rules={
                
                self.date_edit: {"mode": "tab_only"},
                self.advance_input: {"mode": "tab_only"},
                self.account_search_btn: {"mode": "both"},
                self.product_search_btn: {"mode": "both"},
                self.qty_input: {"mode": "tab_only"},
                self.purchase_rate_input: {"mode": "tab_only"},
                self.retail_rate_input: {"mode": "tab_only"},
                self.add_item_btn: { "mode": "both","next": self.product_search_btn},
            }
        )

        app = QApplication.instance()
        if app:
            app.installEventFilter(self._enter_nav)

    # --- All the functional methods remain exactly the same from here ---
    # --- Load Invoice ---
    def load_invoice(self):
        invoice_no, ok = QInputDialog.getInt(self, "Load Invoice", "Enter Invoice #:")
        if not ok:
            return
        invoice = SaleRepo.get_invoice(invoice_no)
        if not invoice:
            QMessageBox.warning(self, "Error", f"Invoice #{invoice_no} not found")
            return

        self.invoice = invoice
        self.invoice_no_label.setText(str(invoice.invoice_no))
        self.date_edit.setDate(QDate(invoice.date.year, invoice.date.month, invoice.date.day))
        self.advance_input.setText(f"{float(invoice.advance):.2f}")  # Convert Decimal to string
        account = AccountRepo.get_account_by_code(invoice.account_code)
        self.account_label.setText(f"{invoice.account_code} - {account.title}")

        self.refresh_items_table()

    # --- Account Search ---
    def open_account_search(self):
        dialog = AccountSearchDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            acc = dialog.selected_account
            if acc:
                self.invoice.account_code = acc["account_code"]
                self.invoice.title = acc.get("title", "")
                self.account_label.setText(f"{acc['account_code']} - {acc['title']}")

    # --- Product Search ---
    def open_product_search(self):
        dialog = ProductSearchDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            prod = dialog.selected_product
            if prod:
                # Default values
                self.qty_input.setText("1")
                self.purchase_rate_input.setText("0.0")
                self.retail_rate_input.setText("0.0")
                self.product_label.setText(f"{prod['product_id']} - {prod['name']}")

    def add_item(self):
        # Make sure a product is selected
        if self.product_label.text() == "Select Product":
            QMessageBox.warning(self, "Error", "Please select a product first")
            return

        # Extract product_id from the label
        product_id = self.product_label.text().split(" - ")[0]

        # Read quantity and rates
        try:
            quantity = int(self.qty_input.text())
            purchase_rate = float(self.purchase_rate_input.text())
            retail_rate = float(self.retail_rate_input.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "Quantity and rates must be numbers")
            return

        # Validate mandatory fields
        if quantity <= 0 or purchase_rate <= 0 or retail_rate <= 0:
            QMessageBox.warning(self, "Error", "Quantity, Purchase Rate and Retail Rate must be greater than zero")
            return

        # Create SaleItem
        # Create SaleItem with proper Decimal conversion
        item = SaleItem(
            product_id=product_id,
            quantity=quantity,
            purchase_rate=float(purchase_rate),  # Pass as float, constructor will convert to Decimal
            retail_price=float(retail_rate)      # Pass as float, constructor will convert to Decimal
        )
        self.invoice.add_item(item)

        # Refresh table
        self.refresh_items_table()
        
        # Clear input fields after adding
        self.product_label.setText("Select Product")
        self.qty_input.setText("1")
        self.purchase_rate_input.setText("0.0")
        self.retail_rate_input.setText("0.0")

    # --- Remove Selected Item ---
    def remove_selected_item(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Please select an item to remove")
            return

        # Remove by index instead of product_id
        self.invoice.remove_item_by_index(selected_row)
        self.refresh_items_table()

    def update_total_display(self):
        # Add a row for totals if needed, or update a label
        total = sum(item.quantity * item.retail_price for item in self.invoice.items)
        # You can add this to your UI layout
        if hasattr(self, 'total_label'):
            self.total_label.setText(f"Total: {total:.2f}")

    # def save_invoice(self):
    #     # --- Mandatory checks ---
    #     if not self.invoice.account_code:
    #         QMessageBox.warning(self, "Error", "Please select an account")
    #         return

    #     if len(self.invoice.items) == 0:
    #         QMessageBox.warning(self, "Error", "Add at least one product/item to invoice")
    #         return

    #     # --- Invoice date ---
    #     self.invoice.date = self.date_edit.date().toPyDate()

    #     # --- Advance can be zero ---
    #     try:
    #          # Convert to Decimal first to maintain consistency
    #         self.invoice.advance = Decimal(str(self.advance_input.text()))
    #     except ValueError:
    #         self.invoice.advance = Decimal('0')

    #     # --- Calculate totals ---
    #     self.invoice.calculate_totals()


    #     # Check if this is an existing invoice being updated
    #     is_update = hasattr(self.invoice, 'invoice_no') and self.invoice.invoice_no is not None

    #     if is_update:
    #         # --- UPDATE EXISTING INVOICE ---
    #         # First reverse all existing transactions
    #         TransactionService.reverse_transaction("sale", self.invoice.invoice_no)
            
    #         # Update the invoice in database
    #         SaleRepo.update_invoice(self.invoice)
    #         msg = "updated"
    #     else:
    #         # --- NEW INVOICE ---
    #         self.invoice.invoice_no = SaleRepo.get_next_invoice_no()
    #         SaleRepo.add_invoice(self.invoice)
    #         msg = "saved"

    #     # --- Post to Ledger via TransactionService ---
    #     remaining_amount = float(self.invoice.remaining_balance)  # Convert to float for ledger
    #     advance_amount = float(self.invoice.advance)  # Convert to float for ledger

        
    #     # 1️⃣ Post main sale amount (total - advance)
    #     if remaining_amount > 0:
    #         TransactionService.post_transaction(
    #             source="sale",
    #             source_id=self.invoice.invoice_no,
    #             date=self.invoice.date,
    #             debit_account=self.invoice.account_code,  # Customer
    #             credit_account=10000002,                      # Revenue account (example)
    #             amount=float(self.invoice.total_amount),
    #             description=f"Sale Invoice #{self.invoice.invoice_no}"
    #         )

    #     # 2️⃣ Post advance if any
    #     if self.invoice.advance > 0:
    #         TransactionService.post_transaction(
    #             source="ADVANCE",
    #             source_id=self.invoice.invoice_no,
    #             date=self.invoice.date,
    #             debit_account=10000001,                       # Cash account
    #             credit_account=self.invoice.account_code, # Customer
    #             amount=self.invoice.advance,
    #             description=f"Advance for Sale Invoice #{self.invoice.invoice_no}"
    #         )

    #     # --- Inform user ---
    #     QMessageBox.information(
    #         self, "Invoice", f"Invoice #{self.invoice.invoice_no} {msg} successfully!\n"
    #                         f"Total: {self.invoice.total_amount:.2f}\n"
    #                         f"Advance: {self.invoice.advance:.2f}\n"
    #                         f"Balance: {self.invoice.remaining_balance:.2f}"
    #     )

    #     # --- Reset for next invoice ---
    #     if not is_update:  # Only reset if it was a new invoice
    #         self.reset_form()





    def save_invoice(self):
        # --- Mandatory checks ---
        if not self.invoice.account_code:
            QMessageBox.warning(self, "Error", "Please select an account")
            return

        if len(self.invoice.items) == 0:
            QMessageBox.warning(self, "Error", "Add at least one product/item to invoice")
            return

        # --- Invoice date ---
        self.invoice.date = self.date_edit.date().toPyDate()

        # --- Advance can be zero ---
        try:
            # Convert to Decimal first to maintain consistency
            self.invoice.advance = Decimal(str(self.advance_input.text()))
        except ValueError:
            self.invoice.advance = Decimal('0')

        # --- Calculate totals ---
        self.invoice.calculate_totals()

        # Check if this is an existing invoice being updated
        is_update = hasattr(self.invoice, 'invoice_no') and self.invoice.invoice_no is not None

        if is_update:
            # --- UPDATE EXISTING INVOICE ---
            # First reverse all existing transactions using your existing method
            TransactionService.reverse_transaction("sale", self.invoice.invoice_no)
            TransactionService.reverse_transaction("ADVANCE", self.invoice.invoice_no)
            
            # Update the invoice in database
            SaleRepo.update_invoice(self.invoice)
            # Log the updated invoice to logs.txt
            try:
                log_update(
                    voucher_type="sale",
                    voucher_id=self.invoice.invoice_no,
                    details=f"date={self.invoice.date}, total={float(self.invoice.total_amount):.2f}, account={self.invoice.account_code}"
                )
            except Exception:
                pass
            msg = "updated"
        else:
            # --- NEW INVOICE ---
            self.invoice.invoice_no = SaleRepo.get_next_invoice_no()
            SaleRepo.add_invoice(self.invoice)
            msg = "saved"

        # --- Post to Ledger via TransactionService ---
        remaining_amount = float(self.invoice.remaining_balance)
        advance_amount = float(self.invoice.advance)
        total_amount = float(self.invoice.total_amount)

        # 1️⃣ Post main sale transaction (Revenue → Customer)
        if total_amount > 0:
            TransactionService.post_transaction(
                source="sale",
                source_id=self.invoice.invoice_no,
                date=self.invoice.date,
                debit_account=self.invoice.account_code,  # Customer (debtor)
                credit_account=10000002,                 # Revenue account
                amount=total_amount,
                description=f"Sale Invoice #{self.invoice.invoice_no}"
            )

        # 2️⃣ Post advance transaction (Cash → Customer) - only if advance > 0
        if self.invoice.advance > 0:
            TransactionService.post_transaction(
                source="ADVANCE",
                source_id=self.invoice.invoice_no,
                date=self.invoice.date,
                debit_account=10000001,                  # Cash account
                credit_account=self.invoice.account_code, # Customer (reduction in receivable)
                amount=advance_amount,
                description=f"Advance for Sale Invoice #{self.invoice.invoice_no}"
            )

        # --- Inform user ---
        QMessageBox.information(
            self, "Invoice", f"Invoice #{self.invoice.invoice_no} {msg} successfully!\n"
                            f"Total: {self.invoice.total_amount:.2f}\n"
                            f"Advance: {self.invoice.advance:.2f}\n"
                            f"Balance: {self.invoice.remaining_balance:.2f}"
        )

        # --- Reset for next invoice ---
        if not is_update:  # Only reset if it was a new invoice
            self.reset_form()

    def reset_form(self):
        self.invoice = SaleInvoice(account_code=self.invoice.account_code, invoice_date=self.invoice.date)
        self.table.setRowCount(0)
        self.invoice_no_label.setText(str(SaleRepo.get_next_invoice_no()))
        self.product_label.setText("Select Product")
        self.qty_input.setText("1")
        self.purchase_rate_input.setText("0.0")
        self.retail_rate_input.setText("0.0")
        self.advance_input.setText("0.0")

    def refresh_items_table(self):
        self.table.setRowCount(0)
        for item in self.invoice.items:
            prod = ProductRepo.get_product_by_id(item.product_id)
            prod_name = prod['name'] if isinstance(prod, dict) else prod.name
            subtotal = float(item.amount)  # Convert Decimal to float for display
            
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(item.product_id)))
            self.table.setItem(row, 1, QTableWidgetItem(prod_name))
            self.table.setItem(row, 2, QTableWidgetItem(str(item.quantity)))
            self.table.setItem(row, 3, QTableWidgetItem(f"{float(item.purchase_rate):.2f}"))
            self.table.setItem(row, 4, QTableWidgetItem(f"{float(item.retail_price):.2f}"))
            self.table.setItem(row, 5, QTableWidgetItem(f"{subtotal:.2f}"))
        
        # Update total display
        self.update_total_display()

    def update_total_display(self):
        total = sum(item.amount for item in self.invoice.items)

        try:
            advance = Decimal(self.advance_input.text()) if self.advance_input.text().strip() else Decimal('0')
        except (ValueError, decimal.InvalidOperation):
            advance = Decimal('0')

        balance = total - advance

        self.total_label.setText(f"{float(total):.2f}")
        self.advance_display.setText(f"{float(advance):.2f}")
        self.balance_label.setText(f"{float(balance):.2f}")

    # ui/sales_ui.py - add this helper method
    def decimal_to_float(self, decimal_value):
        """Safely convert Decimal to float for display"""
        if hasattr(decimal_value, '__float__'):
            return float(decimal_value)
        return 0.0

    def on_advance_changed(self, text):
        try:
            self.invoice.advance = Decimal(text) if text.strip() else Decimal('0')
        except (ValueError, decimal.InvalidOperation):
            self.invoice.advance = Decimal('0')

        # Recalculate totals
        self.invoice.calculate_totals()
        self.update_total_display()

    def closeEvent(self, event):
        app = QApplication.instance()
        if app and hasattr(self, "_enter_nav"):
            app.removeEventFilter(self._enter_nav)
        super().closeEvent(event)