
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QDialog,
                              QPushButton, QLineEdit, QComboBox,
                             QLabel, QMessageBox, QApplication, QDialogButtonBox, QGroupBox)
from PyQt5.QtCore import Qt
from database.product_repo import ProductRepo
from core.product import Product
from ui.product_search_dialog import ProductSearchDialog
from ui.enter_navigation import EnterNavigationManager

class ProductUpdateDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Update Product")
        self.setModal(True)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Product ID input
        id_layout = QHBoxLayout()
        id_layout.addWidget(QLabel("Product ID:"))
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Enter product ID to update")
        id_layout.addWidget(self.id_input)
        layout.addLayout(id_layout)
        
        # Fetch button
        self.fetch_btn = QPushButton("Fetch Product")
        self.fetch_btn.clicked.connect(self.fetch_product)
        layout.addWidget(self.fetch_btn)
        
        # Separator
        layout.addWidget(QLabel("--- Edit Product Details ---"))
        
        # Company Name
        company_layout = QHBoxLayout()
        company_layout.addWidget(QLabel("Company:"))
        self.company_input = QLineEdit()
        company_layout.addWidget(self.company_input)
        layout.addLayout(company_layout)

        # Product Name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel(" Product Name:"))
        self.name_input = QLineEdit()
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        # Status
        status_layout = QHBoxLayout()
        status_layout.addWidget(QLabel("Status:"))
        self.status_combo = QComboBox()
        self.status_combo.addItems(["active", "inactive"])
        status_layout.addWidget(self.status_combo)
        layout.addLayout(status_layout)
        
        # Disable edit fields initially
        self.set_edit_enabled(False)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        self.ok_button = button_box.button(QDialogButtonBox.StandardButton.Ok)
        self.ok_button.setEnabled(False)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
        
    def set_edit_enabled(self, enabled):
        self.company_input.setEnabled(enabled)
        self.name_input.setEnabled(enabled)
        self.status_combo.setEnabled(enabled)
        
    def fetch_product(self):
        try:
            product_id = self.id_input.text().strip()
            if not product_id:
                QMessageBox.warning(self, "Warning", "Please enter a Product ID!")
                return
                
            product = ProductRepo.get_product_by_id(int(product_id))
            if product:
                self.company_input.setText(product.company)
                self.name_input.setText(product.name)
                self.status_combo.setCurrentText(product.status)
                self.set_edit_enabled(True)
                self.ok_button.setEnabled(True)
                QMessageBox.information(self, "Success", "Product found! You can now update the details.")
            else:
                QMessageBox.warning(self, "Not Found", "Product ID not found!")
                self.set_edit_enabled(False)
                self.ok_button.setEnabled(False)
                
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter a valid numeric Product ID!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to fetch product: {str(e)}")
            
    def get_product_data(self):
        return {
            'product_id': int(self.id_input.text()),
            'company': self.company_input.text().strip(),
            'name': self.name_input.text().strip(),
            'status': self.status_combo.currentText()
        }

class ProductsUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Product Management")
        self.setGeometry(100, 100, 600, 500)
        self.apply_styles()
        self.init_ui()

    def apply_styles(self):
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
            /* Form specific styles */
            QLabel#formLabel {
                font-weight: bold;
                color: #34495e;
                min-width: 80px;
                padding: 8px 0px;
            }
            
            QLineEdit#formInput, QComboBox#formCombo {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                background-color: #ecf0f1;
                font-size: 11pt;
                min-height: 25px;
            }
            
            QLineEdit#formInput:focus, QComboBox#formCombo:focus {
                border: 2px solid #3498db;
                background-color: white;
            }
            
            QComboBox#formCombo::drop-down {
                border: 0px;
                padding-right: 10px;
            }
            
            QComboBox#formCombo::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 7px solid #7f8c8d;
            }
        """)

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Title
        title_label = QLabel("Product Management")
        title_label.setObjectName("titleLabel")
        main_layout.addWidget(title_label)

        # Form group for adding new products
        form_group = QGroupBox("Add Product")
        form_layout = QVBoxLayout()
        form_group.setLayout(form_layout)

        # Company Name
        company_layout = QHBoxLayout()
        company_label = QLabel("Company:")
        company_label.setObjectName("formLabel")
        company_layout.addWidget(company_label)
        self.company_input = QLineEdit()
        self.company_input.setPlaceholderText("Enter company name")
        self.company_input.setObjectName("formInput")
        company_layout.addWidget(self.company_input)
        form_layout.addLayout(company_layout)

        # Product Name
        name_layout = QHBoxLayout()
        name_label = QLabel(" Product Name:")
        name_label.setObjectName("formLabel")
        name_layout.addWidget(name_label)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter product name")
        self.name_input.setObjectName("formInput")
        name_layout.addWidget(self.name_input)
        form_layout.addLayout(name_layout)

        # Status
        status_layout = QHBoxLayout()
        status_label = QLabel("Status:")
        status_label.setObjectName("formLabel")
        status_layout.addWidget(status_label)
        self.status_combo = QComboBox()
        self.status_combo.addItems(["active", "inactive"])
        self.status_combo.setObjectName("formCombo")
        status_layout.addWidget(self.status_combo)
        form_layout.addLayout(status_layout)

        # Buttons
        button_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add")
        self.add_btn.setObjectName("actionButton")
        self.add_btn.clicked.connect(self.add_product)
        
        self.update_btn = QPushButton("Update")
        self.update_btn.clicked.connect(self.open_update_dialog)
        
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setObjectName("dangerButton")
        self.clear_btn.clicked.connect(self.reset_form)
        
        self.search_btn = QPushButton("Search")
        self.search_btn.setObjectName("searchButton")
        self.search_btn.clicked.connect(self.open_search_dialog)
        
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.update_btn)
        button_layout.addWidget(self.clear_btn)
        button_layout.addWidget(self.search_btn)

        form_layout.addLayout(button_layout)
        main_layout.addWidget(form_group)

        # Information label (replacing the table)
        info_label = QLabel(
            "Use the 'Search Products' button to find existing products.\n"
            "Use 'Update Product' to modify existing products by entering their ID.\n"
            "Double-click on search results to quickly update products."
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("""
            QLabel {
                background-color: #e3f2fd;
                padding: 15px;
                border-radius: 6px;
                border: 1px solid #bbdefb;
                color: #1565c0;
            }
        """)
        main_layout.addWidget(info_label)

        self.setLayout(main_layout)

        self._enter_nav = EnterNavigationManager(
            self,
            rules={
                self.company_input: {"mode": "tab_only"},
                self.name_input: {"mode": "tab_only"},
                self.status_combo: {"mode": "tab_only", "next": self.add_btn },
                self.add_btn: { "mode": "activate_only"}
            }
        )

        app = QApplication.instance()
        if app:
            app.installEventFilter(self._enter_nav)


    def add_product(self):
        try:
            company = self.company_input.text().strip()
            name = self.name_input.text().strip()
            status = self.status_combo.currentText()

            if not company or not name:
                QMessageBox.warning(self, "Warning", "Company and Name are required!")
                return

            product = Product(company=company, name=name, status=status)
            product_id = ProductRepo.add_product(product)
            
            QMessageBox.information(self, "Success", f"Product added successfully! ID: {product_id}")
            self.reset_form()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add product: {str(e)}")

    def open_update_dialog(self):
        """Open empty update dialog"""
        dialog = ProductUpdateDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            product_data = dialog.get_product_data()
            self.update_product(product_data)

    def update_product(self, product_data):
        try:
            product = Product(
                product_id=product_data['product_id'],
                company=product_data['company'],
                name=product_data['name'],
                status=product_data['status']
            )
            
            ProductRepo.update_product(product)
            QMessageBox.information(self, "Success", "Product updated successfully!")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update product: {str(e)}")

    def reset_form(self):
        self.company_input.clear()
        self.name_input.clear()
        self.status_combo.setCurrentIndex(0)

    def open_search_dialog(self):
        """Open product search dialog and handle selection"""
        search_dialog = ProductSearchDialog(self)
        if search_dialog.exec() == QDialog.DialogCode.Accepted:
            selected_product = search_dialog.get_selected_product()
            if selected_product:
                # Fill the form with selected product data for viewing
                self.company_input.setText(selected_product["company"])
                self.name_input.setText(selected_product["name"])
                self.status_combo.setCurrentText(selected_product["status"])
                
                QMessageBox.information(
                    self, 
                    "Product Loaded", 
                    f"Product details loaded from search.\n"
                    f"You can now add a similar product or use the update dialog to modify existing products."
                )
            else:
                QMessageBox.information(self, "Info", "No product selected from search.")



   