from constants import *
import config
import os
import time
import csv
from datetime import datetime

from PySide6 import QtWidgets, QtCore
import pyqtgraph as pg

from devices.ads1256_reader import ADS1256Reader
from devices.max31856_reader import MAX31856Reader

class repl(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.running = True

        # Initialize readers
        self.ads_reader = ADS1256Reader()
        self.temp_reader = MAX31856Reader()

        self.num_plots = len(ITEMS)

        # Setup CSV file
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(BASE_DIR, "../")
        os.makedirs(data_dir, exist_ok=True)

        file_path = "data/" + datetime.now().strftime('%Y-%m-%d')
        rename = config.settings.get("file_name")
        if rename:
            file_path = "data/" + rename

        temp_path = file_path
        count = 1
        while os.path.isfile(temp_path + ".csv"):
            count += 1
            temp_path = file_path + f" ({count})"

        #self.csv_file = open(data_dir + temp_path + ".csv", mode='w', newline='')
        self.csv_file = open("data_acquired.csv", mode='w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['Timestamp'] + ITEMS)

        pg.setConfigOption('background', WHITE)
        pg.setConfigOption('foreground', BLACK)

        central_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(central_widget)

        self.collection_active = False
        self.toggle_button = QtWidgets.QPushButton("Start")
        self.toggle_button.clicked.connect(self.toggle_collection)
        layout.addWidget(self.toggle_button)

        self.plot_widget = pg.GraphicsLayoutWidget()
        layout.addWidget(self.plot_widget)

        self.setCentralWidget(central_widget)

        self.plots = []
        self.curves = []
        self.y_data = [[] for _ in range(self.num_plots)]
        self.x_data = []

        colors = [RED, GREEN, BLUE, PURPLE, ORANGE, CYAN, MAGENTA, PINK]
        for i in range(self.num_plots):
            row = i // 2
            col = i % 2
            p = self.plot_widget.addPlot(row=row, col=col, title=ITEMS[i])
            p.setLabel('left', ITEMS[i])
            p.setLabel('bottom', 'Time (s)')
            p.showGrid(x=True, y=True)
            curve = p.plot(pen=pg.mkPen(color=colors[i], width=2))
            self.plots.append(p)
            self.curves.append(curve)

        self.timer_started = False
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.refresh = REFRESH_SECONDS * 1000
        if config.settings.get("refresh_interval"):
            self.refresh = int(config.settings.get("refresh_interval")) * 1000

    def update(self):
        if not self.running:
            if not self.csv_file.closed:
                print("Closing CSV file...")
                self.csv_file.close()
            QtWidgets.QApplication.quit()
            return

        ads_values = self.ads_reader.read_all()
        temperature = self.temp_reader.read_temperature()

        inputs = [
            ads_values[0],
            ads_values[1],
            ads_values[2],
            temperature,
            ads_values[3],
            ads_values[4],
            ads_values[5],
            ads_values[6]
            #ads_values[7]
        ]

        current_time = time.time() - self.start_time
        self.x_data.append(current_time)

        for i in range(self.num_plots):
            self.y_data[i].append(inputs[i])
            self.curves[i].setData(self.x_data, self.y_data[i])

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.csv_writer.writerow([timestamp] + inputs)
        self.csv_file.flush()

        max_points = 100
        if len(self.x_data) > max_points:
            self.x_data = self.x_data[-max_points:]
            for i in range(self.num_plots):
                self.y_data[i] = self.y_data[i][-max_points:]

    def toggle_collection(self):
        if self.collection_active:
            self.timer.stop()
            self.toggle_button.setText("Start")
            self.collection_active = False
        else:
            if not self.timer_started:
                self.start_time = time.time()
                self.timer_started = True
            self.update()
            self.timer.start(self.refresh)
            self.toggle_button.setText("Stop")
            self.collection_active = True

    def closeEvent(self, event):
        if self.timer.isActive():
            self.timer.stop()
        if not self.csv_file.closed:
            print("Closing CSV file on window close...")
            self.csv_file.close()
        event.accept()

