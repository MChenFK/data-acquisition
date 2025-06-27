import serial
import time
import logging
from constants import *

class GranvillePhillipsReader(BaseReader):
    def __init__(self):
        logging.basicConfig(
            filename='data/granville_phillips_serial.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

        try:
            self.ser = serial.Serial(
                #port='/tmp/ttyV0',
                port='/dev/ttyUSB0',
                baudrate=9600,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=1,
                rtscts=True,
                dsrdtr=True)
        
        except serial.SerialException as e:
            error_msg = f"Serial error on {port}: {e}"
            print(error_msg)
            logging.error(error_msg)

    def send_command(self, cmd):
        # Ensure it ends with carriage return
        if not cmd.endswith('\r'):
            cmd += '\r'

        # Send command
        ser.write(cmd.encode())
        logging.info(f"Sent: {repr(cmd)}")
        
        # Wait briefly and read response
        time.sleep(0.2)
        response = ser.read_until(b'\r').decode().strip()
        #print(f"Response: {response}")
        logging.info(f"Received: {response}")
        return response

    def read(self):
        response = self.send_command("#RD")
        pressure = [float(response)]
        #print(granville_phillips_data)
        return pressure

    def cleanup(self):
        self.ser.close()
