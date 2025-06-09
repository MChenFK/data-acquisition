import subprocess
import os
import signal
import time

def create_virtual_ports():
    # Start socat to create a virtual serial port pair
    print("[INFO] Creating virtual ports...")
    proc = subprocess.Popen(
        ['socat', '-d', '-d', 'PTY,link=/tmp/ttyV0,raw,echo=0', 'PTY,link=/tmp/ttyV1,raw,echo=0'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    print("[INFO] socat process started. Ports: /tmp/ttyV0 <==> /tmp/ttyV1")
    return proc

def remove_virtual_ports(proc):
    print("[INFO] Terminating socat process...")
    proc.terminate()
    time.sleep(1)
    for port in ["/tmp/ttyV0", "/tmp/ttyV1"]:
        try:
            os.remove(port)
            print(f"[INFO] Removed: {port}")
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    try:
        proc = create_virtual_ports()
        print("[INFO] Press Ctrl+C to stop.")
        proc.wait()
    except KeyboardInterrupt:
        remove_virtual_ports(proc)
