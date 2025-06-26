import serial.tools.list_ports

ports = serial.tools.list_ports.comports()

for port in ports:
    print(f"Device: {port.device}")
    print(f"  Description: {port.description}")
    print(f"  HWID: {port.hwid}")
    print()

"""
Device: /dev/ttyS0
  Description: n/a
  HWID: n/a

Device: /dev/ttyUSB3
  Description: FT232R USB UART - FT232R USB UART
  HWID: USB VID:PID=0403:6001 SER=BG00PA11 LOCATION=1-1.4

Device: /dev/ttyUSB2
  Description: FT232R USB UART - FT232R USB UART
  HWID: USB VID:PID=0403:6001 SER=BG00ORXY LOCATION=1-1.3

Device: /dev/ttyUSB1
  Description: USB-Serial Controller D
  HWID: USB VID:PID=0557:2008 LOCATION=1-1.2

Device: /dev/ttyUSB0
  Description: USB-Serial Controller D
  HWID: USB VID:PID=067B:2303 LOCATION=1-1.1

"""