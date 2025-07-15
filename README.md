# data-acquisition

## Hardware:
- Raspberry Pi 4 Model B
- ADS1256 Analog to Digital Converter
- MAX31856 Thermocouple Reader
- RS232 to USB adapter x2
  - Inficon IC/5
  - Granville Phillips 350
- RS485 to USB adapter x2 (can also handle ttl and RS232)
  - Micromega Controller x2
    - GND -> Black -> RTN
    - A+ -> Red -> +T/R
    - B- -> White -> -T/R

## Requirements:
### (See requirements.txt)

## Steps:
1. Install requirements
   - Run pip install -r requirements.txt
   - Manually download ADS1256 and MAX31856 libraries
2. Place icon on desktop and link to shell file and png
3. Click on icon
   - Runs ./run_data_acquisition.sh
     - Activates virtual environment
     - Runs src/main.py
     - Runs src/web_app/app.py

## Troubleshooting:
1. Make sure desktop icon is properly linked
2. Make sure COM ports align
- Ports should be set in /etc/udev/rules.d/99-usb-serial.rules
- Blue RS232 to USB: /dev/ttyINFICON
- Gray RS232 to USB: /dev/ttyGP350
- Black RS485 to USB 1: /dev/ttyMICROMEGA1
- Black RS485 to USB 2: /dev/ttyMICROMEGA2


