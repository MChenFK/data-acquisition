import Adafruit_GPIO.SPI as SPI
from drivers.Adafruit_MAX31856 import MAX31856
from RPi.GPIO import GPIO

class MAX31856Reader(BaseReader):
    def __init__(self, spi_port=0, spi_device=1):
        self.sensor = MAX31856(
            hardware_spi=SPI.SpiDev(spi_port, spi_device),
            tc_type=MAX31856.MAX31856_K_TYPE
        )

    def read(self):
        try:
            return [self.sensor.read_temp_c()]
        except Exception as e:
            print(f"Error reading temperature: {e}")
            return [float('nan')]

    def cleanup(self):
        GPIO.cleanup()