import serial
import time
import logging
from constants import *
from devices.inficon_constants import *
from devices.base_reader import BaseReader

class InficonReader(BaseReader):
    def __init__(self):
        super().__init__("inficon_IC/5")

        logging.basicConfig(
            filename='data/inficon_serial.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

        self.ser = serial.Serial(
            #port='/tmp/ttyV0',
            port='/dev/ttyINFICON',
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1
        )

        self.last_state = ""
        self.current_layer = 1

    def send_command(self, cmd):
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
                    break
            else:
                time.sleep(0.01)

        decoded_response = response.decode('ascii', errors='replace').strip()
        logging.info(f"Received response: {decoded_response}")
        return decoded_response if decoded_response else "ACK Received (no response data)"

    def read(self):
        print(f"Checking Layer: {self.current_layer}")
        response = self.send_command("SL 0 " + str(self.current_layer))
        print(f"Raw Inficon Response: {response}")
        if response == "NAK Received":
            inficon_data = ["NAK", "NAK", "NAK"]
            self.current_layer += 1
            if self.current_layer > 16:
                self.current_layer = 1
            return inficon_data

        try:
            parts = response.split()
            inficon_data = [float(parts[i]) for i in range(3)]
        except (ValueError, IndexError):
            logging.error(f"Could not parse first 3 values into floats: {response}")
            inficon_data = [0.0, 0.0, 0.0]
        return inficon_data


    def cleanup(self):
        self.ser.close()
