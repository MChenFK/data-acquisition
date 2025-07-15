import serial
import time
import logging
from constants import *
from devices.base_reader import BaseReader

BAUDRATE = 9600
RECOGNITION_CHAR = "*"

class MicromegaReader(BaseReader):
    def __init__(self, port):
        super().__init__(name=f"micromega_{port}")

        logging.basicConfig(
            filename='data/micromega_serial.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

        try:
            self.ser = serial.Serial(
                port=port,
                baudrate=BAUDRATE,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=1
            )
        except serial.SerialException as e:
            error_msg = f"Serial error on {port}: {e}"
            print(error_msg)
            logging.error(error_msg)
            self.ser = None

    def send_command(self, cmd):
        if self.ser is None:
            logging.error("Serial connection not established.")
            return ""

        # Ensure command starts with RECOGNITION_CHAR
        full_cmd = cmd if cmd.startswith(RECOGNITION_CHAR) else RECOGNITION_CHAR + cmd
        # Ensure ends with carriage return
        if not full_cmd.endswith('\r'):
            full_cmd += '\r'

        self.ser.write(full_cmd.encode())
        self.ser.flush()
        logging.info(f"Sent: {repr(full_cmd)}")

        response = self.ser.readline()
        decoded = response.decode(errors='ignore').strip()
        logging.info(f"Received: {decoded}")
        return decoded

    def read(self):
        if self.ser is None:
            return [0.0]

        response = self.send_command("V01")
        try:
            return [float(response)]
        except ValueError:
            logging.error(f"Could not parse response into float: {response}")
            return [0.0]

    def cleanup(self):
        if self.ser:
            self.ser.close()
