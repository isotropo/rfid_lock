#!/usr/bin/env python
import paho.mqtt.client as mqtt
from mfrc522 import SimpleMFRC522
import threading
# from time import gmtime, localtime
import time

reader = SimpleMFRC522()
should_scan = True

# unlock_GPIO = 23

# GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
# GPIO.setup(unlock_GPIO, GPIO.OUT) # GPIO Assign mode


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("Door_Unlock")
    print("Subscribed to Door_Unlock")

# The callback for when a PUBLISH message is received from the server.
# def on_message(client, userdata, msg):
#     print(msg.topic+" "+str(msg.payload))


def on_message(client, userdata, message):
    print("Door unlock for " + message.payload.decode('utf-8') + " seconds")
    # time.sleep(float(message.payload.decode('utf-8')))
    client.publish("RFID_Scan", "0")
    print("Door unlock complete")
    # unlock(message.payload.decode('utf-8'))

# def unlock(time_ms):
#     print("unlocked for "+str(time_ms)+" seconds")
#     GPIO.setup(unlock_GPIO, GPIO.OUT) # GPIO Assign mode
#     GPIO.output(unlock_GPIO, GPIO.LOW) # out
#     GPIO.output(unlock_GPIO, GPIO.HIGH) # on
#     time.sleep(time_ms) # sleep for set time
#     GPIO.output(unlock_GPIO, GPIO.LOW) # out
#     return


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# client.connect("homey.local", 1883, 60)
client.connect("hexfrontdoor.local", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.


def read_loop():
    while True:
        try:
            id, text = reader.read()
            print(id)
            # print(text)
            client.publish("RFID_Scan", str(id))
            # time.sleep(1)
            # client.loop_forever(timeout=5.0)
        finally:
            pass

x = threading.Thread(target=read_loop)

x.start()
client.loop_forever()