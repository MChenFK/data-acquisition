import serial
import time
from constants import *

# Constants
ACK = b'\x06'
NAK = b'\x15'
TIMEOUT = 8  # seconds

# Open serial connection
ser = serial.Serial(
    #port='/tmp/ttyV0',
    port='/dev/ttyUSB0',
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1  # read timeout per call
)

def send_command(cmd):
    """Send command, wait for ACK/NAK, and print response if available."""
    full_command = cmd.encode('ascii') + ACK
    ser.write(full_command)
    logging.info(f"Sent: {cmd} + ACK")

    response = b''
    start_time = time.time()
    got_ack = False

    while True:
        if ser.in_waiting > 0:
            byte = ser.read(1)
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