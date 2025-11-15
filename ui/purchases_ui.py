
# ui/purchases_ui.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,QApplication,
    QTableWidget, QTableWidgetItem, QMessageBox, QDateEdit, QInputDialog, QDialog
)
from PyQt5.QtCore import QDate
from database.purchase_repo import PurchaseRepo
from database.account_repo import AccountRepo
from core.purchase import PurchaseInvoice, PurchaseItem
from ui.account_search_dialog import AccountSearchDialog
from ui.product_search_dialog import ProductSearchDialog
from core.transaction_service import TransactionService
from utils.update_logger import log_update
from ui.enter_navigation import EnterNavigationManager

class PurchaseUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Purchase Module")
        self.resize(900, 600)
        
        # Apply the same enhanced custom stylesheet as Sales UI
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

        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)
        self.setLayout(layout)

        # Title
        title_label = QLabel("Purchase Invoice Management")
        title_label.setObjectName("titleLabel")
        layout.addWidget(title_label)

        # --- Invoice Info ---
        info_layout = QHBoxLayout()
        info_layout.setSpacing(10)
        layout.addLayout(info_layout)

        info_layout.addWidget(QLabel("Purchase #:"))
        self.purchase_no_label = QLabel(str(PurchaseRepo.get_next_purchase_no()))
        info_layout.addWidget(self.purchase_no_label)
        info_layout.addSpacing(20)

        info_layout.addWidget(QLabel("Date:"))
        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setMinimumWidth(120)
        info_layout.addWidget(self.date_edit)
        info_layout.addStretch()

        # --- Supplier ---
        account_layout = QHBoxLayout()
        account_layout.setSpacing(10)
        layout.addLayout(account_layout)

        account_layout.addWidget(QLabel("Supplier:"))
        self.account_label = QLabel("Select Supplier")
        self.account_label.setStyleSheet("background-color: #e9ecef; padding: 6px; border-radius: 4px;")
        account_layout.addWidget(self.account_label)
        account_layout.addSpacing(10)

        self.account_search_btn = QPushButton("Search Supplier")
        self.account_search_btn.setObjectName("searchButton")
        self.account_search_btn.clicked.connect(self.open_account_search)
        account_layout.addWidget(self.account_search_btn)
        account_layout.addStretch()

        # --- Product Section ---
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
        self.product_search_btn.clicked.connect(self.open_product_search)
        product_layout.addWidget(self.product_search_btn)
        product_layout.addSpacing(20)

        product_layout.addWidget(QLabel("Qty:"))
        self.qty_input = QLineEdit("1")
        self.qty_input.setMaximumWidth(60)
        product_layout.addWidget(self.qty_input)

        product_layout.addWidget(QLabel("Rate:"))
        self.purchase_rate_input = QLineEdit("0.0")
        self.purchase_rate_input.setMaximumWidth(80)
        product_layout.addWidget(self.purchase_rate_input)

        self.add_item_btn = QPushButton("Add Item")
        self.add_item_btn.setObjectName("actionButton")
        self.add_item_btn.clicked.connect(self.add_item)
        product_layout.addWidget(self.add_item_btn)

        # --- Items Table ---
        self.items_table = QTableWidget()
        self.items_table.setColumnCount(5)
        self.items_table.setHorizontalHeaderLabels(["Product ID", "Product Name", "Quantity", "Purchase Rate", "Line Total"])
        self.items_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.items_table)
        
        # --- Total Label ---
        total_layout = QHBoxLayout()
        total_layout.setSpacing(20)
        layout.addLayout(total_layout)
        
        total_layout.addWidget(QLabel("Total Amount:"))
        self.total_label = QLabel("0.00")
        self.total_label.setStyleSheet("font-weight: bold; color: #2c3e50; background-color: #e9ecef; padding: 6px; border-radius: 4px; min-width: 80px;")
        total_layout.addWidget(self.total_label)
        total_layout.addStretch()

        # --- Action Buttons ---
        action_layout = QHBoxLayout()
        action_layout.setSpacing(10)
        layout.addLayout(action_layout)

        self.remove_item_btn = QPushButton("Remove Item")
        self.remove_item_btn.setObjectName("dangerButton")
        self.remove_item_btn.clicked.connect(self.remove_selected_item)
        action_layout.addWidget(self.remove_item_btn)

        self.clear_all_btn = QPushButton("Clear All")
        self.clear_all_btn.setObjectName("dangerButton")
        self.clear_all_btn.clicked.connect(self.clear_all_items)
        action_layout.addWidget(self.clear_all_btn)

        action_layout.addStretch()

        # --- Save / Load Buttons ---
        io_layout = QHBoxLayout()
        io_layout.setSpacing(10)
        layout.addLayout(io_layout)

        self.load_btn = QPushButton("Load Purchase")
        self.load_btn.clicked.connect(self.load_purchase)
        io_layout.addWidget(self.load_btn)

        io_layout.addStretch()

        self.save_btn = QPushButton("Save Purchase")
        self.save_btn.setObjectName("actionButton")
        self.save_btn.clicked.connect(self.save_purchase)
        io_layout.addWidget(self.save_btn)

        # Create empty invoice
        self.invoice = PurchaseInvoice(
            account_code=None,
            purchase_date=self.date_edit.date().toPyDate()
        )

        self._enter_nav = EnterNavigationManager(
        self,
        rules={
                
            self.date_edit: {"mode": "tab_only"},
            self.account_search_btn: {"mode": "both"},
            self.product_search_btn: {"mode": "both"},
            self.qty_input: {"mode": "tab_only"},
            self.purchase_rate_input: {"mode": "tab_only"},
            self.add_item_btn: { "mode": "both","next": self.product_search_btn},
            }
        )

        app = QApplication.instance()
        if app:
            app.installEventFilter(self._enter_nav)

    # ---------------- Methods ----------------
    # ALL FUNCTIONAL METHODS REMAIN EXACTLY THE SAME
    # Only the visual styling has been applied

    def add_item(self):
        if self.product_label.text() == "Select Product":
            QMessageBox.warning(self, "Error", "Please select a product first")
            return

        product_id = self.product_label.text().split(" - ")[0]

        try:
            quantity = int(self.qty_input.text())
            purchase_rate = float(self.purchase_rate_input.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "Quantity and Purchase Rate must be numbers")
            return

        if quantity <= 0 or purchase_rate <= 0:
            QMessageBox.warning(self, "Error", "Quantity and Purchase Rate must be greater than zero")
            return

        item = PurchaseItem(product_id=product_id, quantity=quantity, purchase_rate=purchase_rate)
        self.invoice.add_item(item)

        self.refresh_items_table()

        # Reset item fields
        self.product_label.setText("Select Product")
        self.qty_input.setText("1")
        self.purchase_rate_input.setText("0.0")

    def remove_selected_item(self):
        selected_row = self.items_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Please select an item to remove")
            return

        # Remove by index instead of product_id
        self.invoice.remove_item_by_index(selected_row)
        self.refresh_items_table()

    def clear_all_items(self):
        if not self.invoice.items:
            return
            
        if QMessageBox.question(self, "Confirm Clear", "Clear all items?") == QMessageBox.Yes:
            self.invoice.items = []
            self.invoice.calculate_totals()
            self.refresh_items_table()

    def refresh_items_table(self):
        self.items_table.setRowCount(0)

        for item in self.invoice.items:
            row_position = self.items_table.rowCount()
            self.items_table.insertRow(row_position)

            product_name = self.get_product_name(item.product_id)
            line_total = float(item.amount)

            self.items_table.setItem(row_position, 0, QTableWidgetItem(str(item.product_id)))
            self.items_table.setItem(row_position, 1, QTableWidgetItem(product_name))
            self.items_table.setItem(row_position, 2, QTableWidgetItem(str(item.quantity)))
            self.items_table.setItem(row_position, 3, QTableWidgetItem(f"{float(item.purchase_rate):.2f}"))
            self.items_table.setItem(row_position, 4, QTableWidgetItem(f"{line_total:.2f}"))

        self.invoice.calculate_totals()
        self.total_label.setText(f"{float(self.invoice.total_amount):.2f}")


    def save_purchase(self):
        if not self.invoice.account_code:
            QMessageBox.warning(self, "Error", "Please select a supplier!")
            return

        if not self.invoice.items:
            QMessageBox.warning(self, "Error", "Please add at least one item!")
            return

        self.invoice.date = self.date_edit.date().toPyDate()
        self.invoice.calculate_totals()

        # Check if this is an update or new purchase
        is_update = hasattr(self.invoice, 'purchase_id') and self.invoice.purchase_id is not None

        if is_update:
            # --- UPDATE EXISTING PURCHASE ---
            # First reverse all existing transactions
            TransactionService.reverse_transaction("purchase", self.invoice.purchase_id)
            
            # Update the purchase in database
            PurchaseRepo.update_purchase(self.invoice)
            # Log the updated purchase to logs.txt
            try:
                log_update(
                    voucher_type="purchase",
                    voucher_id=self.invoice.purchase_id,
                    details=f"date={self.invoice.date}, total={float(self.invoice.total_amount):.2f}, account={self.invoice.account_code}"
                )
            except Exception:
                pass
            msg = "updated"
        else:
            # --- NEW PURCHASE ---
            self.invoice.purchase_id = PurchaseRepo.add_purchase(self.invoice)
            msg = "saved"

        # --- Post EACH ITEM separately to Ledger ---
        posted_count = 0
        for item in self.invoice.items:
            try:
                item_amount = float(item.amount)
                product_name = self.get_product_name(item.product_id)
                
                TransactionService.post_transaction(
                    source="purchase",
                    source_id=self.invoice.purchase_id,
                    date=self.invoice.date,
                    debit_account=10000003,  # Stock/Inventory account
                    credit_account=self.invoice.account_code,  # Supplier account
                    amount=item_amount,
                    description=f"Purchased {product_name} - {item.quantity} units "
                )
                posted_count += 1
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to post item: {e}")
                return

        QMessageBox.information(self, "Purchase", 
            f"Purchase #{self.invoice.purchase_id} {msg} successfully!\n"
            f"{posted_count} items posted to ledger.")

        # reset
        self.reset_form()

    def reset_form(self):
        self.invoice = PurchaseInvoice(
            account_code=self.invoice.account_code if hasattr(self.invoice, 'account_code') else None,
            purchase_date=self.date_edit.date().toPyDate()
        )
        self.items_table.setRowCount(0)
        self.purchase_no_label.setText(str(PurchaseRepo.get_next_purchase_no()))
        self.total_label.setText("0.00")
        self.account_label.setText("Select Supplier")
        self.product_label.setText("Select Product")

    def load_purchase(self):
        purchase_no, ok = QInputDialog.getInt(self, "Load Purchase", "Enter Purchase #:")
        if not ok:
            return

        invoice = PurchaseRepo.get_purchase(purchase_no)
        if not invoice:
            QMessageBox.warning(self, "Error", f"Purchase #{purchase_no} not found!")
            return

        self.invoice = invoice
        self.purchase_no_label.setText(str(invoice.purchase_id))
        self.date_edit.setDate(QDate(invoice.date.year, invoice.date.month, invoice.date.day))
        account = AccountRepo.get_account_by_code(invoice.account_code)
        self.account_label.setText(f"{invoice.account_code} - {account.title}")
        self.refresh_items_table()

    def open_account_search(self):
        dialog = AccountSearchDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            acc = dialog.selected_account
            if acc:
                self.invoice.account_code = acc["account_code"]
                self.invoice.title = acc.get("title", "")
                self.account_label.setText(f"{acc['account_code']} - {acc['title']}")

    def open_product_search(self):
        dialog = ProductSearchDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            prod = dialog.selected_product
            if prod:
                self.product_label.setText(f"{prod['product_id']} - {prod['name']}")

    def get_product_name(self, product_id):
        product = PurchaseRepo.get_product(product_id)
        if product:
            return product["name"]
        return f"Product {product_id}"
    
    def closeEvent(self, event):
        app = QApplication.instance()
        if app and hasattr(self, "_enter_nav"):
            app.removeEventFilter(self._enter_nav)
        super().closeEvent(event)