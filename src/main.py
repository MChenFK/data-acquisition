from ADS1115Reader import *
from settings import SettingsDialog
import config

reader = None

def signal_handler(sig, frame):
    print("\nCtrl+C detected! Exiting gracefully...")
    if reader:
        reader.running = False

signal.signal(signal.SIGINT, signal_handler)

def main():
    global reader
    
    app = QtWidgets.QApplication(sys.argv)
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    settings_dialog = SettingsDialog()
    if settings_dialog.exec():
        config.settings = settings_dialog.get_settings()
        reader = ADS1115Reader()
        reader.show()
        reader.showMaximized()

        sys.exit(app.exec())
    else:
        print("User exited settings menu")
        sys.exit(0)


if __name__ == "__main__":
    main()
