import serial
import time
import logging
from constants import *
from devices.base_reader import BaseReader

class GranvillePhillipsReader(BaseReader):
    def __init__(self):
        super().__init__("granville_phillips_350")

        logging.basicConfig(
            filename='data/serial_command.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

        try:
            self.ser = serial.Serial(
                #port='/tmp/ttyV0',
                port='/dev/ttyGP350',
                baudrate=9600,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=1,
                rtscts=True,
                dsrdtr=True
            )
        except serial.SerialException as e:
            error_msg = f"Serial error on /dev/ttyGP350: {e}"
            print(error_msg)
            logging.error(error_msg)
            self.ser = None

    def send_command(self, cmd):
        if self.ser is None:
            logging.error("Serial connection not established.")
            return ""

        # Ensure command ends with carriage return
        if not cmd.endswith('\r'):
            cmd += '\r'

        # Send command
        self.ser.write(cmd.encode())
        logging.info(f"Sent: {repr(cmd)}")

        # Wait briefly and read response
        time.sleep(0.2)
        response = self.ser.read_until(b'\r').decode().strip()
        logging.info(f"Received: {response}")
        return response

    def read(self):
        if self.ser is None:
            logging.error("Serial connection not established.")
            return [0.0]

        response = self.send_command("#RD")
        try:
            response = response[2:]
            pressure = [float(response)]
            #print(f"Pressure: {pressure}")
            if pressure[0] > 1000:
                print(f"Granville Phillips offline")
                pressure = [0.0]
        except ValueError:
            logging.error(f"Could not parse response into float: {response}")
            pressure = [0.0]
            self.restart_serial()
        return pressure

    def restart_serial(self):
        if self.ser:
            self.ser.close()

        try:
            self.ser = serial.Serial(
                #port='/tmp/ttyV0',
                port='/dev/ttyGP350',
                baudrate=9600,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=1,
                rtscts=True,
                dsrdtr=True
            )
        except serial.SerialException as e:
            error_msg = f"Serial error on /dev/ttyGP350: {e}"
            print(error_msg)
            logging.error(error_msg)
            logging.info(f"Restarting Granville Phillips connection")
            self.ser = None
        

    def cleanup(self):
        if self.ser:
            self.ser.close()
