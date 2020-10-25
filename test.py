#!/usr/bin/env python
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import threading

reader = SimpleMFRC522()



# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("Door_Unlock")

# The callback for when a PUBLISH message is received from the server.
# def on_message(client, userdata, msg):
#     print(msg.topic+" "+str(msg.payload))

def on_message(client, userdata, message):
    print("Received message '" + message.payload.decode('utf-8') + "' on topic '"
        + message.topic + "' with QoS " + str(message.qos))

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
                # client.loop_forever(timeout=5.0)
        finally:
                GPIO.cleanup()

x = threading.Thread(target=read_loop)
x.start()
client.loop_forever()