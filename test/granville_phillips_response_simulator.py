import serial
import time

PORT = '/tmp/ttyV2'

def simulate_device():
    with serial.Serial(PORT, 9600, timeout=1) as ser:
        print(f"Listening on {PORT}...")

        while True:
            if ser.in_waiting > 0:
                data = ser.read(ser.in_waiting)
                print("Received:", data)

                # Check if command starts with #
                if data.startswith('#'):
                    cmd = data[1:].decode('ascii', errors='ignore').strip()
                    print(f"Command received: '{cmd}'")

                    # Example responses based on command
                    if cmd == "RD":
                        response = "* 1.90E-05"
                        ser.write(response.encode('ascii'))
                    else:
                        # Simulate a NAK for unknown commands
                        ser.write('? SYNTX ER')
                else:
                    print("No # found at start of command. Sending syntax error.")
                    ser.write('? SYNTX ER')

            else:
                time.sleep(0.1)