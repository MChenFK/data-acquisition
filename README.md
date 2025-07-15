# data-acquisition

## Hardware:
- Raspberry Pi 4 Model B
- ADS1256
- MAX31856
- RS-232 to USB adapter

## Steps:
1. Install requirements

## Requirements:
### (See requirements.txt)

## Troubleshooting:
1. Make sure COM ports align
- Ports should be set in /etc/udev/rules.d/99-usb-serial.rules
- Blue serial to USB: /dev/ttyINFICON
- Gray serial to USB: /dev/ttyGP350
- Black RS485 to USB 1: /dev/ttyMICROMEGA1
- Black RS485 to USB 2: /dev/ttyMICROMEGA2


