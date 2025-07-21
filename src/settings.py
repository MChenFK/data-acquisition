import re
from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QVBoxLayout, QMessageBox

class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("40 Inch Data Acquisition")
        self.resize(400, 100)

        self.file_name = QLineEdit()
        self.refresh_interval = QLineEdit()
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.validate_and_accept)

        form_layout = QFormLayout()
        form_layout.addRow("File Name (Default yyyy-mm-dd):", self.file_name)
        form_layout.addRow("Refresh Interval (Default 10 sec):", self.refresh_interval)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(self.ok_button)
        self.setLayout(layout)

    def validate_and_accept(self):
        file_name = self.file_name.text().strip()
        refresh_interval = self.refresh_interval.text().strip()

        # Only allow alphanumeric, underscore, hyphen, and dot
        if file_name:
            if not re.match(r'^[\w\-.]+$', file_name):
                self._show_error("File name contains invalid characters. Allowed: letters, numbers, _, -, .")
                return

        # Validate refresh_interval (must be empty or a non-negative integer)
        if refresh_interval:
            if not refresh_interval.isdigit():
                self._show_error("Refresh interval must be a non-negative integer.")
                return

        self.accept()

    def _show_error(self, message):
        QMessageBox.warning(self, "Invalid Input", message)

    def get_settings(self):
        return {
            "file_name": self.file_name.text(),
            "refresh_interval": self.refresh_interval.text()
        }

