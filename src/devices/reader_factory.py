from devices.ads1256_reader import ADS1256Reader
from devices.max31856_reader import MAX31856Reader
from devices.inficon_serial_reader import InficonReader
from devices.granville_phillips_serial_reader import GranvillePhillipsReader
from devices.micromega_serial_reader import MicromegaReader

def create_reader(config_name):
    if config_name == 'max31856':
        return MAX31856Reader()
    elif config_name == "granville_phillips_350":
        return GranvillePhillipsReader()
    elif config_name == "inficon_IC/5":
        return InficonReader()
    elif config_name == "micromega1":
        return MicromegaReader('/dev/ttyMICROMEGA1')
    elif config_name == "micromega2":
        return MicromegaReader('/dev/ttyMICROMEGA2')
    elif config_name == 'ads1256':
        return ADS1256Reader()
    else:
        raise ValueError(f"Unsupported device type: {config_name}")

def initialize_readers(reader_names):
    return [create_reader(name) for name in reader_names]
