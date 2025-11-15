
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,QApplication,
    QTableWidget, QTableWidgetItem, QMessageBox, QDateEdit, QInputDialog, QDialog
)
from PyQt5.QtCore import QDate,Qt
from database.cash_receivable_repo import CashReceivableRepo
from database.account_repo import AccountRepo
from database.reports_repo import ReportRepo
from core.cash_receivable import CashReceivable, CashReceivableEntry
from ui.account_search_dialog import AccountSearchDialog
from core.transaction_service import TransactionService
from utils.update_logger import log_update
from ui.enter_navigation import EnterNavigationManager

class CashReceivableUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cash Receivable Module")
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
        title_label = QLabel("Cash Receivable Voucher Management")
        title_label.setObjectName("titleLabel")
        layout.addWidget(title_label)

        # --- Voucher Info ---
        info_layout = QHBoxLayout()
        info_layout.setSpacing(10)
        layout.addLayout(info_layout)

        info_layout.addWidget(QLabel("Voucher #:"))
        self.voucher_no_label = QLabel(str(CashReceivableRepo.get_next_voucher_no()))
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

        account_layout.addWidget(QLabel("Customer Account:"))
        self.account_label = QLabel("Select Customer Account")
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
        self.desc_input = QLineEdit("Payment Received")
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

        # Create empty cash receivable
        self.cash_receivable = CashReceivable(
            account_code="10000001",  # Cash account
            cr_date=self.date_edit.date().toPyDate()
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
        if self.account_label.text() == "Select Customer Account":
            QMessageBox.warning(self, "Error", "Please select a customer account first")
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

        description = self.desc_input.text().strip() or "Payment Received"

        entry = CashReceivableEntry(account_code=account_code, amount=amount, description=description)
        self.cash_receivable.add_entry(entry)

        self.refresh_entries_table()

        # Reset entry fields
        self.account_label.setText("Select Customer Account")
        self.amount_input.setText("0.00")
        self.desc_input.setText("Payment Received")

    def remove_selected_entry(self):
        selected_row = self.entries_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Please select an entry to remove")
            return

        # Remove by index
        self.cash_receivable.remove_entry_by_index(selected_row)
        self.refresh_entries_table()

    def clear_all_entries(self):
        if not self.cash_receivable.entries:
            return
            
        if QMessageBox.question(self, "Confirm Clear", "Clear all entries?") == QMessageBox.Yes:
            self.cash_receivable.entries = []
            self.cash_receivable.calculate_totals()
            self.refresh_entries_table()

    def refresh_entries_table(self):
        self.entries_table.setRowCount(0)

        for entry in self.cash_receivable.entries:
            row_position = self.entries_table.rowCount()
            self.entries_table.insertRow(row_position)

            account_title = self.get_account_title(entry.account_code)

            self.entries_table.setItem(row_position, 0, QTableWidgetItem(entry.account_code))
            self.entries_table.setItem(row_position, 1, QTableWidgetItem(account_title))
            self.entries_table.setItem(row_position, 2, QTableWidgetItem(f"{float(entry.amount):.2f}"))
            self.entries_table.setItem(row_position, 3, QTableWidgetItem(entry.description))

        self.cash_receivable.calculate_totals()
        self.total_label.setText(f"{float(self.cash_receivable.total_amount):.2f}")

    def save_voucher(self):
        if not self.cash_receivable.entries:
            QMessageBox.warning(self, "Error", "Please add at least one entry!")
            return

        self.cash_receivable.date = self.date_edit.date().toPyDate()
        self.cash_receivable.calculate_totals()

        # Check if this is an update or new voucher
        is_update = hasattr(self.cash_receivable, 'voucher_id') and self.cash_receivable.voucher_id is not None

        try:
            if is_update:
                # --- UPDATE EXISTING VOUCHER ---
                # First reverse all existing transactions
                TransactionService.reverse_transaction("CR", self.cash_receivable.voucher_id)
                
                # Update the voucher in database
                CashReceivableRepo.update_cash_receivable(self.cash_receivable)
                # Log the updated voucher to logs.txt
                try:
                    log_update(
                        voucher_type="CR",
                        voucher_id=self.cash_receivable.voucher_id,
                        details=f"date={self.cash_receivable.date}, total={float(self.cash_receivable.total_amount):.2f}"
                    )
                except Exception:
                    pass
                msg = "updated"
            else:
                # --- NEW VOUCHER ---
                self.cash_receivable.voucher_id = CashReceivableRepo.add_cash_receivable(self.cash_receivable)
                msg = "saved"

            # Post to ledger
            for entry in self.cash_receivable.entries:
                TransactionService.post_transaction(
                    source="CR",
                    source_id=self.cash_receivable.voucher_id,
                    date=self.cash_receivable.date,
                    debit_account="10000001",  # Cash account
                    credit_account=entry.account_code,  # Customer account
                    amount=float(entry.amount),
                    description=entry.description
                )

            QMessageBox.information(self, "Success", 
                f"Cash Receivable Voucher #{self.cash_receivable.voucher_id} {msg} successfully!\n"
                f"Total: {float(self.cash_receivable.total_amount):.2f}")




            # ✅ Ask if user wants to print
            reply = QMessageBox.question(
                self,
                "Print Voucher",
                "Do you want to print this voucher?",
                QMessageBox.Yes | QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                try:
                    self.report_window = CRReportUI(self.cash_receivable.voucher_id)
                    self.report_window.show()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to open report: {str(e)}")

            # Reset form after successful save (and optional print prompt)
            self.reset_form()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save voucher: {str(e)}")
            # reset
            self.reset_form()

            

    def reset_form(self):
        self.cash_receivable = CashReceivable(
            account_code="10000001",
            cr_date=self.date_edit.date().toPyDate()
        )
        # Clear table data and selection
        self.entries_table.setRowCount(0)
        self.entries_table.clearSelection()
        # Reset voucher number and date
        self.voucher_no_label.setText(str(CashReceivableRepo.get_next_voucher_no()))
        self.date_edit.setDate(QDate.currentDate())
        # Reset totals and input fields
        self.total_label.setText("0.00")
        self.account_label.setText("Select Customer Account")
        self.amount_input.setText("0.00")
        self.desc_input.setText("Payment Received")

    def load_voucher(self):
        voucher_id, ok = QInputDialog.getInt(self, "Load Voucher", "Enter Voucher ID:")
        if not ok:
            return

        voucher = CashReceivableRepo.get_cash_receivable(voucher_id)
        if not voucher:
            QMessageBox.warning(self, "Error", f"Voucher #{voucher_id} not found!")
            return

        self.cash_receivable = voucher
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
        
        if label_text and label_text != "Select Customer Account":
            # Split "1002 - Star Suppliers" → ["1002", "Star Suppliers"]
            parts = label_text.split("-", 1)
            if len(parts) == 2:
                acc_title = parts[1].strip()  # "Star Suppliers"
            else:
                acc_title = label_text.strip()
                
            self.desc_input.setText(f"Payment Received from {acc_title}")
        else:
            self.desc_input.setText("Payment Received")

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





import csv
import os
from datetime import datetime
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, 
                             QTableWidgetItem, QPushButton, QHeaderView, QMessageBox, QFileDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class CRReportUI(QWidget):
    def __init__(self, voucher_id):
        super().__init__()
        self.voucher_id = voucher_id
        self.setWindowTitle(f"Cash Receivable Report - Voucher #{voucher_id}")
        self.resize(1000, 600)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Title
        self.title_label = QLabel(f"Cash Receivable Voucher Report - Voucher #{voucher_id}")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 16pt; 
                font-weight: bold; 
                padding: 12px;
                background-color: #2c3e50;
                color: white;
                border-radius: 5px;
                margin: 5px;
            }
        """)
        layout.addWidget(self.title_label)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Account Code", "Account Title", "CR Amount",
            "Total Debit", "Total Recoveries", "Balance"
        ])
        
        # Table styling and spacing
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #f8f9fa;
                alternate-background-color: #e9ecef;
                gridline-color: #dee2e6;
                font-size: 10pt;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #dee2e6;
            }
            QTableWidget::item:selected {
                background-color: #007bff;
                color: white;
            }
            QHeaderView::section {
                background-color: #343a40;
                color: white;
                font-weight: bold;
                padding: 8px;
                border: 1px solid #495057;
            }
        """)
        
        # Column width settings
        self.table.setColumnWidth(0, 120)  # Account Code
        self.table.setColumnWidth(1, 250)  # Account Title
        self.table.setColumnWidth(2, 120)  # Entry Amount
        self.table.setColumnWidth(3, 120)  # Total Debit
        self.table.setColumnWidth(4, 140)  # Total Recoveries
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)  # Balance
        
        # Enable alternating row colors
        self.table.setAlternatingRowColors(True)
        
        # Enable sorting
        self.table.setSortingEnabled(True)
        
        # Set selection behavior
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        
        layout.addWidget(self.table)

        # Button layout
        button_layout = QHBoxLayout()
        
        # Export to CSV button
        self.export_btn = QPushButton("Export to CSV")
        self.export_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 4px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
        """)
        self.export_btn.clicked.connect(self.export_to_csv)
        button_layout.addWidget(self.export_btn)
        
        # Spacer
        button_layout.addStretch()
        
        # Close button
        self.close_btn = QPushButton("Close")
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 4px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
            QPushButton:pressed {
                background-color: #bd2130;
            }
        """)
        self.close_btn.clicked.connect(self.close)
        button_layout.addWidget(self.close_btn)
        
        layout.addLayout(button_layout)

        # Load data
        self.load_data()

    def load_data(self):
        try:
            rows = ReportRepo.get_cr_voucher_entries(self.voucher_id)
            
            if not rows:
                QMessageBox.information(self, "No Data", "No entries found for this voucher.")
                return

            self.table.setRowCount(len(rows))
            
            # Set font for better readability
            font = QFont()
            font.setPointSize(9)
            
            total_entry_amount = 0
            total_debit = 0
            total_recoveries = 0
            total_balance = 0
            
            for row_idx, row in enumerate(rows):
                # Account Code
                code_item = QTableWidgetItem(str(row.get("account_code", "")))
                code_item.setFont(font)
                self.table.setItem(row_idx, 0, code_item)
                
                # Account Title
                title_item = QTableWidgetItem(str(row.get("title", "")))
                title_item.setFont(font)
                self.table.setItem(row_idx, 1, title_item)
                
                # Entry Amount
                entry_amount = float(row.get('entry_amount', 0))
                entry_item = QTableWidgetItem(f"{entry_amount:,.2f}")
                entry_item.setFont(font)
                entry_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.table.setItem(row_idx, 2, entry_item)
                total_entry_amount += entry_amount
                
                # Total Debit
                total_debit_val = float(row.get('total_debit', 0))
                debit_item = QTableWidgetItem(f"{total_debit_val:,.2f}")
                debit_item.setFont(font)
                debit_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.table.setItem(row_idx, 3, debit_item)
                total_debit += total_debit_val
                
                # Total Recoveries
                total_recoveries_val = float(row.get('total_recoveries', 0))
                recoveries_item = QTableWidgetItem(f"{total_recoveries_val:,.2f}")
                recoveries_item.setFont(font)
                recoveries_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.table.setItem(row_idx, 4, recoveries_item)
                total_recoveries += total_recoveries_val
                
                # Balance
                balance_val = float(row.get('balance', 0))
                balance_item = QTableWidgetItem(f"{balance_val:,.2f}")
                balance_item.setFont(font)
                balance_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                
                # Color code negative balances
                if balance_val < 0:
                    balance_item.setForeground(Qt.red)
                elif balance_val > 0:
                    balance_item.setForeground(Qt.darkGreen)
                    
                self.table.setItem(row_idx, 5, balance_item)
                total_balance += balance_val
            
            # Add totals row
            self.add_totals_row(total_entry_amount, total_debit, total_recoveries, total_balance)
            
            # Resize rows to fit content
            self.table.resizeRowsToContents()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load data: {str(e)}")

    def add_totals_row(self, entry_amount, debit, recoveries, balance):
        """Add a totals row at the bottom of the table"""
        row_pos = self.table.rowCount()
        self.table.insertRow(row_pos)
        
        # Create bold font for totals
        font = QFont()
        font.setPointSize(9)
        font.setBold(True)
        
        # Totals label
        totals_item = QTableWidgetItem("TOTALS")
        totals_item.setFont(font)
        totals_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.table.setItem(row_pos, 1, totals_item)
        
        # Entry Amount total
        entry_item = QTableWidgetItem(f"{entry_amount:,.2f}")
        entry_item.setFont(font)
        entry_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        entry_item.setBackground(Qt.lightGray)
        self.table.setItem(row_pos, 2, entry_item)
        
        # Debit total
        debit_item = QTableWidgetItem(f"{debit:,.2f}")
        debit_item.setFont(font)
        debit_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        debit_item.setBackground(Qt.lightGray)
        self.table.setItem(row_pos, 3, debit_item)
        
        # Recoveries total
        recoveries_item = QTableWidgetItem(f"{recoveries:,.2f}")
        recoveries_item.setFont(font)
        recoveries_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        recoveries_item.setBackground(Qt.lightGray)
        self.table.setItem(row_pos, 4, recoveries_item)
        
        # Balance total
        balance_item = QTableWidgetItem(f"{balance:,.2f}")
        balance_item.setFont(font)
        balance_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        balance_item.setBackground(Qt.lightGray)
        
        # Color code total balance
        if balance < 0:
            balance_item.setForeground(Qt.red)
        elif balance > 0:
            balance_item.setForeground(Qt.darkGreen)
            
        self.table.setItem(row_pos, 5, balance_item)



    def export_to_csv(self):
        """Export table data to CSV file"""
        try:
            if self.table.rowCount() == 0:
                QMessageBox.warning(self, "No Data", "No data to export.")
                return

            # Get save file path
            default_filename = f"cr_voucher_{self.voucher_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Export to CSV", default_filename, "CSV Files (*.csv)"
            )
            
            if not file_path:
                return  # User cancelled
            
            # Ensure .csv extension
            if not file_path.lower().endswith('.csv'):
                file_path += '.csv'
            
            # Write CSV file
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write headers
                headers = []
                for col in range(self.table.columnCount()):
                    headers.append(self.table.horizontalHeaderItem(col).text())
                writer.writerow(headers)
                
                # Write data rows (excluding the totals row)
                for row in range(self.table.rowCount() - 1):  # Exclude last row (totals)
                    row_data = []
                    for col in range(self.table.columnCount()):
                        item = self.table.item(row, col)
                        if item is not None:
                            # Remove formatting for numbers
                            text = item.text().replace(',', '')
                            row_data.append(text)
                        else:
                            row_data.append('')
                    writer.writerow(row_data)
            
            QMessageBox.information(self, "Export Successful", 
                                  f"Data exported successfully to:\n{file_path}")
            
        except Exception as e:
            QMessageBox.critical(self, "Export Failed", f"Failed to export data: {str(e)}")

    def closeEvent(self, event):
        """Handle window close event"""
        event.accept()