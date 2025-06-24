import serial
import time
import logging
from constants import *

# Serial port and device settings
PORT = '/dev/ttyUSB0'
BAUDRATE = 9600
DEVICE_ADDRESS = ""  # RS-485 address of your device
RECOGNITION_CHAR = "*"

class MicromegaReader:
    def __init__(self):
        logging.basicConfig(
            filename='data/granville_phillips_serial.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

        try:
            self.ser = serial.Serial(
                port=PORT,
                baudrate=BAUDRATE,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=1
            )

        except serial.SerialException as e:
        error_msg = f"Serial error on {PORT}: {e}"
        print(error_msg)
        logging.error(error_msg)
        

    def send_command(self, cmd):
        

        
        user_input = input("Command> ").strip()
        if user_input.lower() == "exit":
            break

        # Ensure command starts with "*00"
        if not user_input.startswith(RECOGNITION_CHAR + DEVICE_ADDRESS):
            full_cmd = f"{RECOGNITION_CHAR}{DEVICE_ADDRESS}{user_input}"
        else:
            full_cmd = user_input

        # Ensure it ends with carriage return
        if not full_cmd.endswith('\r'):
            full_cmd += '\r'

        # Send command
        ser.write(full_cmd.encode())
        ser.flush()
        logging.info(f"Sent: {repr(full_cmd)}")

        # Wait and read response
        #time.sleep(0.05)
        #response = ser.read_until(b'\r')
        response = ser.readline()
        print("Raw:", repr(response))

        decoded = response.decode(errors='ignore').strip()
        print("Decoded:", decoded)
        logging.info(f"Received: {response}")

    ser.close()

    

    def get_data(self):
        response = self.send_command("#RD")
        granville_phillips_data = response.split()
        pressure = float(granville_phillips_data[1])
        #print(granville_phillips_data)
        return pressure