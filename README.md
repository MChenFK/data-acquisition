# data-acquisition

## Hardware:
- Raspberry Pi 4 Model B
- ADS1256 Analog to Digital Converter
  - DB25 Connector
  - MKS 247
- MAX31856 Thermocouple Reader
  - Type K Thermocouple
- RS232 to USB adapter x2
  - Inficon IC/5
  - Granville Phillips 350
- RS485 to USB adapter x2 (can also handle ttl and RS232)
  - Micromega Controller x2

## Requirements:
### (See requirements.txt)
- Waveshare ADS1256 library
- Adafruit MAX31856 library

## Steps:
1. Clone repository
   - Navigate to desired directory on pi
   - git clone https://github.com/MChenFK/data-acquisition
1. Install requirements
   - Inside project root directory, create python virtual environment
     - python -m venv data_acquisition_venv
   - Activate python virtual environment
     - source data_acquisition_venv/bin/activate
   - Run pip install -r requirements.txt
   - Manually download ADS1256 and MAX31856 libraries
     - Place inside data_acquisition_venv/lib/python(version)
     - https://www.waveshare.com/wiki/High-Precision_AD/DA_Board
     - 
2. Place icon on desktop and link to shell file and png
   - Do for both data collector and web app
3. Click on newly created data collector shortcut
   - Runs ./run_data_acquisition.sh
     - Activates virtual environment
     - Runs src/main.py
4. Enter file name for csv file and interval for collection
   - Defaults to date for csv file and 10 seconds for interval
   - Results may vary with lower intervals
5. Click start on data collector
6. Click on newly created web app shortcut
     - Runs ./run_web_app.sh
        - Runs src/web_app/app.py
7. Open localhost on browser
  - http://(Raspberry Pi IP):(Port Number)

## Troubleshooting:
1. Make sure cables are hooked up correctly
  - ADS1256 Analog to Digital Converter:
    - Pinout for MKS 247
    - 3: Channel 1 Scaled Output
    - 15: Channel 2 Scaled Output
    - 17: Channel 3 Scaled Output
    - 19: Channel 4 Scaled Output
  - MAX31856 Thermocouple Reader
    - Type K Thermocouple
    - Yellow +
    - Red -
  - Inficon IC/5
    - Blue RS232 to USB
  - Granville Phillips 350
    - Gray RS232 to USB
  - Micromega Controller 1 and 2
    - Black RS485 to USB
      - GND -> Black -> RTN
      - A+ -> Red -> +T/R
      - B- -> White -> -T/R
2. Make sure desktop icon is properly linked
3. Make sure COM ports align
  - Ports should be set in /etc/udev/rules.d/99-usb-serial.rules
  - Blue RS232 to USB: /dev/ttyINFICON
  - Gray RS232 to USB: /dev/ttyGP350
  - Black RS485 to USB 1: /dev/ttyMICROMEGA1
  - Black RS485 to USB 2: /dev/ttyMICROMEGA2
3. ADS1256 only reads positive voltages
  - MKS 247 outputs negative with no flow


