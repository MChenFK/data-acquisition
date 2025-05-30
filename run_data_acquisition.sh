# Navigate to project directory
#cd /home/mebryan/ADS1115/

export DISPLAY=:0
export XDG_RUNTIME_DIR=/run/user/$(id -u)

sleep 1

# Run program
./data_acquisition_venv/bin/python3 src/main.py

