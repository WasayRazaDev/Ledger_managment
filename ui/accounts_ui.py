
# ui/accounts_ui.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,QApplication,
    QMessageBox, QComboBox, QCheckBox, QGroupBox, QGridLayout, QSpacerItem, 
    QSizePolicy
)
from PyQt5.QtGui import QFont 
from core.account import Account
from database.account_repo import AccountRepo
from ui.account_search_dialog import AccountSearchDialog
from ui.enter_navigation import EnterNavigationManager


class AccountsUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📊 Accounts Management")
        self.setGeometry(200, 200, 800, 400)
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', Arial;
                font-size: 10pt;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton#searchBtn {
                background-color: #2196F3;
            }
            QPushButton#searchBtn:hover {
                background-color: #1976D2;
            }
            QPushButton#clearBtn {
                background-color: #f44336;
            }
            QPushButton#clearBtn:hover {
                background-color: #d32f2f;
            }
            QLineEdit, QComboBox {
                padding: 6px;
                border: 1px solid #cccccc;
                border-radius: 4px;
                background-color: white;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #2196F3;
            }
        """)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.layout)

        # --- Header ---
        header_label = QLabel("💼 Accounts Management System")
        header_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        header_label.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")
        self.layout.addWidget(header_label)

        # --- Form Section ---
        form_group = QGroupBox("Account Details")
        form_layout = QGridLayout()
        form_group.setLayout(form_layout)

        # Form fields with labels - Type as first field
        form_layout.addWidget(QLabel("📊 Type:"), 0, 0)
        self.type_combo = QComboBox()
        self.type_combo.addItems(["CUSTOMER", "SUPPLIER", "SYSTEM"])  # Only 3 types
        self.type_combo.setCurrentText("CUSTOMER")  # Set CUSTOMER as default
        form_layout.addWidget(self.type_combo, 0, 1)

        form_layout.addWidget(QLabel("🔢 Account Code:"), 0, 2)
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("Enter code or leave empty for auto")
        self.code_input.setMaxLength(8)
        self.code_input.textChanged.connect(self.on_code_changed)
        form_layout.addWidget(self.code_input, 0, 3)

        form_layout.addWidget(QLabel("📛 Title:"), 1, 0)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Required field")
        form_layout.addWidget(self.name_input, 1, 1)

        form_layout.addWidget(QLabel("🏷️ Unit:"), 1, 2)
        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("Optional category")
        form_layout.addWidget(self.category_input, 1, 3)

        form_layout.addWidget(QLabel("📞 Cell #:"), 2, 0)
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Cell number")
        self.phone_input.setMaxLength(11)
        form_layout.addWidget(self.phone_input, 2, 1)

        form_layout.addWidget(QLabel("✅ Status:"), 2, 2)
        self.status_checkbox = QCheckBox("Active Account")
        self.status_checkbox.setChecked(True)
        form_layout.addWidget(self.status_checkbox, 2, 3)

        self.layout.addWidget(form_group)

        # --- Buttons Section ---
        button_group = QGroupBox("Actions")
        button_layout = QHBoxLayout()
        button_group.setLayout(button_layout)

        self.save_btn = QPushButton("💾 Save Account")
        self.save_btn.clicked.connect(self.save_account)
        self.save_btn.setToolTip("Save account (add new or update existing)")

        self.search_btn = QPushButton("🔍 Search Accounts")
        self.search_btn.clicked.connect(self.open_search_dialog)
        self.search_btn.setObjectName("searchBtn")
        self.search_btn.setToolTip("Search for existing accounts")

        self.clear_btn = QPushButton("🗑️ Clear Form")
        self.clear_btn.clicked.connect(self.clear_form)
        self.clear_btn.setObjectName("clearBtn")
        self.clear_btn.setToolTip("Clear all form fields")

        self.suggest_btn = QPushButton("💡 New Account")
        self.suggest_btn.clicked.connect(self.suggest_account_code)
        self.suggest_btn.setToolTip("Get next available account code")

        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.search_btn)
        button_layout.addWidget(self.clear_btn)
        button_layout.addWidget(self.suggest_btn)
        button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.layout.addWidget(button_group)

        # --- Status Bar ---
        status_layout = QHBoxLayout()
        self.status_label = QLabel("Ready - Enter account code or click 'Suggest Code'")
        self.status_label.setStyleSheet("color: #666; font-style: italic;")
        status_layout.addWidget(self.status_label)
        status_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.layout.addLayout(status_layout)

        self._enter_nav = EnterNavigationManager(
            self,
            rules={
                
                self.name_input: {"mode": "tab_only"},
                self.category_input: {"mode": "tab_only"},
                self.phone_input: {"mode": "tab_only"},
                self.save_btn: {"mode": "both","next": self.suggest_btn},
                self.suggest_btn: {"mode": "activate_only"},
            }
        )

        app = QApplication.instance()
        if app:
            app.installEventFilter(self._enter_nav)


    def on_code_changed(self):
        """When account code is changed, check if it exists and auto-fill if found"""
        code = self.code_input.text().strip()
        if code:
            account = AccountRepo.get_account_by_code(code)
            if account:
                self.fill_form_with_account(account)
                self.status_label.setText(f"Existing account found: {account.title}")
            else:
                self.status_label.setText("New account - ready to save")

    def fill_form_with_account(self, account):
        """Fill form fields with account data"""
        self.name_input.setText(account.title or "")
        
        # Set account type in combo box
        index = self.type_combo.findText(account.account_type or "")
        if index >= 0:
            self.type_combo.setCurrentIndex(index)

        self.category_input.setText(account.unit or "")
        self.phone_input.setText(account.cell or "")
        self.status_checkbox.setChecked(account.status == "ACTIVE")

    # def suggest_account_code(self):
    #     """Get the next available account code"""
    #     try:
    #         # Get all accounts to find the maximum code
    #         accounts = AccountRepo.list_accounts()
    #         max_code = 0
            
    #         for account in accounts:
    #             if account.account_code and account.account_code.isdigit():
    #                 code_num = int(account.account_code)
    #                 if code_num > max_code:
    #                     max_code = code_num
            
    #         next_code = str(max_code + 1).zfill(3)  # Format as 3-digit number
    #         self.code_input.setText(next_code)
    #         self.status_label.setText(f"Suggested code: {next_code}")
    #         self.name_input.setFocus()
    #     except Exception as e:
    #         QMessageBox.warning(self, "Error", f"Could not suggest code: {str(e)}")



    def suggest_account_code(self):
        """Get the next available account code based on selected type"""
        try:
            # Define account code ranges for each type
            ranges = {
                "SYSTEM": (10000001, 19999999),
                "SUPPLIER": (20000001, 29999999),
                "CUSTOMER": (30000001, 39999999)
            }
            
            selected_type = self.type_combo.currentText()
            min_range, max_range = ranges.get(selected_type, (10000001, 19999999))
            
            # Get all accounts to find the maximum code for the selected type
            accounts = AccountRepo.list_accounts()
            max_code = min_range - 1  # Start from min_range - 1
            
            for account in accounts:
                if account.account_code and account.account_code.isdigit():
                    code_num = int(account.account_code)
                    # Only consider codes within the selected type's range
                    if min_range <= code_num <= max_range and code_num > max_code:
                        max_code = code_num
            
            # If no codes found in the range, start from min_range
            if max_code < min_range:
                next_code = str(min_range)
            else:
                # Increment and ensure it doesn't exceed max_range
                next_code = str(min(max_code + 1, max_range))
            
            self.code_input.setText(next_code)
            self.status_label.setText(f"Suggested {selected_type.lower()} code: {next_code}")
            self.name_input.setFocus()
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not suggest code: {str(e)}")



    def save_account(self):
        """Save account - automatically handles both add and update"""
        code = self.code_input.text().strip()
        name = self.name_input.text().strip()
        account_type = self.type_combo.currentText()
        category = self.category_input.text().strip()
        phone = self.phone_input.text().strip()
        status = "ACTIVE" if self.status_checkbox.isChecked() else "INACTIVE"

        if not name:
            QMessageBox.warning(self, "⚠️ Error", "Account name is required")
            return

        # Check if account already exists
        existing_account = None
        if code:
            existing_account = AccountRepo.get_account_by_code(code)

        if existing_account:
            # Update existing account
            existing_account.title = name
            existing_account.account_type = account_type
            existing_account.unit = category
            existing_account.cell = phone
            existing_account.status = status
            
            AccountRepo.update_account(existing_account)
            QMessageBox.information(self, "✅ Updated", f"Account '{name}' has been updated successfully!")
            self.status_label.setText(f"Account '{name}' updated")
        else:
            # Add new account
            account = Account(
                account_code=code or None,  # Let DB auto-generate if empty
                title=name,
                account_type=account_type,
                unit=category,
                cell=phone,
                status=status
            )

            AccountRepo.add_account(account)
            QMessageBox.information(self, "✅ Success", f"Account '{account.title}' has been added successfully!")
            self.status_label.setText(f"Account '{account.title}' added successfully")

        self.clear_form()

    def open_search_dialog(self):
        dialog = AccountSearchDialog(self)
        if dialog.exec_():
            selected_account = dialog.selected_account
            if selected_account:
                # Load the selected account into the form
                account_code = selected_account['account_code']
                account = AccountRepo.get_account_by_code(account_code)
                if account:
                    self.code_input.setText(account.account_code or "")
                    self.fill_form_with_account(account)
                    self.status_label.setText(f"Loaded from search: {account.title}")

    def clear_form(self):
        self.code_input.clear()
        self.name_input.clear()
        self.category_input.clear()
        self.phone_input.clear()
        self.type_combo.setCurrentText("CUSTOMER")  # Reset to CUSTOMER default
        self.status_checkbox.setChecked(True)
        self.status_label.setText("Form cleared - ready for new entry")


    def closeEvent(self, event):
        app = QApplication.instance()
        if app and hasattr(self, "_enter_nav"):
            app.removeEventFilter(self._enter_nav)
        super().closeEvent(event)