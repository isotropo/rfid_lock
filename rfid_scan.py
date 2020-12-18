#!/usr/bin/env python
import paho.mqtt.client as mqtt
from mfrc522 import SimpleMFRC522
import threading
# from time import gmtime, localtime
import time


reader = SimpleMFRC522()
last_id = ""

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("Door_Unlock")
    print("Subscribed to Door_Unlock")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, message):
    print("Door unlock for " + message.payload.decode('utf-8') + " seconds")
    # time.sleep(float(message.payload.decode('utf-8')))
    client.publish("RFID_Scan", "0")
    print("Door unlock complete")
    # unlock(message.payload.decode('utf-8'))


# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
def read_loop():
    global last_id, reader
    while True:
        try:
            uid, text = reader.read()
            print("ID: %s" % (uid))
            client.publish("RFID_Scan", uid)
        except (RuntimeError, TypeError, NameError, ValueError):
            pass
        finally:
            pass


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
x = threading.Thread(target=read_loop)
x.start()
client.loop_forever()