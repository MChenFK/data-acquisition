# splash.py

import sys
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QWidget, QLabel, QProgressBar, QVBoxLayout
from PySide6.QtCore import Qt
import subprocess

class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.SplashScreen | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setFixedSize(400, 200)

        self.label = QLabel("Loading ADS1115 Reader...\nPlease wait...", self)
        self.label.setAlignment(Qt.AlignCenter)

        self.progress = QProgressBar(self)
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(True)

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.label)
        layout.addWidget(self.progress)
        layout.addStretch()
        self.setLayout(layout)

    def setProgress(self, val):
        self.progress.setValue(val)

def main():
    app = QtWidgets.QApplication(sys.argv)

    splash = SplashScreen()
    splash.show()
    app.processEvents()

    progress = 0

    def update_progress():
        nonlocal progress
        progress += 10
        splash.setProgress(progress)
        if progress >= 100:
            timer.stop()
            splash.close()

            # Launch the main app script after splash finishes
            subprocess.Popen([sys.executable, "data_acquisition.py"], start_new_session=True)
            QtWidgets.QApplication.quit()

    timer = QtCore.QTimer()
    timer.timeout.connect(update_progress)
    timer.start(200)  # adjust speed as needed

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
