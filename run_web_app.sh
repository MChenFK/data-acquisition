#!/bin/bash

export DISPLAY=:0
export XDG_RUNTIME_DIR=/run/user/$(id -u)

sleep 1

# Run program
source ./data_acquisition_venv/bin/activate
./data_acquisition_venv/bin/python3 ./src/web_app/launch_app.py

