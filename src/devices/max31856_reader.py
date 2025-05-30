# Global Imports
import logging
import time
import Adafruit_GPIO

# Local Imports
from Adafruit_MAX31856 import MAX31856 as MAX31856

# Raspberry Pi hardware SPI configuration.
SPI_PORT   = 0
SPI_DEVICE = 0
sensor = MAX31856(hardware_spi=Adafruit_GPIO.SPI.SpiDev(SPI_PORT, SPI_DEVICE))