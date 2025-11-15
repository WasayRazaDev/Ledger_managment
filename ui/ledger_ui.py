from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QComboBox, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QGroupBox, QSpacerItem, QSizePolicy, QApplication, QShortcut, QAction, QMenu, QAbstractItemView
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QIcon, QKeySequence

from database.account_repo import AccountRepo
from ui.ledger_popup import LedgerPopup  # your popup window


class LedgerUI(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🔍 Search Accounts")
        self.resize(900, 500)
        self.setWindowIcon(QIcon("icons/search.png"))  # Add appropriate icon if available

        # Apply consistent styling
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
            QLabel {
                font-weight: bold;
                color: #2c3e50;
            }
            QLineEdit, QComboBox {
                padding: 6px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                background-color: white;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #3498db;
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
            QTableWidget {
                gridline-color: black;
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
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)

        # Title
        title_label = QLabel("Account Search - Double click to view ledger")
        title_label.setStyleSheet("""
            font-size: 14pt;
            font-weight: bold;
            color: #2c3e50;
            padding: 10px;
            background-color: #e9ecef;
            border-radius: 6px;
        """)
        layout.addWidget(title_label)

        # --- Filter Section ---
        filter_group = QGroupBox("Filter Criteria")
        filter_layout = QHBoxLayout()
        filter_group.setLayout(filter_layout)

        # Filter by Code
        filter_layout.addWidget(QLabel("Code:"))
        self.code_filter = QLineEdit()
        self.code_filter.setPlaceholderText("Filter by code")
        filter_layout.addWidget(self.code_filter)

        # Filter by Title
        filter_layout.addWidget(QLabel("Title:"))
        self.title_filter = QLineEdit()
        self.title_filter.setPlaceholderText("Filter by title")
        filter_layout.addWidget(self.title_filter)

        # Filter by cell
        filter_layout.addWidget(QLabel("Cell:"))
        self.cell_filter = QLineEdit()
        self.cell_filter.setPlaceholderText("Filter by cell")
        filter_layout.addWidget(self.cell_filter)

        # Filter by unit
        filter_layout.addWidget(QLabel("Unit:"))
        self.unit_filter = QLineEdit()
        self.unit_filter.setPlaceholderText("Filter by unit")
        filter_layout.addWidget(self.unit_filter)

        # # Filter by Type
        # filter_layout.addWidget(QLabel("Type:"))
        # self.type_filter = QComboBox()
        # self.type_filter.addItem("All")
        # self.type_filter.addItems(["CUSTOMER", "SUPPLIER", "SYSTEM"])
        # filter_layout.addWidget(self.type_filter)

        # Filter by Status
        filter_layout.addWidget(QLabel("Status:"))
        self.status_filter = QComboBox()
        self.status_filter.addItem("All")
        self.status_filter.addItems(["ACTIVE", "INACTIVE"])
        filter_layout.addWidget(self.status_filter)

        layout.addWidget(filter_group)

        # --- Results Table ---
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Code", "Title", "Cell", "Unit", "Status"]
        )
        # self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectItems)
        self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        self.table.setColumnWidth(0, 90)  # Code
        self.table.setColumnWidth(1, 350)  # Title
        self.table.setColumnWidth(2, 120)  # Cell
        self.table.setColumnWidth(3, 110)  # Unit
        self.table.setColumnWidth(4, 90)  #status

        self.copy_shortcut = QShortcut(QKeySequence.Copy, self.table)
        self.copy_shortcut.activated.connect(self.copy_selected_cells)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_table_context_menu)

        layout.addWidget(self.table)

        # --- Select Button ---
        button_layout = QHBoxLayout()
        button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        self.select_btn = QPushButton("View Ledger")
        self.select_btn.setObjectName("actionButton")
        button_layout.addWidget(self.select_btn)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)

        layout.addLayout(button_layout)

        # Vars
        self.selected_account = None

        # Signals for live filtering
        self.code_filter.textChanged.connect(self.apply_filters)
        self.title_filter.textChanged.connect(self.apply_filters)
        self.cell_filter.textChanged.connect(self.apply_filters)
        self.unit_filter.textChanged.connect(self.apply_filters)
        # self.type_filter.currentIndexChanged.connect(self.apply_filters)
        self.status_filter.currentIndexChanged.connect(self.apply_filters)

        # Connect select button
        self.select_btn.clicked.connect(self.open_ledger_from_button)
        # Connect double click on table to select account
        self.table.cellDoubleClicked.connect(self.open_ledger)
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
        status = self.status_filter.currentText()

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
            if status != "All" and acc.status != status:
                continue

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
            
            # Color status based on value
            status_item = QTableWidgetItem(acc.status)
            if acc.status == "ACTIVE":
                status_item.setForeground(QBrush(QColor(0, 128, 0)))  # Green for active
            else:
                status_item.setForeground(QBrush(QColor(255, 0, 0)))  # Red for inactive
            self.table.setItem(row_idx, 4, status_item)

    def copy_selected_cells(self):
        ranges = self.table.selectedRanges()
        if not ranges:
            return
        blocks = []
        for r in ranges:
            rows = []
            for i in range(r.topRow(), r.bottomRow() + 1):
                cols = []
                for j in range(r.leftColumn(), r.rightColumn() + 1):
                    item = self.table.item(i, j)
                    cols.append(item.text() if item else "")
                rows.append("\t".join(cols))
            blocks.append("\n".join(rows))
        QApplication.clipboard().setText("\n".join(blocks))

    def show_table_context_menu(self, pos):
        menu = QMenu(self)
        copy_action = QAction("Copy", self)
        copy_action.setShortcut(QKeySequence.Copy)
        copy_action.triggered.connect(self.copy_selected_cells)
        menu.addAction(copy_action)
        menu.exec_(self.table.viewport().mapToGlobal(pos))

    def open_ledger(self, row, col):
        """Open LedgerPopup when an account is double-clicked"""
        account_code = self.table.item(row, 0).text()
        popup = LedgerPopup(account_code, self)
        popup.exec_()

    def open_ledger_from_button(self):
        """Open LedgerPopup when the view ledger button is clicked"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            account_code = self.table.item(current_row, 0).text()
            popup = LedgerPopup(account_code, self)
            popup.exec_()
        else:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Selection Required", "Please select an account first.")


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