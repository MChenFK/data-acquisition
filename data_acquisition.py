from constants import *

import sys
import time
import csv
import signal
from datetime import datetime

import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

from PySide6 import QtWidgets, QtCore
import pyqtgraph as pg

running = True

def signal_handler(sig, frame):
    global running
    print("\nCtrl+C detected! Exiting gracefully...")
    running = False

signal.signal(signal.SIGINT, signal_handler)

class ADS1115Reader(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize I2C and ADS1115
        i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = ADS.ADS1115(i2c)

        self.chan0 = AnalogIn(self.ads, ADS.P0)
        self.chan1 = AnalogIn(self.ads, ADS.P1)
        self.chan2 = AnalogIn(self.ads, ADS.P2)
        self.chan3 = AnalogIn(self.ads, ADS.P3)

        # Set up CSV file
        self.csv_file = open('ads1115_data.csv', mode='w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['Timestamp', ITEMS[RATE], ITEMS[POWER], ITEMS[PRESSURE], ITEMS[TEMPERATURE]])

        # Configure PyQtGraph colors
        pg.setConfigOption('background', WHITE)
        pg.setConfigOption('foreground', BLACK)

        # Layout for multiple plots
        self.plot_widget = pg.GraphicsLayoutWidget()
        self.setCentralWidget(self.plot_widget)

        self.plots = []
        self.curves = []
        self.y_data = [[], [], [], []]
        self.x_data = []

        # Create four separate plot areas
        titles = [ITEMS[RATE], ITEMS[POWER], ITEMS[PRESSURE], ITEMS[TEMPERATURE]]
        colors = [RED, GREEN, BLUE, PURPLE]
        for i in range(4):
            p = self.plot_widget.addPlot(row=i, col=0, title=titles[i])
            p.setLabel('left', ITEMS[i])
            p.setLabel('bottom', 'Time (s)')
            p.showGrid(x=True, y=True)
            curve = p.plot(pen=pg.mkPen(color=colors[i], width=2))
            self.plots.append(p)
            self.curves.append(curve)

        # Start time
        self.start_time = time.time()

        # Timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        refresh = REFRESH_SECONDS * 1000
        self.timer.start(refresh)

    def update(self):
        global running
        if not running:
            if not self.csv_file.closed:
                print("Closing CSV file...")
                self.csv_file.close()
            QtWidgets.QApplication.quit()
            return

        # Read voltages
        voltages = [
            self.chan0.voltage,
            self.chan1.voltage,
            self.chan2.voltage,
            self.chan3.voltage
        ]

        current_time = time.time() - self.start_time
        self.x_data.append(current_time)

        # Append data and update plots
        for i in range(4):
            self.y_data[i].append(voltages[i])
            self.curves[i].setData(self.x_data, self.y_data[i])

        # Write to CSV
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        self.csv_writer.writerow([timestamp] + voltages)
        self.csv_file.flush()

        # Keep last N points
        max_points = 500
        if len(self.x_data) > max_points:
            self.x_data = self.x_data[-max_points:]
            for i in range(4):
                self.y_data[i] = self.y_data[i][-max_points:]

    def closeEvent(self, event):
        if self.timer.isActive():
            self.timer.stop()
        if not self.csv_file.closed:
            print("Closing CSV file on window close...")
            self.csv_file.close()
        event.accept()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.showNormal()  # Exit fullscreen


def main():
    app = QtWidgets.QApplication(sys.argv)
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    reader = ADS1115Reader()
    reader.show()
    reader.showMaximized()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
