from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout,
    QLineEdit, QPushButton, QFileDialog, QMessageBox
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

    import os

    def ok_clicked(self):
        file_name = self.input.text().strip()
        if not file_name:
            return

        if os.path.isabs(file_name) and os.path.isfile(file_name):
            full_path = file_name
        else:
            # Get path to project root (../.. from src/web_app)
            script_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
            if file_name.startswith("data/"):
                data_dir = project_root
            else:
                data_dir = os.path.join(project_root, "data")
            candidate_path = os.path.normpath(os.path.join(data_dir, file_name))

            if os.path.isfile(candidate_path):
                full_path = candidate_path
            else:
                QMessageBox.warning(
                    self,
                    "File Not Found",
                    f"Could not find file:\n\n{file_name}\n\nChecked:\n{candidate_path}"
                )
                return

        # Disable interaction
        self.ok.setEnabled(False)
        self.input.setEnabled(False)
        self.browse.setEnabled(False)

        self.file_selected.emit(full_path)

