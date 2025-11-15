# import sys
# from PyQt5.QtWidgets import (
#     QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
#     QMessageBox, QFileDialog
# )
# from ui.ledger_ui import LedgerUI
# from ui.accounts_ui import AccountsUI
# from ui.products_ui import ProductsUI
# from ui.sales_ui import SalesUI
# from ui.purchases_ui import PurchaseUI
# from ui.cash_receivable_ui import CashReceivableUI
# from ui.cash_payment_ui import CashPayableUI
# from ui.journal_voucher_ui import JournalVoucherUI
# from ui.salewise_profit_ui import SaleProfitReportUI
# from ui.aging_report import AgingReceivablesReport
# from ui.backup_ui import BackupDialog
# from core.backup_service import BackupService


# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Ledger Management System - Ammar Trader")
#         self.resize(500, 400)

#         layout = QVBoxLayout()
#         self.setLayout(layout)

#         # Title
#         title = QLabel("Welcome to Ammar Trader - Ledger Management System")
#         title.setStyleSheet("font-size: 16px; font-weight: bold; text-align: center;")
#         layout.addWidget(title)

#         # --- Ledger Module Button ---
#         self.ledger_btn = QPushButton("Open Ledger Module")
#         self.ledger_btn.clicked.connect(self.open_ledger)
#         layout.addWidget(self.ledger_btn)

#         # --- Accounts Module Button ---
#         self.accounts_btn = QPushButton("Open Accounts Module")
#         self.accounts_btn.clicked.connect(self.open_accounts)
#         layout.addWidget(self.accounts_btn)

#         # --- Products Module Button ---
#         self.products_btn = QPushButton("Open Products Module")
#         self.products_btn.clicked.connect(self.open_products)
#         layout.addWidget(self.products_btn)

#         # --- Sales Module Button ---
#         self.sales_btn = QPushButton("Open Sales Module")
#         self.sales_btn.clicked.connect(self.open_sales)
#         layout.addWidget(self.sales_btn)

#         # --- Purchase Module Button ---
#         self.purchase_btn = QPushButton("Open Purchase Module")
#         self.purchase_btn.clicked.connect(self.open_purchase)
#         layout.addWidget(self.purchase_btn)

#         # --- Cash Receivable Module Button ---
#         self.cash_receivable_btn = QPushButton("Open Cash Receivable Module")
#         self.cash_receivable_btn.clicked.connect(self.open_cash_receivable)
#         layout.addWidget(self.cash_receivable_btn)

#         # --- Cash Payment Module Button ---
#         self.cash_payment_btn = QPushButton("Open Cash Payment Module")
#         self.cash_payment_btn.clicked.connect(self.open_cash_payment)
#         layout.addWidget(self.cash_payment_btn)

#         # --- Journal Voucher Module Button ---
#         self.journal_voucher_btn = QPushButton("Open Journal Voucher Module")
#         self.journal_voucher_btn.clicked.connect(self.open_journal_voucher)
#         layout.addWidget(self.journal_voucher_btn)

#         self.salewiseprofit_report_btn = QPushButton("Open SaleWise Profit Report")
#         self.salewiseprofit_report_btn.clicked.connect(self.open_salewise_profitreport)
#         layout.addWidget(self.salewiseprofit_report_btn)

#         self.aging_report_btn = QPushButton("Open Aging Report")
#         self.aging_report_btn.clicked.connect(self.open_aging)
#         layout.addWidget(self.aging_report_btn)

#         # --- Backup Module Button ---
#         self.backup_btn = QPushButton("Open Backup Module")
#         self.backup_btn.clicked.connect(self.open_backup)
#         layout.addWidget(self.backup_btn)

#         # --- Quit Button ---
#         self.quit_btn = QPushButton("Quit")
#         self.quit_btn.setStyleSheet("background-color: red; color: white; font-weight: bold;")
#         self.quit_btn.clicked.connect(self.confirm_quit)
#         layout.addWidget(self.quit_btn)

#     # ------------------- Module Openers -------------------
#     def open_ledger(self):
#         self.ledger_ui = LedgerUI()
#         self.ledger_ui.show()

#     def open_accounts(self):
#         self.accounts_ui = AccountsUI()
#         self.accounts_ui.show()

#     def open_products(self):
#         self.products_ui = ProductsUI()
#         self.products_ui.show()

#     def open_sales(self):
#         self.sales_ui = SalesUI()
#         self.sales_ui.show()

#     def open_purchase(self):
#         self.purchase_ui = PurchaseUI()
#         self.purchase_ui.show()

#     def open_cash_receivable(self):
#         self.cash_receivable_ui = CashReceivableUI()
#         self.cash_receivable_ui.show()

#     def open_cash_payment(self):
#         self.cash_payment_ui = CashPayableUI()
#         self.cash_payment_ui.show()

#     def open_journal_voucher(self):
#         self.journal_voucher_ui = JournalVoucherUI()
#         self.journal_voucher_ui.show()

#     def open_salewise_profitreport(self):
#         self.salewise_profit_ui = SaleProfitReportUI()
#         self.salewise_profit_ui.show()

#     def open_aging(self):
#         self.aging_report_ui = AgingReceivablesReport()
#         self.aging_report_ui.show()

#     def open_backup(self):
#         self.backup_ui = BackupDialog()
#         self.backup_ui.exec_()
#     def closeEvent(self, event):

#         reply = QMessageBox.question(self, "Backup", 
#                                      "Do you want to take a backup before quitting?",
#                                      QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
#         if reply == QMessageBox.Yes:
#             self.backup_ui = BackupDialog()
#             self.backup_ui.backup_db()
#             event.accept()
#         elif reply == QMessageBox.No:
#             event.accept()
#         else:
#             event.ignore()
#     # ------------------- Quit with Backup -------------------
#     def confirm_quit(self):
#         reply = QMessageBox.question(
#             self,
#             "Quit Application",
#             "Do you want to take a backup before quitting?",
#             QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
#         )

#         if reply == QMessageBox.Yes:
#             folder = QFileDialog.getExistingDirectory(self, "Select Backup Folder")
#             if folder:
#                 try:
#                     file = BackupService.backup_database(folder)
#                     QMessageBox.information(self, "Success", f"Backup saved:\n{file}")
#                 except Exception as e:
#                     QMessageBox.critical(self, "Error", f"Backup failed:\n{str(e)}")
#             QApplication.quit()

#         elif reply == QMessageBox.No:
#             QApplication.quit()

#         # If Cancel → do nothing











# import sys
# from PyQt5.QtWidgets import (
#     QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
#     QMessageBox, QFileDialog, QSpacerItem, QSizePolicy, QGridLayout
# )
# from PyQt5.QtCore import Qt

# from ui.ledger_ui import LedgerUI
# from ui.accounts_ui import AccountsUI
# from ui.products_ui import ProductsUI
# from ui.sales_ui import SalesUI
# from ui.purchases_ui import PurchaseUI
# from ui.cash_receivable_ui import CashReceivableUI
# from ui.cash_payment_ui import CashPayableUI
# from ui.journal_voucher_ui import JournalVoucherUI
# from ui.salewise_profit_ui import SaleProfitReportUI
# from ui.aging_report import AgingReceivablesReport
# from ui.backup_ui import BackupDialog
# from core.backup_service import BackupService


# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Ledger Management System - Ammar Trader")
#         self.resize(1200, 750)

#         main_layout = QVBoxLayout()
#         self.setLayout(main_layout)

#         # ---------------- Header ----------------
#         title = QLabel("📊 Ammar Trader - Ledger Management System")
#         title.setAlignment(Qt.AlignCenter)
#         title.setStyleSheet("font-size: 22px; font-weight: bold; color: #2c3e50; margin: 10px;")
#         main_layout.addWidget(title)

#         # ---------------- Top Row (8 Main Modules) ----------------
#         top_row = QGridLayout()
#         top_row.setSpacing(15)

#         button_style_top = """
#             QPushButton {
#                 background-color: #34495e;
#                 color: white;
#                 font-size: 14px;
#                 font-weight: bold;
#                 padding: 15px;
#                 border-radius: 8px;
#             }
#             QPushButton:hover {
#                 background-color: #2c3e50;
#             }
#         """

#         self.accounts_btn = QPushButton("👥 Accounts"); self.accounts_btn.setStyleSheet(button_style_top); self.accounts_btn.clicked.connect(self.open_accounts)
#         self.ledger_btn = QPushButton("📒 Ledger"); self.ledger_btn.setStyleSheet(button_style_top); self.ledger_btn.clicked.connect(self.open_ledger)
#         self.products_btn = QPushButton("📦 Products"); self.products_btn.setStyleSheet(button_style_top); self.products_btn.clicked.connect(self.open_products)
#         self.sales_btn = QPushButton("💰 Sales"); self.sales_btn.setStyleSheet(button_style_top); self.sales_btn.clicked.connect(self.open_sales)
#         self.purchase_btn = QPushButton("🛒 Purchase"); self.purchase_btn.setStyleSheet(button_style_top); self.purchase_btn.clicked.connect(self.open_purchase)
#         self.cash_receivable_btn = QPushButton("💵 Cash Receivable"); self.cash_receivable_btn.setStyleSheet(button_style_top); self.cash_receivable_btn.clicked.connect(self.open_cash_receivable)
#         self.cash_payment_btn = QPushButton("💳 Cash Payment"); self.cash_payment_btn.setStyleSheet(button_style_top); self.cash_payment_btn.clicked.connect(self.open_cash_payment)
#         self.journal_voucher_btn = QPushButton("📑 Journal Voucher"); self.journal_voucher_btn.setStyleSheet(button_style_top); self.journal_voucher_btn.clicked.connect(self.open_journal_voucher)

#         main_buttons = [
#             self.accounts_btn, self.ledger_btn, self.products_btn, self.sales_btn,
#             self.purchase_btn, self.cash_receivable_btn, self.cash_payment_btn, self.journal_voucher_btn
#         ]

#         for col, btn in enumerate(main_buttons):
#             top_row.addWidget(btn, 0, col)

#         main_layout.addLayout(top_row)

#         # ---------------- Body ----------------
#         body_layout = QHBoxLayout()
#         main_layout.addLayout(body_layout)

#         # --- Left: Reserved Empty Box for Future Graphs ---
#         self.graph_placeholder = QLabel("📊 Future Graphs / Dashboard Area")
#         self.graph_placeholder.setAlignment(Qt.AlignCenter)
#         self.graph_placeholder.setStyleSheet("color: #95a5a6; font-size: 16px; border: 2px dashed #bdc3c7;")
#         body_layout.addWidget(self.graph_placeholder, 2)

#         # --- Right: Sidebar Menu ---
#         sidebar = QVBoxLayout()
#         sidebar.setSpacing(10)

#         button_style_side = """
#             QPushButton {
#                 background-color: #3498db;
#                 color: white;
#                 font-size: 14px;
#                 font-weight: bold;
#                 padding: 12px;
#                 border-radius: 8px;
#                 text-align: left;
#             }
#             QPushButton:hover {
#                 background-color: #2980b9;
#             }
#         """

#         # Add all main modules again in sidebar
#         sidebar.addWidget(QPushButton("👥 Accounts", clicked=self.open_accounts, styleSheet=button_style_side))
#         sidebar.addWidget(QPushButton("📒 Ledger", clicked=self.open_ledger, styleSheet=button_style_side))
#         sidebar.addWidget(QPushButton("📦 Products", clicked=self.open_products, styleSheet=button_style_side))
#         sidebar.addWidget(QPushButton("💰 Sales", clicked=self.open_sales, styleSheet=button_style_side))
#         sidebar.addWidget(QPushButton("🛒 Purchase", clicked=self.open_purchase, styleSheet=button_style_side))
#         sidebar.addWidget(QPushButton("💵 Cash Receivable", clicked=self.open_cash_receivable, styleSheet=button_style_side))
#         sidebar.addWidget(QPushButton("💳 Cash Payment", clicked=self.open_cash_payment, styleSheet=button_style_side))
#         sidebar.addWidget(QPushButton("📑 Journal Voucher", clicked=self.open_journal_voucher, styleSheet=button_style_side))

#         # Reports & Backup
#         sidebar.addWidget(QPushButton("📊 SaleWise Profit Report", clicked=self.open_salewise_profitreport, styleSheet=button_style_side))
#         sidebar.addWidget(QPushButton("📆 Aging Report", clicked=self.open_aging, styleSheet=button_style_side))
#         sidebar.addWidget(QPushButton("🗂 Backup", clicked=self.open_backup, styleSheet=button_style_side))

#         # Spacer pushes Power Off button down
#         sidebar.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

#         # ---------------- Power Off ----------------
#         self.quit_btn = QPushButton("🔴 Power Off", self)
#         self.quit_btn.setStyleSheet("""
#             QPushButton {
#                 background-color: #e74c3c;
#                 color: white;
#                 font-size: 15px;
#                 font-weight: bold;
#                 padding: 12px;
#                 border-radius: 8px;
#                 text-align: left;
#             }
#             QPushButton:hover {
#                 background-color: #c0392b;
#             }
#         """)
#         self.quit_btn.clicked.connect(self.confirm_quit)
#         sidebar.addWidget(self.quit_btn)

#         body_layout.addLayout(sidebar, 1)

#     # ------------------- Module Openers -------------------
#     def open_ledger(self): self.ledger_ui = LedgerUI(); self.ledger_ui.show()
#     def open_accounts(self): self.accounts_ui = AccountsUI(); self.accounts_ui.show()
#     def open_products(self): self.products_ui = ProductsUI(); self.products_ui.show()
#     def open_sales(self): self.sales_ui = SalesUI(); self.sales_ui.show()
#     def open_purchase(self): self.purchase_ui = PurchaseUI(); self.purchase_ui.show()
#     def open_cash_receivable(self): self.cash_receivable_ui = CashReceivableUI(); self.cash_receivable_ui.show()
#     def open_cash_payment(self): self.cash_payment_ui = CashPayableUI(); self.cash_payment_ui.show()
#     def open_journal_voucher(self): self.journal_voucher_ui = JournalVoucherUI(); self.journal_voucher_ui.show()
#     def open_salewise_profitreport(self): self.salewise_profit_ui = SaleProfitReportUI(); self.salewise_profit_ui.show()
#     def open_aging(self): self.aging_report_ui = AgingReceivablesReport(); self.aging_report_ui.show()
#     def open_backup(self): self.backup_ui = BackupDialog(); self.backup_ui.exec_()

#     # ------------------- Quit with Backup -------------------
#     def confirm_quit(self):
#         reply = QMessageBox.question(
#             self,
#             "Quit Application",
#             "Do you want to take a backup before quitting?",
#             QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
#         )
#         if reply == QMessageBox.Yes:
#             folder = QFileDialog.getExistingDirectory(self, "Select Backup Folder")
#             if folder:
#                 try:
#                     file = BackupService.backup_database(folder)
#                     QMessageBox.information(self, "Success", f"Backup saved:\n{file}")
#                 except Exception as e:
#                     QMessageBox.critical(self, "Error", f"Backup failed:\n{str(e)}")
#             QApplication.quit()
#         elif reply == QMessageBox.No:
#             QApplication.quit()
#         # Cancel → do nothing










import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QMessageBox, QFileDialog, QSpacerItem, QSizePolicy, QGridLayout, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import os
from pathlib import Path
from ui.ledger_ui import LedgerUI
from ui.accounts_ui import AccountsUI
from ui.products_ui import ProductsUI
from ui.sales_ui import SalesUI
from ui.purchases_ui import PurchaseUI
from ui.cash_receivable_ui import CashReceivableUI
from ui.cash_payment_ui import CashPayableUI
from ui.journal_voucher_ui import JournalVoucherUI
from ui.salewise_profit_ui import SaleProfitReportUI
from ui.aging_report import AgingReceivablesReport
from ui.backup_ui import BackupDialog
from core.backup_service import BackupService
from ui.cash_memo_ui import CashMemoUI


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ledger Management System - B I C ")
        self.resize(1000, 650)  # Reduced window size
        self.setStyleSheet("background-color: #f8f9fa;")

        # Initialize UI components
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 10, 15, 10)
        main_layout.setSpacing(12)
        self.setLayout(main_layout)

        # ---------------- Header ----------------
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                border-radius: 8px;
                padding: 12px;
            }
        """)
        header_layout = QVBoxLayout(header_frame)
        
        title = QLabel("📊 Bismillah Installment Corp - Ledger Management System")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 20px; 
                font-weight: bold; 
                color: #ecf0f1; 
                padding: 3px;
            }
        """)
        
        subtitle = QLabel("Complete Financial Management Solution")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #bdc3c7; font-size: 12px; padding: 2px;")
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        main_layout.addWidget(header_frame)

        # ---------------- Main Modules Grid ----------------
        modules_section = QVBoxLayout()
        
        section_label = QLabel("Core Modules")
        section_label.setStyleSheet("""
            QLabel {
                font-size: 14px; 
                font-weight: bold; 
                color: #2c3e50; 
                padding: 3px 0px;
            }
        """)
        modules_section.addWidget(section_label)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        # Define modules with icons and colors
        modules = [
            ("👥 Accounts", self.open_accounts, "#3498db"),
            ("📒 Ledger", self.open_ledger, "#2ecc71"),
            ("📦 Products", self.open_products, "#e74c3c"),
            ("💰 Sales", self.open_sales, "#f39c12"),
            ("🛒 Purchase", self.open_purchase, "#9b59b6"),
            ("💵 Cash Receivable", self.open_cash_receivable, "#1abc9c"),
            ("💳 Cash Payment", self.open_cash_payment, "#34495e"),
            ("📑 Journal Voucher", self.open_journal_voucher, "#d35400")
        ]

        for i, (text, callback, color) in enumerate(modules):
            btn = self.create_module_button(text, callback, color)
            row = i // 4
            col = i % 4
            grid_layout.addWidget(btn, row, col)

        modules_section.addLayout(grid_layout)
        main_layout.addLayout(modules_section)

        # ---------------- Body Content ----------------
        body_layout = QHBoxLayout()
        body_layout.setSpacing(15)
        main_layout.addLayout(body_layout)

        # --- Dashboard Area ---
        dashboard_frame = QFrame()
        dashboard_frame.setFrameStyle(QFrame.Box)
        dashboard_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 6px;
                padding: 12px;
            }
        """)
        dashboard_layout = QVBoxLayout(dashboard_frame)
        
        dashboard_title = QLabel("Dashboard Overview")
        dashboard_title.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50; margin-bottom: 8px;")
        dashboard_layout.addWidget(dashboard_title)

        # Placeholder for future graphs/charts
        graph_placeholder = QLabel("📊 Analytics & Reports Dashboard\n\nFinancial summaries, charts, and key metrics\nwill be displayed here.")
        graph_placeholder.setAlignment(Qt.AlignCenter)
        graph_placeholder.setStyleSheet("""
            QLabel {
                color: #7f8c8d; 
                font-size: 13px; 
                padding: 30px;
                border: 2px dashed #bdc3c7;
                border-radius: 5px;
                background-color: #fafafa;
            }
        """)
        graph_placeholder.setMinimumHeight(200)
        dashboard_layout.addWidget(graph_placeholder)

        body_layout.addWidget(dashboard_frame, 3)  # 3:1 ratio

        # --- Sidebar Menu ---
        sidebar_frame = QFrame()
        sidebar_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 6px;
                padding: 12px;
            }
        """)
        sidebar_layout = QVBoxLayout(sidebar_frame)

        # Cash Memo quick action
        cash_memo_btn = self.create_sidebar_button("🧾 Cash Memo", self.open_cash_memo)
        sidebar_layout.addWidget(cash_memo_btn)

        # Reports section
        reports_label = QLabel("Reports")
        reports_label.setStyleSheet("font-size: 13px; font-weight: bold; color: #34495e; margin-top: 8px;")
        sidebar_layout.addWidget(reports_label)

        report_buttons = [
            ("📊 SaleWise Profit", self.open_salewise_profitreport),
            ("📆 Aging Report", self.open_aging),
            ("🗂 Backup & Restore", self.open_backup)
        ]

        for text, callback in report_buttons:
            btn = self.create_sidebar_button(text, callback)
            sidebar_layout.addWidget(btn)

        sidebar_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # System section
        system_label = QLabel("System")
        system_label.setStyleSheet("font-size: 13px; font-weight: bold; color: #34495e; margin-top: 8px;")
        sidebar_layout.addWidget(system_label)

        # Power Off button
        power_off_btn = QPushButton("🔴 System Shutdown")
        power_off_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                font-size: 13px;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
                border: none;
                margin-top: 8px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #a93226;
            }
        """)
        power_off_btn.clicked.connect(self.confirm_quit)
        sidebar_layout.addWidget(power_off_btn)

        body_layout.addWidget(sidebar_frame, 1)

    def create_module_button(self, text, callback, color):
        button = QPushButton(text)
        button.setFixedHeight(65)  # Reduced button height
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                font-size: 13px;
                font-weight: bold;
                padding: 12px;
                border-radius: 6px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(color)};
            }}
            QPushButton:pressed {{
                background-color: {self.darken_color(color, 40)};
            }}
        """)
        button.clicked.connect(callback)
        return button

    def create_sidebar_button(self, text, callback):
        button = QPushButton(text)
        button.setFixedHeight(40)  # Reduced button height
        button.setStyleSheet("""
            QPushButton {
                background-color: #ecf0f1;
                color: #2c3e50;
                font-size: 12px;
                font-weight: bold;
                padding: 8px;
                border-radius: 5px;
                border: 1px solid #bdc3c7;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #d5dbdb;
                border-color: #95a5a6;
            }
            QPushButton:pressed {
                background-color: #bfc9ca;
            }
        """)
        button.clicked.connect(callback)
        return button

    def darken_color(self, hex_color, amount=20):
        """Darken a hex color by the specified amount"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darker = tuple(max(0, value - amount) for value in rgb)
        return f"#{darker[0]:02x}{darker[1]:02x}{darker[2]:02x}"

    def _show_single(self, attr_name, factory):
        inst = getattr(self, attr_name, None)
        if inst is not None and inst.isVisible():
            if inst.windowState() & Qt.WindowMinimized:
                inst.showNormal()
            inst.raise_()
            inst.activateWindow()
            return inst
        inst = factory()
        setattr(self, attr_name, inst)
        inst.show()
        return inst

    # ------------------- Module Openers -------------------
    def open_ledger(self): 
        self._show_single('ledger_ui', LedgerUI)

    def open_accounts(self): 
        self._show_single('accounts_ui', AccountsUI)

    def open_products(self): 
        self._show_single('products_ui', ProductsUI)

    def open_sales(self): 
        self._show_single('sales_ui', SalesUI)

    def open_purchase(self): 
        self._show_single('purchase_ui', PurchaseUI)

    def open_cash_receivable(self): 
        self._show_single('cash_receivable_ui', CashReceivableUI)

    def open_cash_payment(self): 
        self._show_single('cash_payment_ui', CashPayableUI)

    def open_journal_voucher(self): 
        self._show_single('journal_voucher_ui', JournalVoucherUI)

    def open_salewise_profitreport(self): 
        self._show_single('salewise_profit_ui', SaleProfitReportUI)

    def open_aging(self): 
        self._show_single('aging_report_ui', AgingReceivablesReport)

    def open_backup(self): 
        self.backup_ui = BackupDialog()
        self.backup_ui.exec_()

    def open_cash_memo(self):
        self._show_single('cash_memo_ui', CashMemoUI)

    # ------------------- Quit with Backup -------------------
    def confirm_quit(self):
        reply = QMessageBox.question(
            self,
            "System Shutdown",
            "Do you want to create a backup before exiting the application?",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
            QMessageBox.Yes
        )
        
        if reply == QMessageBox.Yes:
            folder = QFileDialog.getExistingDirectory(self, "Select Backup Destination Folder")
            if not folder:
                # Fallback to default backup directory inside project root
                default_dir = str((Path(__file__).resolve().parent.parent / 'backup'))
                os.makedirs(default_dir, exist_ok=True)
                folder = default_dir
            try:
                file = BackupService.backup_database(folder)
                QMessageBox.information(self, "Backup Successful", f"Database backup created successfully:\n{file}")
            except Exception as e:
                QMessageBox.critical(self, "Backup Failed", f"Unable to create backup:\n{str(e)}")
            QApplication.quit()
        elif reply == QMessageBox.No:
            QApplication.quit()
        # Cancel - do nothing


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application-wide font
    font = QFont("Segoe UI", 9)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())