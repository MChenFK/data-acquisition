from drivers.ADS1256 import ADS1256
import RPi.GPIO as GPIO
import spidev
from .base_reader import BaseReader

class ADS1256Reader(BaseReader):
    def __init__(self, differential=False):
        super().__init__("ads1256")

        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.mode = 1
        self.spi.max_speed_hz = 1000000

        self.adc = ADS1256.ADS1256()
        if self.adc.ADS1256_init() != 0:
            raise RuntimeError("Failed to initialize ADS1256.")

        self.num_channels = 8
        self.voltages = [0] * self.num_channels
        self.differential = differential

    def read(self):
        try:
            ADC_Value = self.adc.ADS1256_GetAll()
            for i in range(self.num_channels):
                self.voltages[i] = ADC_Value[i] * 5.0 / 0x7fffff * 100.0
            self.voltages[1] = self.voltages[1]*1.0108-1.1189
            self.voltages[2] = self.voltages[2]*1.0101-1.0603
            print(f"Voltages: {self.voltages}")
            return self.voltages[1:3]

        except Exception as e:
            return [0.0, 0.0]
            raise RuntimeError(f"Failed to read from ADS1256: {e}")

    def cleanup(self):
        GPIO.cleanup()
        self.spi.close()
