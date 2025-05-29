from constants import *

import os
import sys
import time
import csv
import signal
from datetime import datetime

import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

from Adafruit_MAX31856 import MAX31856
import Adafruit_GPIO.SPI as SPI

from PySide6 import QtWidgets, QtCore
import pyqtgraph as pg
import qdarktheme

class ADS1115Reader(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.running = True

        # Initialize I2C and ADS1115
        i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = ADS.ADS1115(i2c)

        self.num_plots = len(ITEMS)

        # Initialize MAX31856 Thermocouple
        SPI_PORT = 0
        SPI_DEVICE = 0
        self.temp_sensor = MAX31856(hardware_spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), tc_type=MAX31856.MAX31856_K_TYPE)

        self.chan0 = AnalogIn(self.ads, ADS.P0)
        self.chan1 = AnalogIn(self.ads, ADS.P1)
        self.chan2 = AnalogIn(self.ads, ADS.P2)
        self.chan3 = AnalogIn(self.ads, ADS.P3)

        # Placeholders:
        self.chan4 = lambda: self.chan0.voltage + 0.1
        self.chan5 = lambda: self.chan1.voltage + 0.1
        self.chan6 = lambda: self.chan2.voltage + 0.1
        #self.chan7 = lambda: self.chan3.voltage + 0.1

        # Set up CSV file
        file_path = "data/" + datetime.now().strftime('%Y-%m-%d')
        temp_path = file_path
        count = 0
        while os.path.isfile(temp_path + ".csv"):
            count += 1
            temp_path = file_path + " (" + str(count) + ")"

        #self.csv_file = open(temp_path + ".csv", mode='w', newline='')
        self.csv_file = open("ads1115_data.csv", mode='w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['Timestamp', ITEMS[RATE], ITEMS[POWER], ITEMS[PRESSURE], ITEMS[TEMPERATURE],
        ITEMS[CRYSTAL], ITEMS[ANODE], ITEMS[NEUTRALIZATION], ITEMS[GAS]])

        # Configure PyQtGraph colors
        pg.setConfigOption('background', WHITE)
        pg.setConfigOption('foreground', BLACK)

        # Main widget and layout
        central_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(central_widget)

        # Start/Stop button
        self.collection_active = False
        self.toggle_button = QtWidgets.QPushButton("Start")
        self.toggle_button.clicked.connect(self.toggle_collection)
        layout.addWidget(self.toggle_button)

        # # Dark mode button
        # self.current_theme = "light"
        # qdarktheme.setup_theme(self.current_theme)
        # self.toggle_button = QtWidgets.QPushButton("Dark Mode")
        # self.toggle_button.clicked.connect(self.toggle_dark_mode)
        # layout.addWidget(self.toggle_button)

        # Add plot widget
        self.plot_widget = pg.GraphicsLayoutWidget()
        layout.addWidget(self.plot_widget)

        self.setCentralWidget(central_widget)


        self.plots = []
        self.curves = []
        self.y_data = [[] for _ in range(self.num_plots)]
        self.x_data = []

        # Create four separate plot areas
        titles = [ITEMS[RATE], ITEMS[POWER], ITEMS[PRESSURE], ITEMS[TEMPERATURE],
        ITEMS[CRYSTAL], ITEMS[ANODE], ITEMS[NEUTRALIZATION], ITEMS[GAS]]
        colors = [RED, GREEN, BLUE, PURPLE, ORANGE, CYAN, MAGENTA, PINK]
        for i in range(self.num_plots):
            row = i // 2
            col = i % 2
            p = self.plot_widget.addPlot(row=row, col=col, title=titles[i])
            p.setLabel('left', titles[i])
            p.setLabel('bottom', 'Time (s)')
            p.showGrid(x=True, y=True)
            curve = p.plot(pen=pg.mkPen(color=colors[i], width=2))
            self.plots.append(p)
            self.curves.append(curve)

        # Start time
        # self.start_time = time.time()
        self.timer_started = False

        # Timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        refresh = REFRESH_SECONDS * 1000
        #self.timer.start(refresh)


    def update(self):
        if not self.running:
            if not self.csv_file.closed:
                print("Closing CSV file...")
                self.csv_file.close()
            QtWidgets.QApplication.quit()
            return

        try:
            temperature = self.temp_sensor.read_temp_c()
        except Exception as e:
            print(f"Error reading temperature: {e}")
            temperature = float('nan')

        # Read inputs
        inputs = [
            self.chan0.voltage,
            self.chan1.voltage,
            self.chan2.voltage,
            temperature,
            self.chan3.voltage,
            self.chan4(),
            self.chan5(),
            self.chan6()
        ]

        current_time = time.time() - self.start_time
        self.x_data.append(current_time)

        # Append data and update plots
        for i in range(self.num_plots):
            self.y_data[i].append(inputs[i])
            self.curves[i].setData(self.x_data, self.y_data[i])

        # Write to CSV
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.csv_writer.writerow([timestamp] + inputs)
        self.csv_file.flush()

        # Keep last N points
        max_points = 100
        if len(self.x_data) > max_points:
            self.x_data = self.x_data[-max_points:]
            for i in range(num_plots):
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
            self.showNormal()

    def toggle_collection(self):
        if self.collection_active:
            self.timer.stop()
            self.toggle_button.setText("Start")
            self.collection_active = False
            
        else:
            if not self.timer_started:
                self.start_time = time.time()
                self.timer_started = True
            self.timer.start(REFRESH_SECONDS * 1000)
            self.toggle_button.setText("Stop")
            self.collection_active = True
            

    # def toggle_dark_mode(self):
    #     if self.current_theme == "dark":
    #         self.current_theme = "light"
    #         self.toggle_button.setText("Dark Mode")
    #     else:
    #         self.current_theme = "dark"
    #         self.toggle_button.setText("Light Mode")

    #     # Apply the new theme
    #     qdarktheme.setup_theme(self.current_theme)

    #     # Match pyqtgraph background/foreground manually
    #     bg = '#FFFFFF' if self.current_theme == 'light' else '#121212'
    #     fg = 'black' if self.current_theme == 'light' else 'white'

    #     pg.setConfigOption('background', bg)
    #     pg.setConfigOption('foreground', fg)

    #     # Update all plot backgrounds
    #     for plot in self.plots:
    #         plot.getViewBox().setBackgroundColor(bg)
            

            


