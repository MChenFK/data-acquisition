# Navigate to project directory
cd /home/mebryan/ADS1115/

export DISPLAY=:0
export XDG_RUNTIME_DIR=/run/user/$(id -u)

sleep 1

# Activate venv
# source ADS1115_venv/bin/activate

# Run program
/home/mebryan/ADS1115/ADS1115_venv/bin/python3 data_acquisition.py
