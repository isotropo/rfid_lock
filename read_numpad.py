#!/usr/bin/env python
# coding: utf-8

# In[1]:


import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
from time import sleep     # this lets us have a time delay (see line 12) 
from datetime import datetime
from threading import Thread
print(GPIO.VERSION)


# In[2]:


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.


# In[3]:


channel = 24
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # GPIO Assign mode

edge = "FALLING"


# In[4]:


def set_edge(specify):
    global edge
    edge = specify
    return


# In[5]:


def get_edge():
    global edge
    return edge


# In[6]:


def reset_event_detect(channel):
    edge = get_edge()
    GPIO.remove_event_detect(channel)
    if edge == "RISING":   
        GPIO.add_event_detect(channel, GPIO.RISING, callback=my_callback, bouncetime=100)
    else:
        GPIO.add_event_detect(channel, GPIO.FALLING, callback=my_callback, bouncetime=100)
    return


# In[7]:


def my_callback(channel):
    now = datetime.now().strftime("%D %H:%M:%S")
    print("{0} detected on pin {1}".format(get_edge(),channel))
    if get_edge() == "FALLING":
        msg = "Door unlocked at {}".format(now)
        print(msg)
        client.publish("Pad_Event", msg)
        set_edge("RISING")
        reset_event_detect(channel)
    else:
        msg = "Door locked at {}".format(now)
        print(msg)
        client.publish("Pad_Event", msg)
        set_edge("FALLING")
        reset_event_detect(channel)


# In[8]:


client = mqtt.Client()
client.on_connect = on_connect


# In[9]:


client.connect("localhost", 1883, 60)


# In[10]:


GPIO.add_event_detect(channel, GPIO.FALLING, callback=my_callback, bouncetime=100)


# In[ ]:


client.loop_forever()


# In[ ]:




