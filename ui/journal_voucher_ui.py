
# ui/journal_voucher_ui.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,QGroupBox,QFormLayout,QApplication,
    QTableWidget, QTableWidgetItem, QMessageBox, QDateEdit, QInputDialog, QDialog
)
from PyQt5.QtCore import QDate
from database.journal_voucher_repo import JournalVoucherRepo
from database.account_repo import AccountRepo
from core.journal_voucher import JournalVoucher, JournalVoucherEntry
from ui.account_search_dialog import AccountSearchDialog
from core.transaction_service import TransactionService
from utils.update_logger import log_update
from ui.enter_navigation import EnterNavigationManager

class JournalVoucherUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Journal Voucher Module")
        self.resize(900, 650)
        
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
            QPushButton#actionButton {
                background-color: #2ecc71;
            }
            QPushButton#actionButton:hover {
                background-color: #27ae60;
            }
            QPushButton#dangerButton {
                background-color: #e74c3c;
            }
            QPushButton#dangerButton:hover {
                background-color: #c0392b;
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
            }
            QTableWidget {
                gridline-color: #dee2e6;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                background-color: white;
                alternate-background-color: #f8f9fa;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)
        self.setLayout(layout)

        # Title
        title_label = QLabel("Journal Voucher Management")
        title_label.setObjectName("titleLabel")
        layout.addWidget(title_label)

        # --- Voucher Info ---
        info_layout = QHBoxLayout()
        info_layout.setSpacing(10)
        layout.addLayout(info_layout)

        info_layout.addWidget(QLabel("Voucher #:"))
        self.voucher_no_label = QLabel(str(JournalVoucherRepo.get_next_voucher_no()))
        info_layout.addWidget(self.voucher_no_label)
        info_layout.addSpacing(20)

        info_layout.addWidget(QLabel("Date:"))
        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setMinimumWidth(120)
        info_layout.addWidget(self.date_edit)
        info_layout.addStretch()

        # --- Narration ---
        narration_layout = QHBoxLayout()
        narration_layout.setSpacing(10)
        layout.addLayout(narration_layout)
        
        narration_layout.addWidget(QLabel("Narration:"))
        self.narration_input = QLineEdit()
        self.narration_input.setPlaceholderText("Enter voucher narration")
        narration_layout.addWidget(self.narration_input)

        # --- Entry Section (Improved layout) ---
        entry_group = QGroupBox("Add Journal Entry")
        entry_layout = QFormLayout(entry_group)
        entry_layout.setHorizontalSpacing(15)
        entry_layout.setVerticalSpacing(8)
        layout.addWidget(entry_group)

        # Account selection row
        account_layout = QHBoxLayout()
        account_layout.setSpacing(10)
        self.account_label = QLabel("Select Account")
        self.account_label.setStyleSheet("background-color: #e9ecef; padding: 6px; border-radius: 4px; min-width: 200px;")
        account_layout.addWidget(self.account_label)
        
        self.account_search_btn = QPushButton("Search Account")
        self.account_search_btn.setObjectName("searchButton")
        self.account_search_btn.clicked.connect(self.open_account_search)
        account_layout.addWidget(self.account_search_btn)
        account_layout.addStretch()
        
        entry_layout.addRow(QLabel("Account:"), account_layout)

        # Amounts row
        amounts_layout = QHBoxLayout()
        amounts_layout.setSpacing(15)
        
        debit_layout = QHBoxLayout()
        debit_layout.addWidget(QLabel("Debit:"))
        self.debit_input = QLineEdit("0.00")
        self.debit_input.setMaximumWidth(120)
        debit_layout.addWidget(self.debit_input)
        amounts_layout.addLayout(debit_layout)
        
        credit_layout = QHBoxLayout()
        credit_layout.addWidget(QLabel("Credit:"))
        self.credit_input = QLineEdit("0.00")
        self.credit_input.setMaximumWidth(120)
        credit_layout.addWidget(self.credit_input)
        amounts_layout.addLayout(credit_layout)
        
        amounts_layout.addStretch()
        entry_layout.addRow(QLabel("Amounts:"), amounts_layout)

        # Description row
        desc_layout = QHBoxLayout()
        desc_layout.setSpacing(10)
        self.desc_input = QLineEdit("Journal entry")
        desc_layout.addWidget(self.desc_input)
        
        self.add_entry_btn = QPushButton("Add Entry")
        self.add_entry_btn.setObjectName("actionButton")
        self.add_entry_btn.clicked.connect(self.add_entry)
        desc_layout.addWidget(self.add_entry_btn)
        
        entry_layout.addRow(QLabel("Description:"), desc_layout)

        # --- Entries Table ---
        table_label = QLabel("Journal Entries")
        table_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        layout.addWidget(table_label)
        
        self.entries_table = QTableWidget()
        self.entries_table.setColumnCount(6)
        self.entries_table.setHorizontalHeaderLabels(["Account Code", "Account Title", "Debit", "Credit", "Description", "Action"])
        self.entries_table.setColumnWidth(0, 150)  # Code
        self.entries_table.setColumnWidth(1, 400)  # Title
        self.entries_table.setColumnWidth(2, 100)  # debit
        self.entries_table.setColumnWidth(3, 100)  # credit
        self.entries_table.setColumnWidth(4,100) #description
        self.entries_table.setColumnWidth(5,100) # action
        self.entries_table.setAlternatingRowColors(True)
        self.entries_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.entries_table.setEditTriggers(QTableWidget.NoEditTriggers)

        self.entries_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.entries_table)
        
        # --- Totals Display ---
        totals_layout = QHBoxLayout()
        totals_layout.setSpacing(20)
        layout.addLayout(totals_layout)
        
        totals_layout.addWidget(QLabel("Total Debit:"))
        self.total_debit_label = QLabel("0.00")
        self.total_debit_label.setStyleSheet("font-weight: bold; color: #2c3e50; background-color: #e9ecef; padding: 6px; border-radius: 4px; min-width: 80px;")
        totals_layout.addWidget(self.total_debit_label)

        totals_layout.addWidget(QLabel("Total Credit:"))
        self.total_credit_label = QLabel("0.00")
        self.total_credit_label.setStyleSheet("font-weight: bold; color: #2c3e50; background-color: #e9ecef; padding: 6px; border-radius: 4px; min-width: 80px;")
        totals_layout.addWidget(self.total_credit_label)

        totals_layout.addStretch()

        # --- Save / Load Buttons ---
        io_layout = QHBoxLayout()
        io_layout.setSpacing(10)
        layout.addLayout(io_layout)

        self.load_btn = QPushButton("Load Voucher")
        self.load_btn.clicked.connect(self.load_voucher)
        io_layout.addWidget(self.load_btn)

        self.clear_all_btn = QPushButton("Clear All")
        self.clear_all_btn.setObjectName("dangerButton")
        self.clear_all_btn.clicked.connect(self.clear_all_entries)
        io_layout.addWidget(self.clear_all_btn)

        io_layout.addStretch()

        self.save_btn = QPushButton("Save Voucher")
        self.save_btn.setObjectName("actionButton")
        self.save_btn.clicked.connect(self.save_voucher)
        io_layout.addWidget(self.save_btn)

        # Create empty journal voucher
        self.journal_voucher = JournalVoucher(jv_date=self.date_edit.date().toPyDate())

        # Define Enter behavior per widget
        self._enter_nav = EnterNavigationManager(
            self,
            rules={
                
                self.date_edit: {"mode": "tab_only"},
                self.narration_input:{ "mode" : "tab_only"},
                self.account_search_btn: {"mode": "both"},
                self.debit_input: {"mode": "tab_only"},
                self.credit_input: {"mode": "tab_only"},
                self.desc_input: {"mode": "tab_only"},
                self.add_entry_btn: { "mode": "both","next": self.account_search_btn},
            }
        )

        app = QApplication.instance()
        if app:
            app.installEventFilter(self._enter_nav)

    # ---------------- Methods ----------------

    def add_entry(self):
        if self.account_label.text() == "Select Account":
            QMessageBox.warning(self, "Error", "Please select an account first")
            return

        account_code = self.account_label.text().split(" - ")[0]

        try:
            debit_amount = float(self.debit_input.text()) if self.debit_input.text() else 0.0
            credit_amount = float(self.credit_input.text()) if self.credit_input.text() else 0.0
        except ValueError:
            QMessageBox.warning(self, "Error", "Amounts must be valid numbers")
            return

        if debit_amount < 0 or credit_amount < 0:
            QMessageBox.warning(self, "Error", "Amounts cannot be negative")
            return

        if debit_amount > 0 and credit_amount > 0:
            QMessageBox.warning(self, "Error", "Cannot have both debit and credit for the same entry")
            return

        if debit_amount == 0 and credit_amount == 0:
            QMessageBox.warning(self, "Error", "Please enter either debit or credit amount")
            return

        

        description = self.desc_input.text().strip() or "Journal entry"

        entry = JournalVoucherEntry(account_code=account_code, credit=credit_amount,debit=debit_amount, description=description)
        self.journal_voucher.add_entry(entry)

        self.refresh_entries_table()

        # Reset entry fields
        self.account_label.setText("Select Account")
        self.debit_input.setText("0.00")
        self.credit_input.setText("0.00")
        self.desc_input.setText("Journal entry")

    def remove_entry(self, row):
        self.journal_voucher.remove_entry_by_index(row)
        self.refresh_entries_table()

    def clear_all_entries(self):
        if not self.journal_voucher.entries:
            return
            
        if QMessageBox.question(self, "Confirm Clear", "Clear all entries?") == QMessageBox.Yes:
            self.journal_voucher.entries = []
            self.journal_voucher.update_totals()
            self.refresh_entries_table()

    def refresh_entries_table(self):
        self.entries_table.setRowCount(0)

        for row, entry in enumerate(self.journal_voucher.entries):
            self.entries_table.insertRow(row)

            account_title = self.get_account_title(entry.account_code)
            debit_amount = float(entry.debit) 
            credit_amount = float(entry.credit) 

            self.entries_table.setItem(row, 0, QTableWidgetItem(entry.account_code))
            self.entries_table.setItem(row, 1, QTableWidgetItem(account_title))
            self.entries_table.setItem(row, 2, QTableWidgetItem(f"{debit_amount:.2f}"))
            self.entries_table.setItem(row, 3, QTableWidgetItem(f"{credit_amount:.2f}"))
            self.entries_table.setItem(row, 4, QTableWidgetItem(entry.description))
            
            # Add remove button
            remove_btn = QPushButton("Remove")
            remove_btn.setObjectName("dangerButton")
            remove_btn.clicked.connect(lambda checked, r=row: self.remove_entry(r))
            self.entries_table.setCellWidget(row, 5, remove_btn)

        self.journal_voucher.update_totals()
        self.total_debit_label.setText(f"{float(self.journal_voucher.total_debit):.2f}")
        self.total_credit_label.setText(f"{float(self.journal_voucher.total_credit):.2f}")


    # def save_voucher(self):
    #     if not self.journal_voucher.entries:
    #         QMessageBox.warning(self, "Error", "Please add at least one entry!")
    #         return

    #     self.journal_voucher.date = self.date_edit.date().toPyDate()

    #     try:
    #         self.journal_voucher.validate_totals()  # This validates debits = credits
    #     except ValueError as e:
    #         QMessageBox.warning(self, "Validation Error", str(e))
    #         return

    #     # Check if this is an update or new voucher
    #     is_update = hasattr(self.journal_voucher, 'voucher_id') and self.journal_voucher.voucher_id is not None

    #     try:
    #         if is_update:
    #             # Update existing voucher
    #             # first reverse all transactions 
    #             TransactionService.reverse_transaction("JV", self.journal_voucher.voucher_id)
    #             # update the voucher in db
    #             JournalVoucherRepo.update_journal_voucher(self.journal_voucher)
    #             msg = "updated"
    #         else:
    #             # New voucher
    #             self.journal_voucher.voucher_id = JournalVoucherRepo.add_journal_voucher(self.journal_voucher)
    #             msg = "saved"

    #         # Post to ledger
    #         debits = [e for e in self.journal_voucher.entries if e.debit > 0]
    #         credits = [e for e in self.journal_voucher.entries if e.credit > 0]

    #         for d in debits:
    #             for c in credits:
    #                 TransactionService.post_transaction(
    #                     source="JV",
    #                     source_id=self.journal_voucher.voucher_id,
    #                     date=self.journal_voucher.date,
    #                     debit_account=d.account_code,
    #                     credit_account=c.account_code,
    #                     amount=min(d.debit, c.credit),  # match amounts
    #                     description=f"JV Posting: {d.description or c.description}"
    #                 )
    #                 # reduce amounts so we don't double-post
    #                 d.debit -= min(d.debit, c.credit)
    #                 c.credit -= min(d.debit, c.credit)


    #         QMessageBox.information(self, "Success", 
    #             f"Journal Voucher #{self.journal_voucher.voucher_id} {msg} successfully!\n"
    #             f"Debit: {float(self.journal_voucher.total_debit):.2f}, "
    #             f"Credit: {float(self.journal_voucher.total_credit):.2f}")

    #         self.reset_form()

    #     except Exception as e:
    #         QMessageBox.critical(self, "Error", f"Failed to save voucher: {str(e)}")

    def save_voucher(self):
        if not self.journal_voucher.entries:
            QMessageBox.warning(self, "Error", "Please add at least one entry!")
            return

        self.journal_voucher.date = self.date_edit.date().toPyDate()

        try:
            self.journal_voucher.validate_totals()
        except ValueError as e:
            QMessageBox.warning(self, "Validation Error", str(e))
            return

        is_update = hasattr(self.journal_voucher, 'voucher_id') and self.journal_voucher.voucher_id is not None

        try:
            if is_update:
                TransactionService.reverse_transaction("JV", self.journal_voucher.voucher_id)
                JournalVoucherRepo.update_journal_voucher(self.journal_voucher)
                # Log the updated journal voucher
                try:
                    log_update(
                        voucher_type="JV",
                        voucher_id=self.journal_voucher.voucher_id,
                        details=f"date={self.journal_voucher.date}, debit={float(self.journal_voucher.total_debit):.2f}, credit={float(self.journal_voucher.total_credit):.2f}"
                    )
                except Exception:
                    pass
                msg = "updated"
            else:
                self.journal_voucher.voucher_id = JournalVoucherRepo.add_journal_voucher(self.journal_voucher)
                msg = "saved"

            # SIMPLE AND CORRECT POSTING LOGIC:
            # Post each debit entry directly to corresponding credit entries
            debits = [e for e in self.journal_voucher.entries if e.debit > 0]
            credits = [e for e in self.journal_voucher.entries if e.credit > 0]
            
            # Create copies of the amounts to work with
            debit_amounts = {i: entry.debit for i, entry in enumerate(debits)}
            credit_amounts = {i: entry.credit for i, entry in enumerate(credits)}
            
            # Match debits to credits sequentially
            debit_idx = 0
            credit_idx = 0
            
            while debit_idx < len(debits) and credit_idx < len(credits):
                debit_entry = debits[debit_idx]
                credit_entry = credits[credit_idx]
                
                # Use the smaller amount between current debit and credit
                amount = min(debit_amounts[debit_idx], credit_amounts[credit_idx])
                
                if amount > 0:
                    TransactionService.post_transaction(
                        source="JV",
                        source_id=self.journal_voucher.voucher_id,
                        date=self.journal_voucher.date,
                        debit_account=debit_entry.account_code,
                        credit_account=credit_entry.account_code,
                        amount=amount,
                        description=f"JV #{self.journal_voucher.voucher_id}: {debit_entry.description or credit_entry.description or 'Journal Entry'}"
                    )
                
                # Reduce the amounts
                debit_amounts[debit_idx] -= amount
                credit_amounts[credit_idx] -= amount
                
                # Move to next entry if current is fully used
                if debit_amounts[debit_idx] == 0:
                    debit_idx += 1
                if credit_amounts[credit_idx] == 0:
                    credit_idx += 1

            QMessageBox.information(self, "Success", 
                f"Journal Voucher #{self.journal_voucher.voucher_id} {msg} successfully!\n"
                f"Debit: {float(self.journal_voucher.total_debit):.2f}, "
                f"Credit: {float(self.journal_voucher.total_credit):.2f}")

            self.reset_form()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save voucher: {str(e)}")


    def reset_form(self):
        self.journal_voucher = JournalVoucher(jv_date=self.date_edit.date().toPyDate())
        self.entries_table.setRowCount(0)
        self.voucher_no_label.setText(str(JournalVoucherRepo.get_next_voucher_no()))
        self.total_debit_label.setText("0.00")
        self.total_credit_label.setText("0.00")
        self.account_label.setText("Select Account")
        self.narration_input.clear()

    def load_voucher(self):
        voucher_id, ok = QInputDialog.getInt(self, "Load Voucher", "Enter Voucher ID:")
        if not ok:
            return

        voucher = JournalVoucherRepo.get_journal_voucher(voucher_id)
        if not voucher:
            QMessageBox.warning(self, "Error", f"Voucher #{voucher_id} not found!")
            return

        self.journal_voucher = voucher
        self.voucher_no_label.setText(str(voucher.voucher_id))
        self.date_edit.setDate(QDate(voucher.date.year, voucher.date.month, voucher.date.day))
        self.refresh_entries_table()

    def open_account_search(self):
        dialog = AccountSearchDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            acc = dialog.selected_account
            if acc:
                self.account_label.setText(f"{acc['account_code']} - {acc['title']}")

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