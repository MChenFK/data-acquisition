from abc import ABC, abstractmethod

from constants import READERS
from devices.ads1256_reader import ADS1256Reader
from devices.max31856_reader import MAX31856Reader
from devices.inficon_serial_reader import InficonReader
from devices.granville_phillips_serial_reader import GranvillePhillipsReader
from devices.micromega import MicromegaReader

class BaseReader(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def cleanup(self):
        pass

def create_reader(config_name):
    name = config_name

    if name == 'max31856':
        return MAX31856Reader()
    elif name == "granville_phillips_350":
        return GranvillePhillipsReader()
    elif name == "inficon_IC/5":
        return InficonReader()
    elif name == "micromega":
        return MicromegaReader()
    elif name == 'ads1256':
        return ADS1256Reader()
    else:
        raise ValueError(f"Unsupported device type: {device_type}")


def initialize_readers(READERS):
    readers = []
    for name in READERS:
        reader = create_reader()

        readers.append(reader)
    return readers

def read_all(readers):
    results = []
    for reader in readers:
        try:
            results.extend(reader.read())
        except Exception as e:
            results.extend(0.0)

    return results
