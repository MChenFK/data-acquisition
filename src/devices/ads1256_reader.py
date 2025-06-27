from drivers.ADS1256 import ADS1256
import RPi.GPIO as GPIO
import spidev

class ADS1256Reader(BaseReader):
    def __init__(self, differential=False):
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.mode = 1
        self.spi.max_speed_hz = 1000000


        self.adc = ADS1256.ADS1256()
        if self.adc.ADS1256_init() != 0:
            raise RuntimeError("Failed to initialize ADS1256.")
        self.num_channels = 8
        self.voltages = [0] * self.num_channels

    def read(self):
        try:
            ADC_Value = self.adc.ADS1256_GetAll()
            for i in range(self.num_channels):
                self.voltages[i] = ADC_Value[i]*5.0/0x7fffff
            return self.voltages

        except Exception as e:
            GPIO.cleanup()
            raise RuntimeError(f"Failed to read from ADS1256: {e}")

    def cleanup(self):
        GPIO.cleanup()

