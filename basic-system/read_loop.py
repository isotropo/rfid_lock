import numpy as np
import pandas as pd
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import threading

reader = SimpleMFRC522()
whitelist = pd.read_csv('whitelist.csv')
whitelist_df = pd.DataFrame(data=whitelist)
uid_list = whitelist_df.loc[:,'uid']
admin_id = uid_list[0] 


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
                print('ADMIN ID!')
                add_users()
            elif should_unlock(uid):
                print(uid)
                unlock()
        finally:
                GPIO.cleanup()

# Scan id once. Used for add_users.
def scan_id():
    try:
        id, text = reader.read()
    finally:
        GPIO.cleanup()
    return id

# Admin method for adding new RFID tags to the whitelist.
def add_users():
    global whitelist_df
    while True:
        uid = scan_id()
        # print(str(uid)+" scanned")
        if not uid in uid_list:
           print("adding"+str(uid))
           whitelist_df = whitelist_df.append({'uid': str(uid)}, ignore_index=True) 
           update_uid_list()
        if uid == admin_id:
            update_csv()
            print("exiting add users mode")
            return

def update_uid_list():
     global uid_list
     global whitelist_df
     uid_list = whitelist_df.loc[:,'uid']
     return


# Export the modified whitelist_df dataframe to whitelist.csv
def update_csv():
    global whitelist_df
    print("updating csv")
    whitelist_df.to_csv(r'whitelist.csv')
    return

x = threading.Thread(target=read_loop)
x.start()
