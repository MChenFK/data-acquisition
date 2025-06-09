import serial
import time

# Change this to the virtual port to listen on
PORT = '/tmp/ttyV1'  # or '/dev/pts/6' on Linux/Mac

ACK = b'\x06'
NAK = b'\x15'

def simulate_device():
    with serial.Serial(PORT, 9600, timeout=1) as ser:
        print(f"Listening on {PORT}...")

        while True:
            if ser.in_waiting > 0:
                data = ser.read(ser.in_waiting)
                print("Received:", data)

                # Check if command ends with ACK
                if data.endswith(ACK):
                    cmd = data[:-1].decode('ascii', errors='ignore').strip()
                    print(f"Command received: '{cmd}'")

                    # Example responses based on command
                    if cmd == "RG 01":
                        response = "Response to RG 01"
                        ser.write(response.encode('ascii') + ACK)
                    elif cmd == "RG 02":
                        response = "Response to RG 02"
                        ser.write(response.encode('ascii') + ACK)
                    elif cmd == "SL 0 1":
                        response = "3.281  12.900    0.004  23 00:02 01:35 GXXXXXXX  17   1"
                        ser.write(response.encode('ascii') + ACK)
                    else:
                        # Simulate a NAK for unknown commands
                        ser.write(NAK)
                else:
                    print("No ACK found at end of command. Sending NAK.")
                    ser.write(NAK)

            else:
                time.sleep(0.1)

if __name__ == "__main__":
    simulate_device()
