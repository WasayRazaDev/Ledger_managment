from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QPushButton, QFileDialog, QMessageBox
)
from core.backup_service import BackupService


class BackupDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Database Backup & Restore")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()

        btn_backup = QPushButton("Backup Database")
        btn_backup.clicked.connect(self.backup_db)
        layout.addWidget(btn_backup)

        btn_restore = QPushButton("Restore Database")
        btn_restore.clicked.connect(self.restore_db)
        layout.addWidget(btn_restore)

        self.setLayout(layout)

    def backup_db(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Backup Folder")
        if folder:
            try:
                file = BackupService.backup_database(folder)
                QMessageBox.information(self, "Success", f"Backup saved:\n{file}")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def restore_db(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select Backup File", "", "SQL Files (*.sql)")
        if file:
            try:
                BackupService.restore_database(file)
                QMessageBox.information(self, "Success", "Database restored successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
