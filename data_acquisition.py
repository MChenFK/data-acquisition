from ADS1115Reader import *

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

    reader = ADS1115Reader()
    reader.show()
    reader.showMaximized()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
