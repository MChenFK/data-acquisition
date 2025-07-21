def read_all(readers):
    results = [0.0] * 9

    for reader in readers:
        try:
            data = reader.read()
            if not isinstance(data, (list, tuple)):
                data = [data]

            if reader.name == "inficon_IC/5":
                results[0] = data[0] if len(data) > 0 else 0.0  # RATE
                results[1] = data[1] if len(data) > 1 else 0.0  # POWER
                results[4] = data[2] if len(data) > 2 else 0.0  # CRYSTAL

            elif reader.name == "granville_phillips_350":
                results[2] = data[0] if len(data) > 0 else 0.0  # PRESSURE

            elif reader.name == "max31856":
                results[3] = data[0] if len(data) > 0 else 0.0  # TEMPERATURE

            elif reader.name == "micromega_/dev/ttyMICROMEGA1":
                results[5] = data[0] if len(data) > 0 else 0.0  # ANODE CURRENT

            elif reader.name == "micromega_/dev/ttyMICROMEGA2":
                results[6] = data[0] if len(data) > 0 else 0.0  # NEUTRALIZATION CURRENT

            elif reader.name == "ads1256":
                #print(data[0])
                #print(data[1])
                results[7] = data[0] if len(data) > 0 else 0.0  # GAS FLOW
                results[8] = data[1] if len(data) > 0 else 0.0
            else:
                print(f"Unknown device: {reader.name}")

        except Exception as e:
            print(f"Error reading from {reader.name}: {e}")

    return results
