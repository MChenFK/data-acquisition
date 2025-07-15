import Adafruit_GPIO.SPI as SPI
from drivers.Adafruit_MAX31856 import MAX31856
import RPi.GPIO as GPIO
from devices.base_reader import BaseReader

class MAX31856Reader(BaseReader):
    def __init__(self, spi_port=0, spi_device=1):
        super().__init__("max31856")  # Initialize BaseReader with name

        try:
            self.sensor = MAX31856(
                hardware_spi=SPI.SpiDev(spi_port, spi_device),
                tc_type=MAX31856.MAX31856_K_TYPE
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize MAX31856 sensor: {e}")

    def read(self):
        try:
            return [self.sensor.read_temp_c()]
        except Exception as e:
            print(f"Error reading temperature: {e}")
            return [float('nan')]

    def cleanup(self):
        GPIO.cleanup()
