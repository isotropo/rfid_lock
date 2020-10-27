import numpy as np
import pandas as pd
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

whitelist = pd.read_csv('whitelist.csv')
df = pd.DataFrame(data=whitelist)
uid_list = df.loc[:,'uid']

id = 987204272652

def should_unlock(id,uid_list):
  ret = False
  for uid in uid_list:
    if uid == id:
      ret = True
  return ret

print(should_unlock(id,uid_list))

# def unlock(time_ms):
#     if should_unlock(id,uid_list):
#         # flip relay pin for n seconds
#         # publish door unlocked
#         # publish door locked