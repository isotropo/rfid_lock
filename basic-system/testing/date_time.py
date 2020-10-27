# from datetime import datetime
# import datetime
# import time
# from datetime import time
# import datetime


from datetime import datetime
# n = datetime.now()
# t = n.timetuple()
# y, m, d, h, mins, sec, wd, yd, i = t
h = datetime.now().timetuple()[3:5]
print(h)

# n = datetime.datetime.now()
# t = n.timetuple()
# y, m, d, h, mins, sec, wd, yd, i = t

# print(h)

# print(date.today().weekday())

# year, month, day, hour, min = map(int, time.strftime("%Y %m %d %H %M").split())

# print(hour)

# hh = map(str, time.strftime("%H").split())
# print(hh)

# print(datetime.datetime.now().hour)

# def get_hour():
#     strings = time.strftime("%Y,%m,%d,%H,%M,%S")
#     t = strings.split(',')
#     numbers = [ int(x) for x in t ]
#     print numbers