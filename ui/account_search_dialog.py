
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QComboBox, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView
)
from PyQt5.QtCore import Qt
from database.account_repo import AccountRepo


class AccountSearchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🔍 Search Accounts")
        self.resize(900, 400)

        layout = QVBoxLayout(self)

        # --- Filter Section ---
        filter_layout = QHBoxLayout()

        # Filter by Code
        filter_layout.addWidget(QLabel("Code:"))
        self.code_filter = QLineEdit()
        filter_layout.addWidget(self.code_filter)

        # Filter by Title
        filter_layout.addWidget(QLabel("Title:"))
        self.title_filter = QLineEdit()
        filter_layout.addWidget(self.title_filter)

        # Filter by cell
        filter_layout.addWidget(QLabel("cell:"))
        self.cell_filter = QLineEdit()
        filter_layout.addWidget(self.cell_filter)

        # Filter by unit
        filter_layout.addWidget(QLabel("Unit:"))
        self.unit_filter = QLineEdit()
        filter_layout.addWidget(self.unit_filter)

        # # Filter by Type
        # filter_layout.addWidget(QLabel("Type:"))
        # self.type_filter = QComboBox()
        # self.type_filter.addItem("All")
        # self.type_filter.addItems(["CUSTOMER", "SUPPLIER", "SYSTEM"])
        # filter_layout.addWidget(self.type_filter)

        # # Filter by Status
        # filter_layout.addWidget(QLabel("Status:"))
        # self.status_filter = QComboBox()
        # self.status_filter.addItem("All")
        # self.status_filter.addItems(["ACTIVE", "INACTIVE"])
        # filter_layout.addWidget(self.status_filter)

        layout.addLayout(filter_layout)

        # --- Results Table ---
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["Code", "Title", "cell",  "Unit"]
        )
        # self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setColumnWidth(0, 100)  # Code
        self.table.setColumnWidth(1, 400)  # Title
        self.table.setColumnWidth(2, 150)  # Cell
        self.table.setColumnWidth(3, 150)  # Unit
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        # --- Select Button ---
        self.select_btn = QPushButton("Select")
        layout.addWidget(self.select_btn)

        # Vars
        self.selected_account = None

        # Signals for live filtering
        self.code_filter.textChanged.connect(self.apply_filters)
        self.title_filter.textChanged.connect(self.apply_filters)
        self.cell_filter.textChanged.connect(self.apply_filters)
        self.unit_filter.textChanged.connect(self.apply_filters)
        # self.type_filter.currentIndexChanged.connect(self.apply_filters)
        # self.status_filter.currentIndexChanged.connect(self.apply_filters)

        # Connect select button
        self.select_btn.clicked.connect(self.get_selected_account)
        # Connect double click on table to select account
        self.table.cellDoubleClicked.connect(self.get_selected_account)

        self.setFocusPolicy(Qt.StrongFocus)
        # Load all initially
        self.apply_filters()

    def apply_filters(self):
        """Apply filters and reload table live"""
        code = self.code_filter.text().strip().lower()
        title = self.title_filter.text().strip().lower()
        cell = self.cell_filter.text().strip().lower()
        unit = self.unit_filter.text().strip().lower()
        # acc_type = self.type_filter.currentText()
        # status = self.status_filter.currentText()

        accounts = AccountRepo.list_accounts()
        filtered = []

        for acc in accounts:
            # Filter by code
            if code and code not in acc.account_code.lower():
                continue
            # Filter by title
            if title and title not in acc.title.lower():
                continue
            # Filter by cell
            if cell and cell not in (acc.cell or "").lower():
                continue
            # Filter by unit
            if unit and unit not in (acc.unit or "").lower():
                continue
            # # Filter by type
            # if acc_type != "All" and acc.account_type != acc_type:
            #     continue
            # Filter by status
            # if status != "All" and acc.status != status:
            #     continue

            filtered.append(acc)

        # Populate table
        self.table.setRowCount(0)
        for row_idx, acc in enumerate(filtered):
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(acc.account_code))
            self.table.setItem(row_idx, 1, QTableWidgetItem(acc.title))
            self.table.setItem(row_idx, 2, QTableWidgetItem(acc.cell or ""))
            # self.table.setItem(row_idx, 3, QTableWidgetItem(acc.account_type or ""))
            self.table.setItem(row_idx, 3, QTableWidgetItem(acc.unit or ""))
            # self.table.setItem(row_idx, 4, QTableWidgetItem(acc.status))




    def get_selected_account(self, *args):
        """Store selected account and close. Can be called from button or double click"""
        row = self.table.currentRow()
        if row >= 0:
            self.selected_account = {
                "account_code": self.table.item(row, 0).text(),
                "title": self.table.item(row, 1).text(),
                "cell": self.table.item(row, 2).text(),
                # "type": self.table.item(row, 3).text(),
                "unit": self.table.item(row, 3).text(),
                # "status": self.table.item(row, 4).text(),
            }
            self.accept()


    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Down:
            # Check if focus is on any input field
            focused = self.focusWidget()
            if focused in [self.code_filter, self.title_filter, self.cell_filter, self.unit_filter]:
                if self.table.rowCount() > 0:
                    self.table.setFocus()
                    self.table.selectRow(0)
                    return
        super().keyPressEvent(event)