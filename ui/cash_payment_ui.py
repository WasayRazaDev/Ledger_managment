
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,QApplication,
    QTableWidget, QTableWidgetItem, QMessageBox, QDateEdit, QInputDialog, QDialog
)
from PyQt5.QtCore import QDate
from database.cash_payment_repo import CashPayableRepo
from database.account_repo import AccountRepo
from core.cash_payment import CashPayable, CashPayableEntry
from ui.account_search_dialog import AccountSearchDialog
from core.transaction_service import TransactionService
from utils.update_logger import log_update
from ui.enter_navigation import EnterNavigationManager

class CashPayableUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cash Payable Module")
        self.resize(900, 600)
        
        # Apply the same enhanced custom stylesheet
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
        title_label = QLabel("Cash Payable Voucher Management")
        title_label.setObjectName("titleLabel")
        layout.addWidget(title_label)

        # --- Voucher Info ---
        info_layout = QHBoxLayout()
        info_layout.setSpacing(10)
        layout.addLayout(info_layout)

        info_layout.addWidget(QLabel("Voucher #:"))
        self.voucher_no_label = QLabel(str(CashPayableRepo.get_next_voucher_no()))
        info_layout.addWidget(self.voucher_no_label)
        info_layout.addSpacing(20)

        info_layout.addWidget(QLabel("Date:"))
        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setMinimumWidth(120)
        info_layout.addWidget(self.date_edit)
        info_layout.addStretch()

        # --- Account Selection ---
        account_layout = QHBoxLayout()
        account_layout.setSpacing(10)
        layout.addLayout(account_layout)

        account_layout.addWidget(QLabel("Supplier Account:"))
        self.account_label = QLabel("Select Supplier Account")
        self.account_label.setStyleSheet("background-color: #e9ecef; padding: 6px; border-radius: 4px;")
        account_layout.addWidget(self.account_label)
        account_layout.addSpacing(10)

        self.account_search_btn = QPushButton("Search Account")
        self.account_search_btn.setObjectName("searchButton")
        self.account_search_btn.clicked.connect(self.open_account_search)
        account_layout.addWidget(self.account_search_btn)
        account_layout.addStretch()

        # --- Entry Section ---
        entry_layout = QHBoxLayout()
        entry_layout.setSpacing(10)
        layout.addLayout(entry_layout)

        entry_layout.addWidget(QLabel("Amount:"))
        self.amount_input = QLineEdit("0.00")
        self.amount_input.setMaximumWidth(100)
        entry_layout.addWidget(self.amount_input)

        entry_layout.addWidget(QLabel("Description:"))
        self.desc_input = QLineEdit("Payment Made")
        entry_layout.addWidget(self.desc_input)

        self.add_entry_btn = QPushButton("Add Entry")
        self.add_entry_btn.setObjectName("actionButton")
        self.add_entry_btn.clicked.connect(self.add_entry)
        entry_layout.addWidget(self.add_entry_btn)

        # --- Entries Table ---
        self.entries_table = QTableWidget()
        self.entries_table.setColumnCount(4)
        self.entries_table.setHorizontalHeaderLabels(["Account Code", "Account Title", "Amount", "Description"])
        self.entries_table.setColumnWidth(0, 150)  # Code
        self.entries_table.setColumnWidth(1, 400)  # Title
        self.entries_table.setColumnWidth(2, 100)  # debit
        self.entries_table.setColumnWidth(3, 100)  # credit
        self.entries_table.setAlternatingRowColors(True)
        self.entries_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.entries_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.entries_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.entries_table)
        
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

        self.remove_entry_btn = QPushButton("Remove Entry")
        self.remove_entry_btn.setObjectName("dangerButton")
        self.remove_entry_btn.clicked.connect(self.remove_selected_entry)
        action_layout.addWidget(self.remove_entry_btn)

        self.clear_all_btn = QPushButton("Clear All")
        self.clear_all_btn.setObjectName("dangerButton")
        self.clear_all_btn.clicked.connect(self.clear_all_entries)
        action_layout.addWidget(self.clear_all_btn)

        action_layout.addStretch()

        # --- Save / Load Buttons ---
        io_layout = QHBoxLayout()
        io_layout.setSpacing(10)
        layout.addLayout(io_layout)

        self.load_btn = QPushButton("Load Voucher")
        self.load_btn.clicked.connect(self.load_voucher)
        io_layout.addWidget(self.load_btn)

        io_layout.addStretch()

        self.save_btn = QPushButton("Save Voucher")
        self.save_btn.setObjectName("actionButton")
        self.save_btn.clicked.connect(self.save_voucher)
        io_layout.addWidget(self.save_btn)

        # Create empty cash payable
        self.cash_payable = CashPayable(
            account_code="10000001",  # Cash account
            cp_date=self.date_edit.date().toPyDate()
        )

        # Define Enter behavior per widget
        self._enter_nav = EnterNavigationManager(
            self,
            rules={
                
                self.date_edit: {"mode": "tab_only"},
                self.account_search_btn: {"mode": "both"},
                self.amount_input: {"mode": "tab_only"},
                self.desc_input: {"mode": "tab_only"},
                self.add_entry_btn: { "mode": "both","next": self.account_search_btn},
            }
        )

        app = QApplication.instance()
        if app:
            app.installEventFilter(self._enter_nav)

    # ---------------- Methods ----------------

    def add_entry(self):
        if self.account_label.text() == "Select Supplier Account":
            QMessageBox.warning(self, "Error", "Please select a supplier account first")
            return

        account_code = self.account_label.text().split(" - ")[0]

        try:
            amount = float(self.amount_input.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "Amount must be a valid number")
            return

        if amount <= 0:
            QMessageBox.warning(self, "Error", "Amount must be greater than zero")
            return

        description = self.desc_input.text().strip() or "Payment Made"

        entry = CashPayableEntry(account_code=account_code, amount=amount, description=description)
        self.cash_payable.add_entry(entry)

        self.refresh_entries_table()

        # Reset entry fields
        self.account_label.setText("Select Supplier Account")
        self.amount_input.setText("0.00")
        self.desc_input.setText("Payment Made")

    def remove_selected_entry(self):
        selected_row = self.entries_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Please select an entry to remove")
            return

        # Remove by index
        self.cash_payable.remove_entry_by_index(selected_row)
        self.refresh_entries_table()

    def clear_all_entries(self):
        if not self.cash_payable.entries:
            return
            
        if QMessageBox.question(self, "Confirm Clear", "Clear all entries?") == QMessageBox.Yes:
            self.cash_payable.entries = []
            self.cash_payable.calculate_totals()
            self.refresh_entries_table()

    def refresh_entries_table(self):
        self.entries_table.setRowCount(0)

        for entry in self.cash_payable.entries:
            row_position = self.entries_table.rowCount()
            self.entries_table.insertRow(row_position)

            account_title = self.get_account_title(entry.account_code)

            self.entries_table.setItem(row_position, 0, QTableWidgetItem(entry.account_code))
            self.entries_table.setItem(row_position, 1, QTableWidgetItem(account_title))
            self.entries_table.setItem(row_position, 2, QTableWidgetItem(f"{float(entry.amount):.2f}"))
            self.entries_table.setItem(row_position, 3, QTableWidgetItem(entry.description))

        self.cash_payable.calculate_totals()
        self.total_label.setText(f"{float(self.cash_payable.total_amount):.2f}")

    def save_voucher(self):
        if not self.cash_payable.entries:
            QMessageBox.warning(self, "Error", "Please add at least one entry!")
            return

        self.cash_payable.date = self.date_edit.date().toPyDate()
        self.cash_payable.calculate_totals()

        # Check if this is an update or new voucher
        is_update = hasattr(self.cash_payable, 'voucher_id') and self.cash_payable.voucher_id is not None

        try:
            if is_update:
                # --- UPDATE EXISTING VOUCHER ---
                # First reverse all existing transactions
                TransactionService.reverse_transaction("CP", self.cash_payable.voucher_id)
                
                # Update the voucher in database
                CashPayableRepo.update_cash_payable(self.cash_payable)
                # Log the updated voucher to logs.txt
                try:
                    log_update(
                        voucher_type="CP",
                        voucher_id=self.cash_payable.voucher_id,
                        details=f"date={self.cash_payable.date}, total={float(self.cash_payable.total_amount):.2f}"
                    )
                except Exception:
                    pass
                msg = "updated"
            else:
                # --- NEW VOUCHER ---
                self.cash_payable.voucher_id = CashPayableRepo.add_cash_payable(self.cash_payable)
                msg = "saved"

            # Post to ledger (REVERSED: Debit Supplier, Credit Cash)
            for entry in self.cash_payable.entries:
                TransactionService.post_transaction(
                    source="CP",
                    source_id=self.cash_payable.voucher_id,
                    date=self.cash_payable.date,
                    debit_account=entry.account_code,  # Supplier account (DEBIT)
                    credit_account="10000001",  # Cash account (CREDIT)
                    amount=float(entry.amount),
                    description=entry.description
                )

            QMessageBox.information(self, "Success", 
                f"Cash Payable Voucher #{self.cash_payable.voucher_id} {msg} successfully!\n"
                f"Total: {float(self.cash_payable.total_amount):.2f}")

            # reset
            self.reset_form()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save voucher: {str(e)}")

    def reset_form(self):
        self.cash_payable = CashPayable(
            account_code="10000001",
            cp_date=self.date_edit.date().toPyDate()
        )
        self.entries_table.setRowCount(0)
        self.voucher_no_label.setText(str(CashPayableRepo.get_next_voucher_no()))
        self.total_label.setText("0.00")
        self.account_label.setText("Select Supplier Account")

    def load_voucher(self):
        voucher_id, ok = QInputDialog.getInt(self, "Load Voucher", "Enter Voucher ID:")
        if not ok:
            return

        voucher = CashPayableRepo.get_cash_payable(voucher_id)
        if not voucher:
            QMessageBox.warning(self, "Error", f"Voucher #{voucher_id} not found!")
            return

        self.cash_payable = voucher
        self.voucher_no_label.setText(str(voucher.voucher_id))
        self.date_edit.setDate(QDate(voucher.date.year, voucher.date.month, voucher.date.day))
        self.refresh_entries_table()

    def open_account_search(self):
        dialog = AccountSearchDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            acc = dialog.selected_account
            if acc:
                # Set the account label
                self.account_label.setText(f"{acc['account_code']} - {acc['title']}")
                
                # Update description automatically
                self.update_description()


    def update_description(self):
        label_text = self.account_label.text()
        
        if label_text and label_text != "Select Supplier Account":
            # Split "1002 - Star Suppliers" → ["1002", "Star Suppliers"]
            parts = label_text.split("-", 1)
            if len(parts) == 2:
                acc_title = parts[1].strip()  # "Star Suppliers"
            else:
                acc_title = label_text.strip()
                
            self.desc_input.setText(f"Payment made to {acc_title}")
        else:
            self.desc_input.setText("Payment Made")



    def get_account_title(self, account_code):
        account = AccountRepo.get_account_by_code(account_code)
        if account:
            return account.title
        return f"Account {account_code}"
    
    def closeEvent(self, event):
        app = QApplication.instance()
        if app and hasattr(self, "_enter_nav"):
            app.removeEventFilter(self._enter_nav)
        super().closeEvent(event)