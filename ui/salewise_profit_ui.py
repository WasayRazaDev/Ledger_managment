import csv
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

from datetime import datetime
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QDateEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView, QFileDialog
)
from PyQt5.QtCore import QDate, Qt
from database.reports_repo import ReportRepo


class SaleProfitReportUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sale-wise Profit & Loss Report")
        self.resize(1200, 700)
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
                color: black;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        self.report_data = []  # To store the report data for calculations
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        # --- Filter Row ---
        filter_layout = QHBoxLayout()
        layout.addLayout(filter_layout)

        filter_layout.addWidget(QLabel("Start Date:"))
        self.start_date_edit = QDateEdit(QDate.currentDate().addDays(-30))
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDisplayFormat("dd/MM/yyyy")
        filter_layout.addWidget(self.start_date_edit)

        filter_layout.addWidget(QLabel("End Date:"))
        self.end_date_edit = QDateEdit(QDate.currentDate())
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDisplayFormat("dd/MM/yyyy")
        filter_layout.addWidget(self.end_date_edit)

        filter_layout.addStretch()  # Push button to the right
        
        self.generate_btn = QPushButton("Generate Report")
        self.generate_btn.clicked.connect(self.generate_report)
        filter_layout.addWidget(self.generate_btn)
        
        self.export_btn = QPushButton("Export to CSV")
        self.export_btn.clicked.connect(self.export_to_csv)
        filter_layout.addWidget(self.export_btn)

        self.export_pdf_btn = QPushButton("Export to PDF")
        self.export_pdf_btn.clicked.connect(self.export_to_pdf)
        filter_layout.addWidget(self.export_pdf_btn)

        # --- Report Header ---
        header_layout = QVBoxLayout()
        header_layout.setAlignment(Qt.AlignCenter)
        
        # Main heading
        main_heading = QLabel("Bismillah Installment Corp")
        main_heading.setAlignment(Qt.AlignCenter)
        main_heading.setStyleSheet("font-size: 24pt; font-weight: bold; margin: 10px;")
        header_layout.addWidget(main_heading)
        
        # Sub heading
        sub_heading = QLabel("Sale-wise Profit & Loss Statement")
        sub_heading.setAlignment(Qt.AlignCenter)
        sub_heading.setStyleSheet("font-size: 14pt; font-weight: bold; margin: 15px;")
        header_layout.addWidget(sub_heading)
        
        layout.addLayout(header_layout)

        # --- Date Range and Print Date ---
        date_info_layout = QHBoxLayout()
        
        # Date range
        self.date_range_label = QLabel()
        date_info_layout.addWidget(self.date_range_label)
        
        date_info_layout.addStretch()  # Push print date to the right
        
        # Print date
        self.print_date_label = QLabel(f"Print Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        date_info_layout.addWidget(self.print_date_label)
        
        layout.addLayout(date_info_layout)

        # --- Report Table ---
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "Title", "Cell No", "Product Name", "Quantity",
            "Sale", "Purchase", "Profit", "Advance", "Balance"
        ])
        
        # Style the table header
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setStyleSheet("QHeaderView::section { background-color: #f0f0f0; padding: 5px; border: 1px solid #c0c0c0; }")
        
        # Enable alternating row colors for better readability
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("alternate-background-color: #f9f9f9; background-color: white;")
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
            }
        """)
        layout.addWidget(self.table)
        

        # --- Totals Row ---
        totals_layout = QHBoxLayout()
        totals_layout.addWidget(QLabel("Totals:"))
        
        # We'll create labels for each total that needs to be displayed
        self.quantity_total = QLabel("0")
        self.sale_total = QLabel("0.00")
        self.purchase_total = QLabel("0.00")
        self.profit_total = QLabel("0.00")
        self.advance_total = QLabel("0.00")
        self.balance_total = QLabel("0.00")
        
        # Add spacing to align with table columns
        totals_layout.addStretch()  # For Title column
        totals_layout.addStretch()  # For Cell No column
        totals_layout.addStretch()  # For Product Name column
        totals_layout.addWidget(self.quantity_total)
        totals_layout.addWidget(self.sale_total)
        totals_layout.addWidget(self.purchase_total)
        totals_layout.addWidget(self.profit_total)
        totals_layout.addWidget(self.advance_total)
        totals_layout.addWidget(self.balance_total)
        
        # Style the totals row
        for i in range(totals_layout.count()):
            widget = totals_layout.itemAt(i).widget()
            if widget:
                widget.setStyleSheet("font-weight: bold; padding: 5px;")
        
        layout.addLayout(totals_layout)

    def generate_report(self):
        start_date = self.start_date_edit.date().toPyDate()
        end_date = self.end_date_edit.date().toPyDate()
        
        # Update date range label
        self.date_range_label.setText(f"Date Range: {start_date.strftime('%d/%m/%Y')} to {end_date.strftime('%d/%m/%Y')}")

        try:
            self.report_data = ReportRepo.get_sale_profit_report(start_date, end_date)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to fetch report: {e}")
            return

        # Initialize totals
        quantity_total = 0
        sale_total = 0.0
        purchase_total = 0.0
        profit_total = 0.0
        advance_total = 0.0
        balance_total = 0.0

        self.table.setRowCount(0)
        for i, r in enumerate(self.report_data):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(r["customer"]))
            self.table.setItem(i, 1, QTableWidgetItem(r["cell_no"]))
            self.table.setItem(i, 2, QTableWidgetItem(r["product_name"]))
            self.table.setItem(i, 3, QTableWidgetItem(str(r["quantity"])))
            self.table.setItem(i, 4, QTableWidgetItem(f"{r['sale_amount']:.2f}"))
            self.table.setItem(i, 5, QTableWidgetItem(f"{r['purchase_amount']:.2f}"))
            self.table.setItem(i, 6, QTableWidgetItem(f"{r['profit']:.2f}"))
            self.table.setItem(i, 7, QTableWidgetItem(f"{r['advance']:.2f}"))
            self.table.setItem(i, 8, QTableWidgetItem(f"{r['balance']:.2f}"))
            
            # Calculate totals
            quantity_total += int(r["quantity"])
            sale_total += float(r["sale_amount"])
            purchase_total += float(r["purchase_amount"])
            profit_total += float(r["profit"])
            advance_total += float(r["advance"])
            balance_total += float(r["balance"])

        # Update totals labels
        self.quantity_total.setText(str(quantity_total))
        self.sale_total.setText(f"{sale_total:.2f}")
        self.purchase_total.setText(f"{purchase_total:.2f}")
        self.profit_total.setText(f"{profit_total:.2f}")
        self.advance_total.setText(f"{advance_total:.2f}")
        self.balance_total.setText(f"{balance_total:.2f}")

        # Update print date
        self.print_date_label.setText(f"Print Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    def export_to_csv(self):
        if not self.report_data:
            QMessageBox.warning(self, "Warning", "No data to export. Please generate a report first.")
            return
        
        # Get save file path
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Report", f"Sale_Profit_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", 
            "CSV Files (*.csv)"
        )
        
        if not file_path:
            return  # User cancelled
        
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header information
                writer.writerow(["Bismillah Installment Corp"])
                writer.writerow(["Sale-wise Profit & Loss Statement"])
                writer.writerow([])  # Empty row
                
                # Write date information
                start_date = self.start_date_edit.date().toString("dd/MM/yyyy")
                end_date = self.end_date_edit.date().toString("dd/MM/yyyy")
                writer.writerow([f"Date Range: {start_date} to {end_date}"])
                writer.writerow([f"Report Generated: {datetime.now()}"])
                writer.writerow([])  # Empty row
                
                # Write column headers
                headers = ["Title", "Cell No", "Product Name", "Quantity", "Sale", 
                        "Purchase", "Profit", "Advance", "Balance"]
                writer.writerow(headers)
                
                # Write data rows
                for row in self.report_data:
                    writer.writerow([
                        row.get("customer", ""),
                        row.get("cell_no", ""),
                        row.get("product_name", ""),
                        str(row.get("quantity", 0)),
                        f"{float(row.get('sale_amount', 0)):.2f}",
                        f"{float(row.get('purchase_amount', 0)):.2f}",
                        f"{float(row.get('profit', 0)):.2f}",
                        f"{float(row.get('advance', 0)):.2f}",
                        f"{float(row.get('balance', 0)):.2f}"
                    ])
                
                # Calculate totals
                quantity_total = sum(int(r.get("quantity", 0)) for r in self.report_data)
                sale_total = sum(float(r.get("sale_amount", 0)) for r in self.report_data)
                purchase_total = sum(float(r.get("purchase_amount", 0)) for r in self.report_data)
                profit_total = sum(float(r.get("profit", 0)) for r in self.report_data)
                advance_total = sum(float(r.get("advance", 0)) for r in self.report_data)
                balance_total = sum(float(r.get("balance", 0)) for r in self.report_data)
                
                # Write totals row
                writer.writerow([])  # Empty row
                writer.writerow([
                    "TOTALS", "", "", 
                    str(quantity_total),
                    f"{sale_total:.2f}",
                    f"{purchase_total:.2f}",
                    f"{profit_total:.2f}",
                    f"{advance_total:.2f}",
                    f"{balance_total:.2f}"
                ])
            
            QMessageBox.information(self, "Success", f"Report exported successfully to:\n{file_path}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export report: {str(e)}")



    def export_to_pdf(self):
        if not self.report_data:
            QMessageBox.warning(self, "Warning", "No data to export. Please generate a report first.")
            return

        # Save file dialog
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Report", f"Sale_Profit_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            "PDF Files (*.pdf)"
        )
        if not file_path:
            return

        try:
            doc = SimpleDocTemplate(file_path, pagesize=A4)
            elements = []
            styles = getSampleStyleSheet()

            # --- Title ---
            title = Paragraph("<b><font size=18>Bismillah Installment Corp</font></b>", styles['Title'])
            elements.append(title)
            elements.append(Spacer(1, 5))

            subtitle = Paragraph("<b><font size=14>Sale-wise Profit & Loss Statement</font></b>", styles['Title'])
            elements.append(subtitle)
            elements.append(Spacer(1, 10))

            # --- Dates row ---
            start_date = self.start_date_edit.date().toString("dd/MM/yyyy")
            end_date = self.end_date_edit.date().toString("dd/MM/yyyy")
            report_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            dates_data = [
                [f"From: {start_date} To: {end_date}", f"Report Generated: {report_date}"]
            ]
            dates_table = Table(dates_data, colWidths=[280, 280])
            dates_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
            ]))
            elements.append(dates_table)
            elements.append(Spacer(1, 10))

            # --- Table headers ---
            table_data = [
                ["Title", "Cell No", "Product Name", "Quantity",
                "Sale", "Purchase", "Profit", "Advance", "Balance"]
            ]

            # --- Add rows ---
            total_quantity = total_sale = total_purchase = total_profit = total_advance = total_balance = 0
            for row in self.report_data:
                table_data.append([
                    row.get("customer", ""),
                    row.get("cell_no", ""),
                    row.get("product_name", ""),
                    row.get("quantity", 0),
                    f"{float(row.get('sale_amount',0)):.2f}",
                    f"{float(row.get('purchase_amount',0)):.2f}",
                    f"{float(row.get('profit',0)):.2f}",
                    f"{float(row.get('advance',0)):.2f}",
                    f"{float(row.get('balance',0)):.2f}"
                ])
                total_quantity += int(row.get("quantity", 0))
                total_sale += float(row.get("sale_amount", 0))
                total_purchase += float(row.get("purchase_amount", 0))
                total_profit += float(row.get("profit", 0))
                total_advance += float(row.get("advance", 0))
                total_balance += float(row.get("balance", 0))

            # --- Add totals row ---
            table_data.append([
                "TOTALS", "", "", total_quantity,
                f"{total_sale:.2f}",
                f"{total_purchase:.2f}",
                f"{total_profit:.2f}",
                f"{total_advance:.2f}",
                f"{total_balance:.2f}"
            ])

            # --- Create table ---
            t = Table(table_data, repeatRows=1, hAlign='CENTER')
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.lightblue),
                ('TEXTCOLOR',(0,0),(-1,0),colors.white),
                ('ALIGN',(3,1),(-1,-1),'RIGHT'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0,0), (-1,0), 8),
                ('BACKGROUND', (0,-1), (-1,-1), colors.lightgrey),
                ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
                ('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ]))

            elements.append(t)
            doc.build(elements)
            QMessageBox.information(self, "Success", f"PDF exported successfully to:\n{file_path}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export PDF: {str(e)}")
