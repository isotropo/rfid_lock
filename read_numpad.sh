#!/bin/bash

run_loop() {
    /usr/bin/python3 /home/pi/rfid_lock/read_numpad.py
}

until run_loop; do
    echo read_numpad.py crashed with exit code $?\n Restarting read_numpad.py”
    sleep 2
done
