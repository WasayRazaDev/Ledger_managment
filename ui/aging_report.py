from database.reports_repo import ReportRepo
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QTableWidget, QTableWidgetItem, QPushButton, 
                             QHeaderView, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtGui import QTextDocument, QTextCursor, QTextTableFormat, QTextCharFormat, QFont
import csv
import datetime

class AgingReceivablesReport(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aging Receivables Report")
        self.resize(1200, 700)
        
        # Apply styling
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 10pt;
                background-color: #f8f9fa;
            }
            QLabel#headerLabel {
                font-size: 18pt;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px;
            }
            QLabel#subHeaderLabel {
                font-size: 14pt;
                font-weight: bold;
                color: #3498db;
                padding: 5px;
            }
            QPushButton {
                background-color: #3498db;
                border: none;
                color: white;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
            QPushButton#exportButton {
                background-color: #2ecc71;
            }
            QPushButton#exportButton:hover {
                background-color: #27ae60;
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
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        self.setLayout(layout)

        # Header section
        header_label = QLabel("Bismillah Instalment Corporation")
        header_label.setObjectName("headerLabel")
        header_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(header_label)
        
        # Add some spacing
        layout.addSpacing(10)
        
        # Sub-header
        sub_header_label = QLabel("Aging Receivable Report")
        sub_header_label.setObjectName("subHeaderLabel")
        sub_header_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(sub_header_label)
        
        # Add some spacing
        layout.addSpacing(20)

        # Report date
        date_layout = QHBoxLayout()
        date_layout.addStretch()
        date_label = QLabel(f"Report Date: {QDate.currentDate().toString('dd-MMM-yyyy')}")
        date_layout.addWidget(date_label)
        layout.addLayout(date_layout)

        # Export buttons
        export_layout = QHBoxLayout()
        export_layout.addStretch()
        
        self.export_csv_btn = QPushButton("Export to CSV")
        self.export_csv_btn.setObjectName("exportButton")
        self.export_csv_btn.clicked.connect(self.export_to_csv)
        export_layout.addWidget(self.export_csv_btn)
        
        self.export_pdf_btn = QPushButton("Export to PDF")
        self.export_pdf_btn.setObjectName("exportButton")
        self.export_pdf_btn.clicked.connect(self.export_to_pdf)
        export_layout.addWidget(self.export_pdf_btn)
        
        layout.addLayout(export_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Account Code", "Title", "Cell", "Amount", 
            "Date", "Days", "Balance", "Voucher Type"
        ])

                # Set column widths for better spacing
        self.table.setColumnWidth(0, 100)   # Account_code
        self.table.setColumnWidth(1, 355)   # Title
        self.table.setColumnWidth(2, 120)   # Cell
        self.table.setColumnWidth(3, 100)   # Amount
        self.table.setColumnWidth(4, 100)  # Date
        self.table.setColumnWidth(5, 100)  # Days
        self.table.setColumnWidth(6, 110)  # Balance
        self.table.setColumnWidth(7, 120)  # Voucher Type
        # self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        # Load data
        self.load_data()

    def load_data(self):
        try:
            # Fetch data from the repository
            data = ReportRepo.get_receivables_report()
            
            if not data:
                QMessageBox.information(self, "No Data", "No receivables data found.")
                return
            
            # Set row count
            self.table.setRowCount(len(data))
            
            # Populate table
            for row_idx, row_data in enumerate(data):
                self.table.setItem(row_idx, 0, QTableWidgetItem(str(row_data.get('account_code', ''))))
                self.table.setItem(row_idx, 1, QTableWidgetItem(str(row_data.get('title', ''))))
                self.table.setItem(row_idx, 2, QTableWidgetItem(str(row_data.get('cell', ''))))
                self.table.setItem(row_idx, 3, QTableWidgetItem(f"{float(row_data.get('amount', 0)):,.2f}"))
                
                # Format date if it exists
                date_value = row_data.get('date', '')
                if date_value:
                    if isinstance(date_value, datetime.date):
                        formatted_date = date_value.strftime('%Y-%m-%d')
                    else:
                        formatted_date = str(date_value)
                else:
                    formatted_date = ''
                self.table.setItem(row_idx, 4, QTableWidgetItem(formatted_date))
                
                # Color code days based on age
                days = row_data.get('days', 0)
                days_item = QTableWidgetItem(str(days))
                
                if days > 90:
                    days_item.setBackground(Qt.red)
                    days_item.setForeground(Qt.white)
                elif days > 60:
                    days_item.setBackground(Qt.darkYellow)
                    days_item.setForeground(Qt.black)
                elif days > 30:
                    days_item.setBackground(Qt.yellow)
                    days_item.setForeground(Qt.black)
                self.table.setItem(row_idx, 5, days_item)
                
                self.table.setItem(row_idx, 6, QTableWidgetItem(f"{float(row_data.get('balance', 0)):,.2f}"))
                self.table.setItem(row_idx, 7, QTableWidgetItem(str(row_data.get('voucher_type', ''))))
                
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to load data: {str(e)}")

    def export_to_csv(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save CSV File", "aging_receivables_report.csv", "CSV Files (*.csv)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # Write headers
                    headers = [self.table.horizontalHeaderItem(i).text() 
                              for i in range(self.table.columnCount())]
                    writer.writerow(headers)
                    
                    # Write data
                    for row in range(self.table.rowCount()):
                        row_data = []
                        for col in range(self.table.columnCount()):
                            item = self.table.item(row, col)
                            row_data.append(item.text() if item else "")
                        writer.writerow(row_data)
                        
                QMessageBox.information(self, "Success", "CSV file exported successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export CSV: {str(e)}")

    def export_to_pdf(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save PDF File", "aging_receivables_report.pdf", "PDF Files (*.pdf)"
        )
        
        if file_path:
            try:
                # Create printer and set output
                printer = QPrinter(QPrinter.HighResolution)
                printer.setOutputFormat(QPrinter.PdfFormat)
                printer.setOutputFileName(file_path)
                printer.setPageSize(QPrinter.A4)
                printer.setFullPage(False)
                
                # Create document
                document = QTextDocument()
                
                # Build HTML content for PDF
                html = """
                <html>
                <head>
                <style>
                    body { font-family: Arial, sans-serif; }
                    .header { font-size: 18pt; font-weight: bold; text-align: center; color: #2c3e50; }
                    .subheader { font-size: 14pt; font-weight: bold; text-align: center; color: #3498db; margin-bottom: 20px; }
                    .date { text-align: right; margin-bottom: 20px; }
                    table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                    th { background-color: #3498db; color: white; padding: 8px; border: 1px solid #dee2e6; font-weight: bold; }
                    td { padding: 6px; border: 1px solid #dee2e6; }
                    .over-90 { background-color: #ffcccc; }
                    .over-60 { background-color: #ffffcc; }
                    .over-30 { background-color: #ccffcc; }
                </style>
                </head>
                <body>
                """

                html += f'<div class="header">Bismillah Instalment Corporation</div>'
                html += f'<div class="subheader">Aging Receivable Report</div>'
                html += f'<div class="date">Report Date: {QDate.currentDate().toString("dd-MMM-yyyy")}</div>'
                
                html += '<table>'
                html += '<tr>'
                for col in range(self.table.columnCount()):
                    html += f'<th>{self.table.horizontalHeaderItem(col).text()}</th>'
                html += '</tr>'
                
                for row in range(self.table.rowCount()):
                    html += '<tr>'
                    for col in range(self.table.columnCount()):
                        item = self.table.item(row, col)
                        text = item.text() if item else ""
                        
                        # Apply color coding for days column
                        if col == 5:  # Days column
                            days = int(text) if text.isdigit() else 0
                            if days > 90:
                                cell_class = "over-90"
                            elif days > 60:
                                cell_class = "over-60"
                            elif days > 30:
                                cell_class = "over-30"
                            else:
                                cell_class = ""
                            html += f'<td class="{cell_class}">{text}</td>'
                        else:
                            html += f'<td>{text}</td>'
                    html += '</tr>'
                
                html += '</table>'
                html += '</body></html>'
                
                document.setHtml(html)
                document.print_(printer)
                
                QMessageBox.information(self, "Success", "PDF file exported successfully!")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export PDF: {str(e)}")