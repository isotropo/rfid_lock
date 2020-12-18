#!/bin/bash

run_loop() {
    /usr/bin/python3 /home/pi/rfid_lock/rfid_scan.py
}

until run_loop; do
    echo rfid_scan.py crashed with exit code $?\n Restarting rfid_scan.py”
    sleep 2
done
