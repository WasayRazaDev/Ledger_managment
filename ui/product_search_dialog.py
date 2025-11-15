    
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QLineEdit, QComboBox,
                             QLabel, QHeaderView)
from PyQt5.QtCore import Qt
from database.product_repo import ProductRepo

class ProductSearchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🔍 Search Products")
        self.resize(800, 400)  # Wider to accommodate company column

        layout = QVBoxLayout(self)

        # --- Filter Section ---
        filter_layout = QHBoxLayout()

        # Filter by Name
        filter_layout.addWidget(QLabel("Name:"))
        self.name_filter = QLineEdit()
        self.name_filter.setPlaceholderText("Enter product name")
        filter_layout.addWidget(self.name_filter)

        
        # Filter by Company
        filter_layout.addWidget(QLabel("Company:"))
        self.company_filter = QLineEdit()
        self.company_filter.setPlaceholderText("Enter company name")
        filter_layout.addWidget(self.company_filter)

        
        # Filter by Product ID
        filter_layout.addWidget(QLabel("Product ID:"))
        self.id_filter = QLineEdit()
        self.id_filter.setPlaceholderText("Enter product ID")
        filter_layout.addWidget(self.id_filter)

        # Filter by Status
        filter_layout.addWidget(QLabel("Status:"))
        self.status_filter = QComboBox()
        self.status_filter.addItem("All")
        self.status_filter.addItems(["active", "inactive"])
        filter_layout.addWidget(self.status_filter)

        layout.addLayout(filter_layout)

        # --- Results Table ---
        self.table = QTableWidget()
        self.table.setColumnCount(4)  # Changed to 4 columns
        self.table.setHorizontalHeaderLabels(["Product ID", "Company", "Name", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        
        # Connect double-click signal
        self.table.cellDoubleClicked.connect(self.on_double_click)
        
        layout.addWidget(self.table)

        # --- Select Button ---
        self.select_btn = QPushButton("Select")
        self.select_btn.clicked.connect(self.select_product)
        layout.addWidget(self.select_btn)

        # Vars
        self.selected_product = None

        # Signals for live filtering
        self.id_filter.textChanged.connect(self.apply_filters)
        self.company_filter.textChanged.connect(self.apply_filters)
        self.name_filter.textChanged.connect(self.apply_filters)
        self.status_filter.currentIndexChanged.connect(self.apply_filters)

        self.setFocusPolicy(Qt.StrongFocus)
        # Load All Initially
        self.apply_filters()

    def apply_filters(self):
        """Apply filters and reload table live"""
        product_id = self.id_filter.text().strip().lower()
        company = self.company_filter.text().strip().lower()
        name = self.name_filter.text().strip().lower()
        status = self.status_filter.currentText()

        try:
            products = ProductRepo.get_all_products()
            
            filtered = []
            for product in products:
                # Convert product object to dict for easier filtering
                product_dict = {
                    "product_id": product.product_id,
                    "company": product.company,
                    "name": product.name,
                    "status": product.status
                }
                
                # Apply filters

                if name and name not in product_dict["name"].lower():
                    continue
                if company and company not in product_dict["company"].lower():
                    continue
                if product_id and product_id not in str(product_dict["product_id"]).lower():
                    continue
                if status != "All" and product_dict["status"] != status:
                    continue
                    
                filtered.append(product_dict)

            # Populate table
            self.table.setRowCount(len(filtered))
            for row_idx, product in enumerate(filtered):
                self.table.setItem(row_idx, 0, QTableWidgetItem(str(product["product_id"])))
                self.table.setItem(row_idx, 1, QTableWidgetItem(product["company"]))
                self.table.setItem(row_idx, 2, QTableWidgetItem(product["name"]))
                self.table.setItem(row_idx, 3, QTableWidgetItem(product["status"]))

        except Exception as e:
            print(f"Error applying filters: {e}")

    def on_double_click(self, row, column):
        """Handle double-click on table row"""
        self.select_product_from_row(row)
        
    def select_product_from_row(self, row):
        """Select product from specific row"""
        if row >= 0 and row < self.table.rowCount():
            self.selected_product = {
                "product_id": self.table.item(row, 0).text(),
                "company": self.table.item(row, 1).text(),
                "name": self.table.item(row, 2).text(),
                "status": self.table.item(row, 3).text(),
            }
            self.accept()

    def select_product(self):
        """Store selected product and close"""
        row = self.table.currentRow()
        if row >= 0:
            self.select_product_from_row(row)
        else:
            self.reject()

    def get_selected_product(self):
        """Return the selected product data"""
        return self.selected_product
    

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Down:
            # Check if focus is on any input field
            focused = self.focusWidget()
            if focused in [self.name_filter, self.company_filter, self.id_filter, self.status_filter]:
                if self.table.rowCount() > 0:
                    self.table.setFocus()
                    self.table.selectRow(0)
                    return
        super().keyPressEvent(event)