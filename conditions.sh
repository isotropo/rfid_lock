#!/bin/bash

run_loop() {
    /usr/bin/python3 /home/pi/rfid_lock/conditions.py
}

until run_loop; do
    echo “conditions.py crashed with exit code $?\n Restarting conditions.py”
    sleep 2
done
