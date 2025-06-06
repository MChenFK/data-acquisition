# Inficon (See manual)

# Constants
ACK = b'\x06'
NAK = b'\x15'
TIMEOUT = 0.2  # seconds

#7-33
STATE = [
    "READY",
    "SOURCE SWITCH",
    "RISE 1",
    "SOAK 1",
    "RISE 2",
    "SOAK 2",
    "SHUTTER DELAY",
    "DEPOSIT BEFORE RAMPS",
    "RATE RAMP 1",
    "DEPOSIT BETWEEN RAMPS",
    "RATE RAMP 2",
    "DEPOSIT AFTER RAMPS",
    "TIME POWER",
    "FEED RAMP",
    "FEED",
    "IDLE RAMP",
    "IDLE",
    "MANUAL",
    "STOP",
    "AUTOTUNE MANUAL",
    "AUTOTUNE TUNING",
    "AUTOTUNE ERROR",
    "AUTOTUNE RAMP",
    "NOT ACTIVE"
]