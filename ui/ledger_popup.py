# from PyQt5.QtWidgets import (
#     QDialog, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
#     QPushButton, QHBoxLayout, QFileDialog, QMessageBox,
#     QHeaderView, QGroupBox, QSpacerItem, QSizePolicy
# )
# from PyQt5.QtGui import  QBrush, QColor, QIcon
# from PyQt5.QtCore import Qt
# from PyQt5.QtPrintSupport import QPrinter, QPrintDialog

# from database.account_repo import AccountRepo
# from database.ledger_repo import LedgerRepo
# import csv
# from PyQt5.QtWidgets import QDateEdit
# from PyQt5.QtCore import QDate
# import os

# class LedgerPopup(QDialog):
#     def __init__(self, account_code, parent=None):
#         super().__init__(parent)   # attach to parent window
#         self.account_code = account_code
#         self.setWindowTitle(f"Ledger - {account_code}")
#         self.resize(1000, 700)
#         self.setWindowIcon(QIcon("icons/ledger_detail.png"))  # Add appropriate icon if available

#         # Apply consistent styling
#         self.setStyleSheet("""
#             QDialog {
#                 background-color: #f5f5f5;
#             }
#             QLabel {
#                 font-weight: bold;
#             }
#             QLineEdit, QComboBox, QDateEdit {
#                 padding: 5px;
#                 border: 1px solid #ccc;
#                 border-radius: 3px;
#             }
#             QPushButton {
#                 background-color: #2196F3;
#                 color: white;
#                 border: none;
#                 padding: 8px 16px;
#                 border-radius: 4px;
#                 font-weight: bold;
#             }
#             QPushButton:hover {
#                 background-color: #0b7dda;
#             }
#             QTableWidget {
#                 gridline-color: #ddd;
#                 background-color: white;
#                 alternate-background-color: #f9f9f9;
#             }
#             QHeaderView::section {
#                 background-color: #e1e1e1;
#                 padding: 8px;
#                 border: none;
#                 font-weight: bold;
#                 color : black;
#             }
#         """)

#         layout = QVBoxLayout(self)
#         layout.setSpacing(15)
#         layout.setContentsMargins(15, 15, 15, 15)

#         # --- Header with account details ---
#         self.header = QLabel()
#         self.header.setAlignment(Qt.AlignCenter)
#         self.header.setStyleSheet("""
#             background-color: #e8f4ff;
#             padding: 15px;
#             border-radius: 5px;
#             font-size: 14pt;
#             font-weight: bold;
#         """)
#         layout.addWidget(self.header)

#         # --- Date filter ---
#         date_group = QGroupBox("Date Range Filter")
#         date_group.setStyleSheet("QGroupBox { font-weight: bold; }")
#         filter_layout = QHBoxLayout()
#         date_group.setLayout(filter_layout)
        
#         filter_layout.addWidget(QLabel("From:"))
#         self.from_date = QDateEdit()
#         self.from_date.setCalendarPopup(True)
#         self.from_date.setDate(QDate.currentDate().addMonths(-1))
#         filter_layout.addWidget(self.from_date)

#         filter_layout.addWidget(QLabel("To:"))
#         self.to_date = QDateEdit()
#         self.to_date.setCalendarPopup(True)
#         self.to_date.setDate(QDate.currentDate())
#         filter_layout.addWidget(self.to_date)

#         self.filter_btn = QPushButton("Apply Filter")
#         self.filter_btn.clicked.connect(self.load_ledger_entries)
#         filter_layout.addWidget(self.filter_btn)
        
#         filter_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

#         layout.addWidget(date_group)

#         # --- Ledger table ---
#         self.table = QTableWidget()
#         self.table.setAlternatingRowColors(True)
#         layout.addWidget(self.table)

#         # --- Buttons ---
#         btn_layout = QHBoxLayout()
#         btn_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
#         export_btn = QPushButton("Export to CSV")
#         export_btn.clicked.connect(self.export_csv)
#         btn_layout.addWidget(export_btn)

#         print_btn = QPushButton("Print Ledger")
#         print_btn.clicked.connect(self.print_ledger)
#         btn_layout.addWidget(print_btn)
        
#         close_btn = QPushButton("Close")
#         close_btn.clicked.connect(self.accept)
#         btn_layout.addWidget(close_btn)

#         layout.addLayout(btn_layout)

#         # Load initial data
#         self.load_account_info()
#         self.load_ledger_entries()

#     def load_account_info(self):
#         account = AccountRepo.get_account_by_code(self.account_code)
#         if account:
#             self.header.setText(
#                 f"<h2 style='margin:0'>Ammar Trader</h2>"
#                 f"<p><b>Account Code:</b> {account.account_code} | "
#                 f"<b>Name:</b> {account.title} | "
#                 f"<b>Unit:</b> {account.unit} | "
#                 f"<b>Account Type:</b> {account.account_type}</p>"
#             )

#             # ✅ Set default from_date = account creation date
#             if hasattr(account, 'created_at') and account.created_at:
#                 self.from_date.setDate(QDate.fromString(str(account.created_at), "yyyy-MM-dd"))
#             else:
#                 self.from_date.setDate(QDate(2000, 1, 1))  # fallback if no created_at

#             # ✅ To date = today
#             self.to_date.setDate(QDate.currentDate())

#     def load_ledger_entries(self):
#         from_date = self.from_date.date().toString("yyyy-MM-dd")
#         to_date = self.to_date.date().toString("yyyy-MM-dd")

#         entries = LedgerRepo.get_ledger_by_account_code(
#             self.account_code, from_date, to_date
#         )

#         # Define the headers in required order (without Ledger ID)
#         headers = [
#             "Date", "Account Code", "Voucher Type", "Voucher ID",
#             "Description", "Debit", "Credit", "Balance"
#         ]
#         self.table.setColumnCount(len(headers))
#         self.table.setHorizontalHeaderLabels(headers)
#         self.table.setRowCount(len(entries))

#         # Apply enhanced table styling
#         self.table.setStyleSheet("""
#             QTableWidget {
#                 gridline-color: #d0d0d0;
#                 background-color: white;
#                 alternate-background-color: #f8f9fa;
#                 selection-background-color: #e3f2fd;
#             }
#             QHeaderView::section {
#                 background-color: #e9ecef;
#                 padding: 8px;
#                 border: none;
#                 font-weight: bold;
#                 font-size: 10pt;
#                 color : black;
#             }
#         """)
        
#         # Set column widths for better spacing
#         self.table.setColumnWidth(0, 90)  # Date
#         self.table.setColumnWidth(1, 90)   # Account Code
#         self.table.setColumnWidth(2, 80)  # Voucher Type
#         self.table.setColumnWidth(3, 70)  # Voucher ID
#         self.table.setColumnWidth(4, 310)  # Description
#         self.table.setColumnWidth(5, 100)  # Debit
#         self.table.setColumnWidth(6, 100)  # Credit
#         self.table.setColumnWidth(7, 120)  # Balance
        
#         # Enable alternating row colors
#         self.table.setAlternatingRowColors(True)
        
#         # Set row height for better spacing
#         for row in range(len(entries)):
#             self.table.setRowHeight(row, 30)

#         for row, entry in enumerate(entries):
#             # --- Fix for date ---
#             date_val = entry.get("date", "")
#             if hasattr(date_val, "strftime"):   # datetime/date object
#                 date_str = date_val.strftime("%d-%m-%Y")
#             else:
#                 date_str = str(date_val or "")

#             # Date
#             date_item = QTableWidgetItem(date_str)
#             date_item.setTextAlignment(Qt.AlignCenter)
#             self.table.setItem(row, 0, date_item)

#             # Account Code
#             account_code_item = QTableWidgetItem(str(entry.get("account_code", "")))
#             account_code_item.setTextAlignment(Qt.AlignCenter)
#             self.table.setItem(row, 1, account_code_item)

#             # Voucher Type
#             voucher_type_item = QTableWidgetItem(str(entry.get("voucher_type", "")))
#             voucher_type_item.setTextAlignment(Qt.AlignCenter)
#             self.table.setItem(row, 2, voucher_type_item)

#             # Voucher ID
#             voucher_id_item = QTableWidgetItem(str(entry.get("voucher_id", "")))
#             voucher_id_item.setTextAlignment(Qt.AlignCenter)
#             self.table.setItem(row, 3, voucher_id_item)

#             # Description
#             desc_item = QTableWidgetItem(str(entry.get("description", "")))
#             self.table.setItem(row, 4, desc_item)

#             # Debit - right aligned with formatting
#             debit = float(entry.get("debit", 0))
#             debit_item = QTableWidgetItem(f"{debit:,.2f}")
#             debit_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            
#             if debit > 0:
#                 debit_item.setForeground(QBrush(QColor(0, 128, 0)))  # Green for debit
#             self.table.setItem(row, 5, debit_item)

#             # Credit - right aligned with formatting
#             credit = float(entry.get("credit", 0))
#             credit_item = QTableWidgetItem(f"{credit:,.2f}")
#             credit_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            
#             if credit > 0:
#                 credit_item.setForeground(QBrush(QColor(255, 0, 0)))  # Red for credit
#             self.table.setItem(row, 6, credit_item)

#             # Balance - right aligned with formatting
#             balance = float(entry.get("balance", 0))
#             balance_item = QTableWidgetItem(f"{balance:,.2f}")
#             balance_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            
#             if balance < 0:
#                 balance_item.setForeground(QBrush(QColor(255, 0, 0)))  # Red for negative
#             elif balance > 0:
#                 balance_item.setForeground(QBrush(QColor(0, 128, 0)))  # Green for positive
#             else:
#                 balance_item.setForeground(QBrush(QColor(0, 0, 0)))  # Black for zero
                
#             self.table.setItem(row, 7, balance_item)

#         # Make description column expand to fill space
#         self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        
#         # Sort by date initially
#         self.table.setSortingEnabled(True)
#         self.table.sortByColumn(0, Qt.AscendingOrder)

#     def export_csv(self):
#         """Export the ledger entries to a CSV file"""
#         default_name = f"ledger_{self.account_code}_{QDate.currentDate().toString('yyyyMMdd')}.csv"
#         path, _ = QFileDialog.getSaveFileName(
#             self, "Save Ledger", default_name, "CSV Files (*.csv)"
#         )
        
#         if path:
#             try:
#                 with open(path, mode="w", newline="", encoding="utf-8") as file:
#                     writer = csv.writer(file)
                    
#                     # Write headers
#                     headers = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
#                     writer.writerow(headers)

#                     # Write rows
#                     for row in range(self.table.rowCount()):
#                         row_data = []
#                         for col in range(self.table.columnCount()):
#                             item = self.table.item(row, col)
#                             row_data.append(item.text() if item else "")
#                         writer.writerow(row_data)
                        
#                 QMessageBox.information(self, "Success", f"Ledger exported successfully to:\n{os.path.basename(path)}")
#             except Exception as e:
#                 QMessageBox.critical(self, "Error", f"Failed to export CSV: {str(e)}")

#     def print_ledger(self):
#         """Send the ledger to printer (or PDF if user chooses)"""
#         try:
#             printer = QPrinter(QPrinter.HighResolution)
#             printer.setPageSize(QPrinter.A4)
#             printer.setOrientation(QPrinter.Landscape)
            
#             dialog = QPrintDialog(printer, self)
#             dialog.setWindowTitle("Print Ledger")
            
#             if dialog.exec_() == QPrintDialog.Accepted:
#                 # TODO: Implement proper printing with formatting
#                 QMessageBox.information(self, "Print", "Ledger sent to printer successfully.")
#         except Exception as e:
#             QMessageBox.critical(self, "Error", f"Failed to print: {str(e)}")










from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QFileDialog, QMessageBox,
    QHeaderView, QGroupBox, QSpacerItem, QSizePolicy, QComboBox
)
from PyQt5.QtGui import QBrush, QColor, QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog

from database.account_repo import AccountRepo
from database.ledger_repo import LedgerRepo
import csv
from PyQt5.QtWidgets import QDateEdit
from PyQt5.QtCore import QDate
import os

class LedgerPopup(QDialog):
    def __init__(self, account_code, parent=None):
        super().__init__(parent)
        self.account_code = account_code
        self.current_page = 1
        self.rows_per_page = 100
        self.all_entries = []
        
        self.setWindowTitle(f"Ledger - {account_code}")
        self.resize(1000, 700)
        self.setWindowIcon(QIcon("icons/ledger_detail.png"))

        # Apply consistent styling
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
            QLabel {
                font-weight: bold;
            }
            QLineEdit, QComboBox, QDateEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 3px;
            }
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
            QTableWidget {
                gridline-color: #ddd;
                background-color: white;
                alternate-background-color: #f9f9f9;
            }
            QHeaderView::section {
                background-color: #e1e1e1;
                padding: 8px;
                border: none;
                font-weight: bold;
                color : black;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)

        # --- Header with account details ---
        self.header = QLabel()
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setStyleSheet("""
            background-color: #e8f4ff;
            padding: 15px;
            border-radius: 5px;
            font-size: 14pt;
            font-weight: bold;
        """)
        layout.addWidget(self.header)

        # --- Date filter ---
        date_group = QGroupBox("Date Range Filter")
        date_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        filter_layout = QHBoxLayout()
        date_group.setLayout(filter_layout)
        
        filter_layout.addWidget(QLabel("From:"))
        self.from_date = QDateEdit()
        self.from_date.setCalendarPopup(True)
        self.from_date.setDate(QDate.currentDate().addMonths(-1))
        filter_layout.addWidget(self.from_date)

        filter_layout.addWidget(QLabel("To:"))
        self.to_date = QDateEdit()
        self.to_date.setCalendarPopup(True)
        self.to_date.setDate(QDate.currentDate())
        filter_layout.addWidget(self.to_date)

        self.filter_btn = QPushButton("Apply Filter")
        self.filter_btn.clicked.connect(self.load_ledger_entries)
        filter_layout.addWidget(self.filter_btn)
        
        filter_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        layout.addWidget(date_group)

        # --- Pagination Controls ---
        pagination_layout = QHBoxLayout()
        
        self.first_btn = QPushButton("First")
        self.first_btn.clicked.connect(self.go_to_first_page)
        self.first_btn.setEnabled(False)
        pagination_layout.addWidget(self.first_btn)
        
        self.prev_btn = QPushButton("◀ Previous")
        self.prev_btn.clicked.connect(self.previous_page)
        self.prev_btn.setEnabled(False)
        pagination_layout.addWidget(self.prev_btn)
        
        self.page_label = QLabel("Page 1 of 1")
        self.page_label.setAlignment(Qt.AlignCenter)
        self.page_label.setStyleSheet("font-weight: bold; padding: 5px;")
        pagination_layout.addWidget(self.page_label)
        
        self.next_btn = QPushButton("Next ▶")
        self.next_btn.clicked.connect(self.next_page)
        self.next_btn.setEnabled(False)
        pagination_layout.addWidget(self.next_btn)
        
        self.last_btn = QPushButton("Last")
        self.last_btn.clicked.connect(self.go_to_last_page)
        self.last_btn.setEnabled(False)
        pagination_layout.addWidget(self.last_btn)
        
        pagination_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        # Rows per page selector
        pagination_layout.addWidget(QLabel("Rows per page:"))
        self.rows_combo = QComboBox()
        self.rows_combo.addItems(["50", "100", "200", "500"])
        self.rows_combo.setCurrentText("100")
        self.rows_combo.currentTextChanged.connect(self.change_rows_per_page)
        pagination_layout.addWidget(self.rows_combo)

        layout.addLayout(pagination_layout)

        # --- Ledger table ---
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)

        # --- Buttons ---
        btn_layout = QHBoxLayout()
        btn_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        export_btn = QPushButton("Export to CSV")
        export_btn.clicked.connect(self.export_csv)
        btn_layout.addWidget(export_btn)

        print_btn = QPushButton("Print Ledger")
        print_btn.clicked.connect(self.print_ledger)
        btn_layout.addWidget(print_btn)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)

        layout.addLayout(btn_layout)

        # Load initial data
        self.load_account_info()
        self.load_ledger_entries()

    def load_account_info(self):
        account = AccountRepo.get_account_by_code(self.account_code)
        if account:
            self.header.setText(
                f"<h2 style='margin:0'>Bismillah Installment Corporation</h2>"
                f"<p><b>Account Code:</b> {account.account_code} | "
                f"<b>Name:</b> {account.title} | "
                f"<b>Unit:</b> {account.unit} | "
                f"<b>Account Type:</b> {account.account_type}</p>"
            )

            if hasattr(account, 'created_at') and account.created_at:
                self.from_date.setDate(QDate.fromString(str(account.created_at), "yyyy-MM-dd"))
            else:
                self.from_date.setDate(QDate(2000, 1, 1))

            self.to_date.setDate(QDate.currentDate())

    def load_ledger_entries(self):
        from_date = self.from_date.date().toString("yyyy-MM-dd")
        to_date = self.to_date.date().toString("yyyy-MM-dd")

        # Load ALL entries from database
        self.all_entries = LedgerRepo.get_ledger_by_account_code(
            self.account_code, from_date, to_date
        )
        
        # ✅ CHANGE: Calculate and set to last page instead of first page
        total_pages = max(1, (len(self.all_entries) + self.rows_per_page - 1) // self.rows_per_page)
        self.current_page = total_pages  # Set to last page by default
        
        self.display_current_page()

    def display_current_page(self):
        if not self.all_entries:
            self.table.setRowCount(0)
            self.page_label.setText("No records found")
            self.update_pagination_controls()
            return
        
        # Calculate page indices
        start_idx = (self.current_page - 1) * self.rows_per_page
        end_idx = start_idx + self.rows_per_page
        current_entries = self.all_entries[start_idx:end_idx]
        
        # Define headers
        headers = [
            "Date", "Account Code", "Voucher Type", "Voucher ID",
            "Description", "Debit", "Credit", "Balance"
        ]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(current_entries))

        # Apply enhanced table styling
        self.table.setStyleSheet("""
            QTableWidget {
                gridline-color: #d0d0d0;
                background-color: white;
                alternate-background-color: #f8f9fa;
                selection-background-color: #e3f2fd;
            }
            QHeaderView::section {
                background-color: #e9ecef;
                padding: 8px;
                border: none;
                font-weight: bold;
                font-size: 10pt;
                color : black;
            }
        """)
        
        # Set column widths for better spacing
        self.table.setColumnWidth(0, 90)   # Date
        self.table.setColumnWidth(1, 90)   # Account Code
        self.table.setColumnWidth(2, 80)   # Voucher Type
        self.table.setColumnWidth(3, 70)   # Voucher ID
        self.table.setColumnWidth(4, 310)  # Description
        self.table.setColumnWidth(5, 100)  # Debit
        self.table.setColumnWidth(6, 100)  # Credit
        self.table.setColumnWidth(7, 120)  # Balance
        
        # Enable alternating row colors
        self.table.setAlternatingRowColors(True)
        
        # Set row height for better spacing
        for row in range(len(current_entries)):
            self.table.setRowHeight(row, 30)

        # Populate table with current page data
        for row, entry in enumerate(current_entries):
            # Date
            date_val = entry.get("date", "")
            if hasattr(date_val, "strftime"):
                date_str = date_val.strftime("%d-%m-%Y")
            else:
                date_str = str(date_val or "")

            date_item = QTableWidgetItem(date_str)
            date_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 0, date_item)

            # Account Code
            account_code_item = QTableWidgetItem(str(entry.get("account_code", "")))
            account_code_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 1, account_code_item)

            # Voucher Type
            voucher_type_item = QTableWidgetItem(str(entry.get("voucher_type", "")))
            voucher_type_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 2, voucher_type_item)

            # Voucher ID
            voucher_id_item = QTableWidgetItem(str(entry.get("voucher_id", "")))
            voucher_id_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 3, voucher_id_item)

            # Description
            desc_item = QTableWidgetItem(str(entry.get("description", "")))
            self.table.setItem(row, 4, desc_item)

            # Debit - right aligned with formatting
            debit = float(entry.get("debit", 0))
            debit_item = QTableWidgetItem(f"{debit:,.2f}")
            debit_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            
            if debit > 0:
                debit_item.setForeground(QBrush(QColor(0, 128, 0)))  # Green for debit
            self.table.setItem(row, 5, debit_item)

            # Credit - right aligned with formatting
            credit = float(entry.get("credit", 0))
            credit_item = QTableWidgetItem(f"{credit:,.2f}")
            credit_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            
            if credit > 0:
                credit_item.setForeground(QBrush(QColor(255, 0, 0)))  # Red for credit
            self.table.setItem(row, 6, credit_item)

            # Balance - right aligned with formatting
            balance = float(entry.get("balance", 0))
            balance_item = QTableWidgetItem(f"{balance:,.2f}")
            balance_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            
            if balance < 0:
                balance_item.setForeground(QBrush(QColor(255, 0, 0)))  # Red for negative
            elif balance > 0:
                balance_item.setForeground(QBrush(QColor(0, 128, 0)))  # Green for positive
            else:
                balance_item.setForeground(QBrush(QColor(0, 0, 0)))  # Black for zero
                
            self.table.setItem(row, 7, balance_item)

        # Make description column expand to fill space
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        
        # Enable sorting
        self.table.setSortingEnabled(True)
        
        # Update pagination controls
        self.update_pagination_controls()

    def update_pagination_controls(self):
        total_records = len(self.all_entries)
        if total_records == 0:
            self.page_label.setText("No records found")
            self.prev_btn.setEnabled(False)
            self.next_btn.setEnabled(False)
            self.first_btn.setEnabled(False)
            self.last_btn.setEnabled(False)
            return
            
        total_pages = max(1, (total_records + self.rows_per_page - 1) // self.rows_per_page)
        
        # Update page label
        start_record = (self.current_page - 1) * self.rows_per_page + 1
        end_record = min(self.current_page * self.rows_per_page, total_records)
        self.page_label.setText(f"Page {self.current_page} of {total_pages} (Records {start_record:,} - {end_record:,} of {total_records:,})")
        
        # Update button states
        self.prev_btn.setEnabled(self.current_page > 1)
        self.next_btn.setEnabled(self.current_page < total_pages)
        self.first_btn.setEnabled(self.current_page > 1)
        self.last_btn.setEnabled(self.current_page < total_pages)

    def change_rows_per_page(self):
        """Change the number of rows displayed per page"""
        self.rows_per_page = int(self.rows_combo.currentText())
        # Stay on approximately the same records when changing page size
        if self.all_entries:
            current_record = (self.current_page - 1) * self.rows_per_page
            self.current_page = (current_record // self.rows_per_page) + 1
        else:
            self.current_page = 1
        self.display_current_page()

    def go_to_first_page(self):
        """Go to first page"""
        if self.all_entries and self.current_page != 1:
            self.current_page = 1
            self.display_current_page()

    def go_to_last_page(self):
        """Go to last page"""
        if self.all_entries:
            total_pages = (len(self.all_entries) + self.rows_per_page - 1) // self.rows_per_page
            if self.current_page != total_pages:
                self.current_page = total_pages
                self.display_current_page()

    def next_page(self):
        """Go to next page"""
        total_pages = (len(self.all_entries) + self.rows_per_page - 1) // self.rows_per_page
        if self.current_page < total_pages:
            self.current_page += 1
            self.display_current_page()

    def previous_page(self):
        """Go to previous page"""
        if self.current_page > 1:
            self.current_page -= 1
            self.display_current_page()

    def export_csv(self):
        """Export ALL ledger entries to a CSV file (not just current page)"""
        if not self.all_entries:
            QMessageBox.warning(self, "No Data", "No ledger entries to export.")
            return
            
        default_name = f"ledger_{self.account_code}_{QDate.currentDate().toString('yyyyMMdd')}.csv"
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Ledger", default_name, "CSV Files (*.csv)"
        )
        
        if path:
            try:
                account = AccountRepo.get_account_by_code(self.account_code)
                
                with open(path, mode="w", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    
                    # Header rows
                    writer.writerow(["Bismillah Installment Corporation"])
                    if account:
                        writer.writerow([
                            f"Account Code: {account.account_code}",
                            f"Name: {account.title}",
                            f"Unit: {account.unit}",
                            f"Account Type: {account.account_type}"
                        ])
                    writer.writerow([
                        f"Period: {self.from_date.date().toString('dd-MM-yyyy')} to {self.to_date.date().toString('dd-MM-yyyy')}"
                    ])
                    writer.writerow([f"Generated: {QDate.currentDate().toString('dd-MM-yyyy')}"])
                    writer.writerow([f"Total Records: {len(self.all_entries):,}"])
                    writer.writerow([])

                    # Write column headers
                    headers = ["Date", "Account Code", "Voucher Type", "Voucher ID", 
                              "Description", "Debit", "Credit", "Balance"]
                    writer.writerow(headers)

                    # Write ALL rows (not just current page)
                    for entry in self.all_entries:
                        date_val = entry.get("date", "")
                        if hasattr(date_val, "strftime"):
                            date_str = date_val.strftime("%d-%m-%Y")
                        else:
                            date_str = str(date_val or "")

                        row_data = [
                            date_str,
                            entry.get("account_code", ""),
                            entry.get("voucher_type", ""),
                            entry.get("voucher_id", ""),
                            entry.get("description", ""),
                            f"{float(entry.get('debit', 0)):,.2f}",
                            f"{float(entry.get('credit', 0)):,.2f}",
                            f"{float(entry.get('balance', 0)):,.2f}"
                        ]
                        writer.writerow(row_data)
                        
                QMessageBox.information(self, "Success", 
                    f"Ledger exported successfully!\n"
                    f"Total records: {len(self.all_entries):,}\n"
                    f"File: {os.path.basename(path)}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export CSV: {str(e)}")

    def print_ledger(self):
        """Send the ledger to printer (or PDF if user chooses)"""
        if not self.all_entries:
            QMessageBox.warning(self, "No Data", "No ledger entries to print.")
            return
            
        try:
            printer = QPrinter(QPrinter.HighResolution)
            printer.setPageSize(QPrinter.A4)
            printer.setOrientation(QPrinter.Landscape)
            
            dialog = QPrintDialog(printer, self)
            dialog.setWindowTitle("Print Ledger")
            
            if dialog.exec_() == QPrintDialog.Accepted:
                # Actually render the content to the printer
                self._render_ledger_to_printer(printer)
                QMessageBox.information(self, "Print", 
                    f"Ledger sent to printer successfully.\n"
                    f"Printing {len(self.all_entries):,} records.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to print: {str(e)}")


    def _render_ledger_to_printer(self, printer):
        """Render the ledger data to printer/PDF"""
        from PyQt5.QtGui import QTextDocument, QTextCursor, QTextTableFormat
        from PyQt5.QtGui import QTextCharFormat, QFont, QTextBlockFormat
        from PyQt5.QtCore import Qt
        
        doc = QTextDocument()
        cursor = QTextCursor(doc)
        
        # === BEAUTIFIED HEADER ===
        
        # Company Name
        company_fmt = QTextCharFormat()
        company_fmt.setFont(QFont("Arial", 16, QFont.Bold))
        company_fmt.setForeground(QColor(0, 51, 102))  # Dark blue
        
        block_fmt = QTextBlockFormat()
        block_fmt.setAlignment(Qt.AlignCenter)
        cursor.setBlockFormat(block_fmt)
        cursor.insertText("BISMILLAH INSTALLMENT CORPORATION\n", company_fmt)
        
        # Tagline/Subtitle
        tagline_fmt = QTextCharFormat()
        tagline_fmt.setFont(QFont("Arial", 9, QFont.StyleItalic))
        tagline_fmt.setForeground(QColor(100, 100, 100))
        cursor.insertText("Financial Management System\n", tagline_fmt)
        
        # Divider line
        cursor.insertText("━" * 80 + "\n")
        
        # Report Title
        title_fmt = QTextCharFormat()
        title_fmt.setFont(QFont("Arial", 13, QFont.Bold))
        title_fmt.setForeground(QColor(0, 51, 102))
        cursor.insertText("LEDGER REPORT\n\n", title_fmt)
        
        # Account Details Section - Left align
        account = AccountRepo.get_account_by_code(self.account_code)
        
        details_fmt = QTextCharFormat()
        details_fmt.setFont(QFont("Arial", 10))
        
        block_fmt_left = QTextBlockFormat()
        block_fmt_left.setAlignment(Qt.AlignLeft)
        cursor.setBlockFormat(block_fmt_left)
        
        if account:
            cursor.insertText(f"Account Code: {account.account_code} | ", details_fmt)
            cursor.insertText(f"Name: {account.title}\n", details_fmt)
            cursor.insertText(f"Unit: {account.unit} | ", details_fmt)
            cursor.insertText(f"Type: {account.account_type}\n\n", details_fmt)
        
        # Date Range and Print Info
        info_fmt = QTextCharFormat()
        info_fmt.setFont(QFont("Arial", 9))
        info_fmt.setForeground(QColor(80, 80, 80))
        
        cursor.insertText(f"Period: {self.from_date.date().toString('dd-MM-yyyy')} to {self.to_date.date().toString('dd-MM-yyyy')} | ", info_fmt)
        cursor.insertText(f"Generated: {QDate.currentDate().toString('dd-MM-yyyy')} | ", info_fmt)
        cursor.insertText(f"Total Records: {len(self.all_entries):,}\n", info_fmt)
        
        cursor.insertText("━" * 80 + "\n\n", info_fmt)
        
        # === TABLE ===
        
        # Create table with headers
        table_format = QTextTableFormat()
        table_format.setCellPadding(6)
        table_format.setCellSpacing(0)
        table_format.setBorder(1)
        
        # +1 for header row
        table = cursor.insertTable(len(self.all_entries) + 1, 8, table_format)
        
        # Add column headers with background color
        headers = ["Date", "Account Code", "Voucher Type", "Voucher ID", "Description", "Debit", "Credit", "Balance"]
        header_fmt = QTextCharFormat()
        header_fmt.setFont(QFont("Arial", 10, QFont.Bold))
        
        for col, header in enumerate(headers):
            cell = table.cellAt(0, col)
            cell_cursor = cell.firstCursorPosition()
            cell_cursor.insertText(header, header_fmt)
        
        # Add data rows
        data_fmt = QTextCharFormat()
        data_fmt.setFont(QFont("Arial", 9))
        
        for row, entry in enumerate(self.all_entries, start=1):
            date_val = entry.get("date", "")
            if hasattr(date_val, "strftime"):
                date_str = date_val.strftime("%d-%m-%Y")
            else:
                date_str = str(date_val or "")
            
            row_data = [
                date_str,
                str(entry.get("account_code", "")),
                str(entry.get("voucher_type", "")),
                str(entry.get("voucher_id", "")),
                str(entry.get("description", "")),
                f"{float(entry.get('debit', 0)):,.2f}",
                f"{float(entry.get('credit', 0)):,.2f}",
                f"{float(entry.get('balance', 0)):,.2f}"
            ]
            
            for col, data in enumerate(row_data):
                cell = table.cellAt(row, col)
                cell_cursor = cell.firstCursorPosition()
                
                # Right align numeric columns
                if col in [5, 6, 7]:  # Debit, Credit, Balance
                    cell_block_fmt = QTextBlockFormat()
                    cell_block_fmt.setAlignment(Qt.AlignRight)
                    cell_cursor.setBlockFormat(cell_block_fmt)
                
                cell_cursor.insertText(data, data_fmt)
        
        # Print the document
        doc.print(printer)