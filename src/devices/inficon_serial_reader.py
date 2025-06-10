import serial
import time
import logging
from constants import *
from devices.inficon_constants import *

class InficonReader:
    def __init__(self):

        logging.basicConfig(
            filename='data/serial.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

        # Open serial connection
        self.ser = serial.Serial(
            # Virtual serial port for testing
            port='/tmp/ttyV0',
            #port='/dev/ttyUSB0',
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1  # read timeout per call
        )

        self.last_state = ""
        self.current_layer = 1

    def send_command(self, cmd):
        # Send command, wait for ACK/NAK, and print response if available
        full_command = cmd.encode('ascii') + ACK
        self.ser.write(full_command)
        logging.info(f"Sent: {cmd} + ACK")

        response = b''
        start_time = time.time()
        got_ack = False

        while True:
            if self.ser.in_waiting > 0:
                byte = self.ser.read(1)
                if not got_ack:
                    if byte == ACK:
                        logging.info("Received: ACK")
                        got_ack = True
                        continue
                    elif byte == NAK:
                        logging.warning("Received: NAK")
                        return "NAK Received"
                    else:
                        response += byte
                else:
                    response += byte
            elif time.time() - start_time > TIMEOUT:
                if not got_ack:
                    logging.error("Receive timeout (no ACK/NAK)")
                    return "RECEIVE TIMEOUT (no ACK/NAK)"
                else:
                    break  # End if ACK received and no more data after timeout
            else:
                time.sleep(0.01)

        decoded_response = response.decode('ascii', errors='replace').strip()
        logging.info(f"Received response: {decoded_response}")
        return decoded_response if decoded_response else "ACK Received (no response data)"

    def get_inficon_data(self):
        # rate, power, thickness
        response = self.send_command("SL 0 " + str(self.current_layer))
        if response == "NAK Received":
            inficon_data = ["NAK"]
            self.current_layer += 1
            return inficon_data
        inficon_data = response.split()
        #print(inficon_data)
        return inficon_data
        