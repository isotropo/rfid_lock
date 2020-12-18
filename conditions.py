import paho.mqtt.client as mqtt
import numpy as np
import pandas as pd
import time
import RPi.GPIO as GPIO
import os
import datetime
import threading

time_s = 10.0
unlock_GPIO = 23
last_id = 0
should_add_next = False

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # GPIO Numbers instead of board numbers
GPIO.setup(unlock_GPIO, GPIO.OUT)  # GPIO Assign mode

whitelist_file = '/home/pi/rfid_lock/whitelist.csv'

# super_list = whitelist_df.loc[whitelist_df['user_type'] == 'super', 'uid']
    

# Time is within a range
def time_in_range(index):
    whitelist_df = get_whitelist_df()
    """Return true if now is in the range [start, end]"""
    start = whitelist_df.loc[index,'start_time']
    end = whitelist_df.loc[index,'end_time']
    now = datetime.datetime.now().time()
    if start <= end:
        return start <= now <= end
    else:
        return start <= now or now <= end

def get_whitelist():
    global whitelist_file
    dateparse = lambda x: pd.to_datetime(x, format='%H:%M:%S').time()
    whitelist = pd.read_csv(whitelist_file, parse_dates=['start_time','end_time'], date_parser=dateparse)
    return whitelist

def get_whitelist_df():
    global whitelist, whitelist_df
    whitelist = get_whitelist()
    whitelist_df = pd.DataFrame(data=whitelist)
    return whitelist_df

def get_uid_list():
    whitelist_df = get_whitelist_df()
    uid_list = whitelist_df.loc[:, 'uid']
    return uid_list

def get_admin_list():
    whitelist_df = get_whitelist_df()
    admin_list = whitelist_df.loc[whitelist_df['user_type'] == 'admin', 'uid']
    return admin_list

# The function that iterates through the uid_list and checks if a scanned id exists in the uid_list
def should_unlock(scan_id):
    set_last_id(scan_id)
    uid_list = get_uid_list()
    for index, uid in enumerate(uid_list, start=0):
        if str(uid) == str(scan_id) and time_in_range(index):
            return True
    return False

# Check if scan_id is in admin_list
def is_admin(scan_id):
    admin_list = get_admin_list()
    for uid in admin_list:
        if str(uid) == str(scan_id):
            print("admin")
            return True
    return False

def is_user(scan_id):
    uid_list = get_uid_list()
    for uid in uid_list:
        if str(uid) == str(scan_id):
            return True
    return False

def get_last_id():
    global last_id
    return last_id

def get_should_add_next():
    global should_add_next
    return should_add_next

def set_should_add_next(add_next):
    global should_add_next
    should_add_next = add_next

def get_super_add():
    global super_add
    return super_add

# The function that checks if a scanned uid should be added.
def should_add(scan_id):
    should_add_next = get_should_add_next()
    if is_admin(scan_id) and should_add_next == False:
        set_should_add_next(True)
        set_last_id(scan_id)
        return True
    else:
        set_last_id(scan_id)
        return False

def get_start_time(user_type):
    start_time = '00:00:00'
    return start_time

def get_end_time(user_type):
    end_time = '23:59:59'
    return end_time

def make_concat_list(scan_id,user_type,uid_num):
    concat_list = pd.DataFrame({
            "user": ["user" + str(uid_num)],
            "user_type": [str(user_type)],
            "uid": [str(scan_id)],
            "start_time": [pd.to_datetime(get_start_time(user_type), format='%H:%M:%S').time()],
            "end_time": [pd.to_datetime(get_end_time(user_type), format='%H:%M:%S').time()]
    })
    return concat_list

def update_whitelist(concat_list):
    global whitelist_file, whitelist_df
    whitelist_df = whitelist_df.append(concat_list, ignore_index=True)
    whitelist_df.to_csv(
        whitelist_file,
        index=False,
        columns={"user", "user_type", "uid", "start_time", "end_time"},
        date_format='%H:%M:%S'
    )
    print("Whitelist successfully updated.")
    return True

# The function that gets called after an admin token is swiped, which adds the scanned id to the whitelist.csv file and repopulates the uid_list.
def add_uid(scan_id):
    if is_user(scan_id):
        return False
    if scan_id == "0":
        return False
    should_add_next = get_should_add_next()
    if should_add_next == True:
        user_type = "default"
        uid_list = get_uid_list()
        uid_num = str(len(uid_list))
        update_whitelist(make_concat_list(scan_id,user_type,uid_num))
        print("Added uid " + str(scan_id) + " to username user" + str(uid_num))
        set_should_add_next(False)
        return True
    else:
        return False

# The function that sends a high signal to the unlock_GPIO pin for a duration of time_s seconds.
def unlock():
    global time_s, unlock_GPIO
    print("Unlocked for " + str(time_s) + " seconds")
    GPIO.setup(unlock_GPIO, GPIO.OUT)  # GPIO Assign mode
    GPIO.output(unlock_GPIO, GPIO.LOW)  # out
    GPIO.output(unlock_GPIO, GPIO.HIGH)  # on
    time.sleep(time_s)  # sleep for set time
    GPIO.output(unlock_GPIO, GPIO.LOW)  # out
    return

# The callback for when the client receives a CONNECT response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("RFID_Scan")

def set_last_id(scan_id):
    global last_id
    last_id = scan_id
    return True


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global time_s
    last_id = get_last_id()
    scan_id = msg.payload.decode('utf-8')
    if msg.topic == "RFID_Scan" and scan_id != last_id:
        print("Previous UID " + str(last_id))
        print(msg.topic + " " + str(scan_id))
        if should_add(scan_id):
            return
        if add_uid(scan_id):
            set_last_id("0")
            return
        if should_unlock(scan_id):
            print("Access granted")
            client.publish("Door_Unlock", str(time_s))
            unlock()

def check_unlock_loop():
    global unlock_GPIO
    while True:
        try:
            unlock_hours_file = '/home/pi/rfid_lock/unlock_hours.csv'
            unlock_hours_dateparse = lambda x: pd.to_datetime(x, format='%Y-%m-%d %H:%M:%S')
            unlock_hours_csv = pd.read_csv(unlock_hours_file, parse_dates=['start_unlock','end_unlock'], date_parser=unlock_hours_dateparse)
            unlock_hours_df = pd.DataFrame(data=unlock_hours_csv)
            i = 0
            while i < len(unlock_hours_df):
                if_pad_unlock()
                unlock_start = unlock_hours_df.loc[i, 'start_unlock']
                unlock_end = unlock_hours_df.loc[i, 'end_unlock']
                time_now = datetime.datetime.now()
                if unlock_start <= time_now <= unlock_end:
                    unlock_delta_obj = unlock_end - time_now
                    unlock_seconds = unlock_delta_obj.total_seconds()
                    print("Unlocked for " + str(unlock_seconds) + " seconds")
                    GPIO.setup(unlock_GPIO, GPIO.OUT)  # GPIO Assign mode
                    GPIO.output(unlock_GPIO, GPIO.LOW)  # out
                    GPIO.output(unlock_GPIO, GPIO.HIGH)  # on
                    time.sleep(unlock_seconds)  # sleep for set time
                    print("Locked")
                    GPIO.output(unlock_GPIO, GPIO.LOW)  # out
                i += 1
            time.sleep(15.0)
        except (RuntimeError, TypeError, NameError, ValueError):
            pass
        finally:
            pass


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
x = threading.Thread(target=check_unlock_loop)
x.start()
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
