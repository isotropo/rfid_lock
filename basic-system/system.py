import numpy as np
import pandas as pd
from time import gmtime, localtime
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522


reader = SimpleMFRC522()
whitelist = pd.read_csv('whitelist.csv')
whitelist_df = pd.DataFrame(data=whitelist)
uid_list = whitelist_df.loc[:,'uid']
admin_id = uid_list[0] 

# Function defs:

# Returns admin id
# def get_admin_id():
#     admin_id = uid_list[0]
#     # print(admin_id)
#     return admin_id

# Main function loop
def read_loop():
    while True:
        try:
            uid = scan_id()
            if uid == admin_id:
                print("ADMIN_ID")
                # add_users()
            # elif should_unlock(uid):
                # unlock()
        finally:
                GPIO.cleanup()

# Admin method for adding new RFID tags to the whitelist.
def add_users():
    while True:
        uid = scan_id()
        if not uid in uid_list:
            whitelist_df = whitelist_df.append({'uid': uid}, ignore_index=True) 
            # whitelist_append(uid,whitelist_df)
        if uid == admin_id:
            update_csv()
            return

# Scan id once. Used for add_users.
def scan_id():
    try:
        id, text = reader.read()
    finally:
        GPIO.cleanup()
    return id

# Append uid to whitelist.
# def whitelist_append(uid,whitelist_df):
#    whitelist_df = whitelist_df.append({'uid': uid}, ignore_index=True) 
#    return

# Export the modified whitelist_df dataframe to whitelist.csv
def update_csv():
    whitelist.to_csv(r'whitelist.csv')

def should_unlock(scan_id):
  for uid in uid_list:
    suid = str(uid)
    print(type(suid), type(scan_id))
    print(suid == scan_id, suid, scan_id)
    if str(uid) == str(scan_id):
        return True
    else:
        return False

def unlock():
    global time_ms
    GPIO.setup(unlock_GPIO, GPIO.OUT) # GPIO Assign mode
    GPIO.output(unlock_GPIO, GPIO.LOW) # out
    GPIO.output(unlock_GPIO, GPIO.HIGH) # on
    time.sleep(time_ms) # sleep for set time
    GPIO.output(unlock_GPIO, GPIO.LOW) # out


# set up dataframes
usergroups = pd.read_csv('usergroups.csv')
usergroups_df = pd.DataFrame(data=usergroups)

usergroups_list = usergroups_df.to_dict()

print(usergroups_list)

# Variable defs

time_ms = 10.0
unlock_GPIO = 23

GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
GPIO.setup(unlock_GPIO, GPIO.OUT) # GPIO Assign mode

# user_groups = {define user groups}

x = threading.Thread(target=read_loop)
x.start()
