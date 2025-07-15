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
            results.extend([0.0])  # fallback for errors
    return results
