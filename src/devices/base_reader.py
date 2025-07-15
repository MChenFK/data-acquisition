from abc import ABC, abstractmethod

from constants import READERS
from devices.ads1256_reader import ADS1256Reader
from devices.max31856_reader import MAX31856Reader
from devices.inficon_serial_reader import InficonReader
from devices.granville_phillips_serial_reader import GranvillePhillipsReader
from devices.micromega import MicromegaReader1

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
    if config_name == 'max31856':
        return MAX31856Reader()
    elif config_name == "granville_phillips_350":
        return GranvillePhillipsReader()
    elif config_name == "inficon_IC/5":
        return InficonReader()
    elif config_name == "micromega1":
        return MicromegaReader('/dev/ttyMICROMEGA1')   # Pass port explicitly
    elif config_name == "micromega2":
        return MicromegaReader('/dev/ttyMICROMEGA2')   # Pass port explicitly
    elif config_name == 'ads1256':
        return ADS1256Reader()
    else:
        raise ValueError(f"Unsupported device type: {config_name}")

def initialize_readers(reader_names):
    readers = []
    for name in reader_names:
        reader = create_reader(name)
        readers.append(reader)
    return readers

def read_all(readers):
    results = []
    for reader in readers:
        try:
            data = reader.read()
            if isinstance(data, (list, tuple)):
                results.extend(data)
            else:
                results.append(data)
        except Exception as e:
            print(f"Error reading from {reader.name}: {e}")
            # Extend 0s for each expected item from this reader
            results.extend([0.0])
    return results
