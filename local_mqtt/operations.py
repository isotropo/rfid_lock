import datetime
from datetime import date, time


# import and/or set parameter values
# unlock_time, whitelist: uid, user, usergroup: time_range[7]
uid = 5
usergroup = "default"
whitelist = {
    
}

def ifValid(uid,usergroup):
    
    day = date.today().weekday()
    now = datetime.datetime.now()
    hour = '{:02d}'.format(now.hour)
    minute = '{:02d}'.format(now.minute)
    print(day,hour,minute)
    # Check if user is present. If assigned usergroup, check if current time is within time_range[day]

