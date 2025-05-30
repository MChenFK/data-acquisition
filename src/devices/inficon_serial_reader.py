import serial

SERIAL_PORT = '/dev/ttyV0'
BAUDRATE = 9600

def main():
    try:
        with serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1) as ser:
            print(f"Listening on {SERIAL_PORT} at {BAUDRATE} baud...")
            while True:
                line = ser.readline()
                if line:
                    decoded = line.decode('utf-8', errors='replace').strip()
                    print(decoded)
    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except KeyboardInterrupt:
        print("\nExiting on user interrupt.")

if __name__ == "__main__":
    main()
