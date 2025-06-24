import serial
import time
import logging
from constants import *

class GranvillePhillipsReader:
    def __init__(self):
        logging.basicConfig(
            filename='data/granville_phillips_serial.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def send_command(self, cmd):
        return

    def get_granville_phillips_data(self):
        response = self.send_command("#RD")
        granville_phillips_data = response.split()
        pressure = float(granville_phillips_data[1])
        #print(granville_phillips_data)
        return pressure
