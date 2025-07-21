import sys
import subprocess
import os
import signal

from PySide6.QtWidgets import QApplication
from file_dialog import FileDialog

class LauncherApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.dialog = FileDialog()
        self.dialog.file_selected.connect(self.launch_server)
        self.dialog.destroyed.connect(self.on_gui_closed)

        self.server_process = None

    def launch_server(self, file_path):
        # Save selected file
        with open("last_data_path.txt", "w") as f:
            f.write(file_path)

        # Set env variable for Dash app
        env = os.environ.copy()
        env["DATA_PATH"] = file_path

        # Start Gunicorn in background
        self.server_process = subprocess.Popen([
            "gunicorn", "src.web_app.app:server",
            "--bind", "0.0.0.0:8050",
            "--timeout", "120",
            "--graceful-timeout", "10",
            "--preload"
        ])


    def on_gui_closed(self):
        if self.server_process:
            print("Shutting down server...")
            self.server_process.send_signal(signal.SIGTERM)
            self.server_process.wait(timeout=10)
            print("Server shut down.")

    def run(self):
        self.dialog.show()
        self.app.exec()

if __name__ == "__main__":
    launcher = LauncherApp()
    launcher.run()
