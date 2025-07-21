from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout,
    QLineEdit, QPushButton, QFileDialog
)
from PySide6.QtCore import Signal
import os

class FileDialog(QWidget):
    file_selected = Signal(str)
    cancelled = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select Data File")
        self.setFixedSize(400, 150)

        layout = QVBoxLayout()
        self.label = QLabel("Enter file name:")
        layout.addWidget(self.label)

        # Load default path
        try:
            with open("last_data_path.txt", "r") as f:
                default_path = f.read().strip()
        except FileNotFoundError:
            default_path = ""

        self.input = QLineEdit(default_path)
        layout.addWidget(self.input)

        self.browse = QPushButton("Browse...")
        self.browse.clicked.connect(self.browse_file)
        layout.addWidget(self.browse)

        self.ok = QPushButton("Start Server")
        self.ok.clicked.connect(self.ok_clicked)
        layout.addWidget(self.ok)

        self.setLayout(layout)

    def browse_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Data File")
        if file_name:
            self.input.setText(file_name)

    def ok_clicked(self):
        file_name = self.input.text()
        if file_name:
            # Disable all UI elements to make the app uninteractable
            self.ok.setEnabled(False)
            self.input.setEnabled(False)
            self.browse.setEnabled(False)  # Disable the "Browse" button

            # Emit the signal to start the server
            self.file_selected.emit(file_name)


