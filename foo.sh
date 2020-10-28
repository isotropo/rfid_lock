#!/bin/sh -e

sleep 10
docker run -i -p 1883:1883 -p 9001:9001 -v /home/pi/docker/mosquitto.conf:/mosquitto/config/mosquitto.conf -v /mosquitto/data -v /mosquitto/log eclipse-mosquitto &
sleep 60
/usr/bin/python3 /home/pi/rfid_lock/test.py &
/usr/bin/python3 /home/pi/rfid_lock/conditions.py
exit 0