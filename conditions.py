import paho.mqtt.client as mqtt
import numpy as np
import pandas as pd
import time
import RPi.GPIO as GPIO

time_ms = 10.0
unlock_GPIO = 23

GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
GPIO.setup(unlock_GPIO, GPIO.OUT) # GPIO Assign mode

# user_groups = {
#     "247_access": {
#         "allowed_times": {
#             "weekday": "00:00-00:00",
#             "weekend": "00:00-00:00"
#         },
#         "time_ms": "10.0"
#     }
# }

# print(dict_test['default_group'])


# def ifUnlocked(time_ms):
#   time_left = time_ms
#   while(time_left > 0):
#     print(time_left)
#     time.sleep(1)
#     time_left -= 1
#   return False
    
whitelist = pd.read_csv('whitelist.csv')
whitelist_df = pd.DataFrame(data=whitelist)
uid_list = whitelist_df.loc[:,'uid']

# usergroups = pd.read_csv('usergroups.csv')
# usergroups_df = pd.DataFrame(data=usergroups)

# usergroups_list = usergroups_df.to_dict()

# print(usergroups_list)


def should_unlock(scan_id):
  for uid in uid_list:
    suid = str(uid)
    # print(type(suid), type(scan_id))
    # print(suid == scan_id, suid, scan_id)
    if suid == str(scan_id):
        return True
  return False


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("RFID_Scan")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if msg.topic == "RFID_Scan":
        if should_unlock(msg.payload.decode('utf-8')):
            print("access granted")
            unlock()
            # client.publish("Door_Unlock", str(time_ms))
            client.publish("Door_Unlock", time_ms)

def unlock():
  global time_ms
  print("unlocked for "+str(time_ms)+" seconds")
  GPIO.setup(unlock_GPIO, GPIO.OUT) # GPIO Assign mode
  GPIO.output(unlock_GPIO, GPIO.LOW) # out
  GPIO.output(unlock_GPIO, GPIO.HIGH) # on
  time.sleep(time_ms) # sleep for set time
  GPIO.output(unlock_GPIO, GPIO.LOW) # out
  return

# def unlock():
#     global time_ms
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

client.connect("hexfrontdoor.local", 1883, 60)
# client.connect("homey.local", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.

client.loop_forever()
